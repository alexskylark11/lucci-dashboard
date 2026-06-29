"""
Build pod_recency.json: for every clean POD (samples excluded), determine
the most recent week they ordered Lucci by scanning all weekly Ethica
snapshots in chronological order. Days are computed relative to the
06.26.26 'as-of' date. Status thresholds: <=60d green, 60-90d yellow,
>=90d red (or pre-snapshot-history red).
"""
import pandas as pd
import re
import json
from datetime import datetime

PATH = r'C:\Users\AlexBerger\Downloads\Lucci_Product Locator File + Depletion report (13).xlsx'
AS_OF = datetime(2026, 6, 26)
OUT_JSON = r'C:\Users\AlexBerger\OneDrive - skylarkgrowth.com\Desktop\HRL Ratings System\lucci-dashboard\pod_recency.json'

SAMPLE_PATTERN = re.compile(
    r'SAMPLE|SAMPL\b|F\s*&\s*F\s*FINE\s*WINE|F&F\s*FINE\s*WINE|'
    r'SGWS-HOUSE|SGWS-TEAM|TEAM\s*#|'
    r'\bREP\s*#|\bSALES\s+REP|\bREP\s+\d|REPS?\b\s+\d{2,}|'
    r'\bETHICA\s+WINES?\b|UNCLASSIFIED\s+ACCOUNT|BERKELEY\s+BOWL\s*-\s*WAREHOUSE|'
    r'CORPORATE\s+WITHDRAW|WITHDRAWL|WITHDRAWAL',
    re.IGNORECASE
)
PERSON_NAME_PATTERN = re.compile(
    r'^[A-Z][a-z]+\s+[A-Z][a-z]+$|^[A-Z]\.\s*[A-Z][a-z]+|'
    r'^[A-Z][a-z]+\s+[A-Z]\.|^[A-Z][a-z]+,\s+[A-Z][a-z]+$',
)
# Known sales-rep allocations that the regex can't safely detect
HARDCODED_EXCLUDES = {"KRATZKE  ROBERT", "KRATZKE ROBERT"}

xls = pd.ExcelFile(PATH)

def parse_date(sheet):
    m = re.search(r'(\d{2})\.(\d{2})\.(\d{2})', sheet)
    if m:
        mm, dd, yy = m.groups()
        return datetime(2000 + int(yy), int(mm), int(dd))
    return None

dep_tabs = [s for s in xls.sheet_names if s.startswith('Depletions ') and parse_date(s)]
dep_tabs.sort(key=parse_date)
print(f"Found {len(dep_tabs)} weekly snapshots:")
for t in dep_tabs:
    print(f"  {t} -> {parse_date(t).date()}")

def load_snapshot(sheet):
    df = pd.read_excel(xls, sheet, header=None)
    n = df.shape[1]
    months_by_width = {
        24: ['Nov','Dec','Jan','Feb','Mar'],
        26: ['Nov','Dec','Jan','Feb','Mar','Apr'],
        28: ['Nov','Dec','Jan','Feb','Mar','Apr','May'],
        30: ['Nov','Dec','Jan','Feb','Mar','Apr','May','Jun'],
    }
    if n not in months_by_width:
        print(f"  [WARN] {sheet} has unexpected width {n}, skipping")
        return None
    months = months_by_width[n]
    cols = ['Premise','State','TradeChannel','Chain','RetailAcct','City']
    for m in months:
        cols += [f'{m}_Cases', f'{m}_PODs']
    cols += ['YTD_Cases','YTD_PODs','PY_Cases','PY_PODs',
             'Diff_Cases','Diff_PODs','Pct_Cases','Pct_PODs']
    df.columns = cols
    data = df.iloc[2:].copy()
    data['YTD_Cases'] = pd.to_numeric(data['YTD_Cases'], errors='coerce').fillna(0)
    data = data[(data['Chain']!='Total') & (data['State']!='Total') &
                (data['TradeChannel']!='Total') & (data['RetailAcct']!='Total')]
    return data

# Latest snapshot defines the universe of clean accounts.
latest = load_snapshot(dep_tabs[-1])
def is_excluded(r):
    text = f"{r['Chain']} {r['RetailAcct']}"
    acct_clean = str(r['RetailAcct']).strip().upper()
    if SAMPLE_PATTERN.search(text): return True
    if PERSON_NAME_PATTERN.match(str(r['RetailAcct'])): return True
    if acct_clean in HARDCODED_EXCLUDES: return True
    if r['YTD_Cases'] < 0.083: return True
    return False
latest['IsEx'] = latest.apply(is_excluded, axis=1)
clean = latest[~latest['IsEx']].copy()
print(f"\nClean universe (latest snapshot): {len(clean)} PODs")

def key(r):
    return (str(r['RetailAcct']).strip().upper(),
            str(r['City']).strip().upper(),
            str(r['State']).strip().upper())

# Walk snapshots chronologically; track each account's last-increase date
last_order = {}
prev_ytd = {}
for tab in dep_tabs:
    snap_date = parse_date(tab)
    snap = load_snapshot(tab)
    if snap is None:
        continue
    for _, r in snap.iterrows():
        k = key(r)
        try:
            ytd = float(r['YTD_Cases'])
        except (ValueError, TypeError):
            ytd = 0
        if ytd <= 0:
            continue
        prev = prev_ytd.get(k, 0)
        if ytd > prev + 0.001:  # cumulative increased = activity in this week
            last_order[k] = snap_date
            prev_ytd[k] = ytd
        elif k not in prev_ytd:
            # Account first appears here with YTD>0 -- earliest visible activity
            last_order[k] = snap_date
            prev_ytd[k] = ytd

first_snap_date = parse_date(dep_tabs[0])
results = []
for _, r in clean.iterrows():
    k = key(r)
    last_dt = last_order.get(k)
    if last_dt:
        days = (AS_OF - last_dt).days
        last_str = f"{last_dt.month}/{last_dt.day}/{str(last_dt.year)[-2:]}"
    else:
        days = 999
        last_str = "—"
    if days <= 60:
        status = "Green"
    elif days <= 90:
        status = "Yellow"
    else:
        status = "Red"
    results.append({
        "account": str(r['RetailAcct']),
        "city": str(r['City']),
        "state": str(r['State']),
        "premise": str(r['Premise']).strip(),
        "chain": str(r['Chain']) if r['Chain'] != 'INDEPENDENTS' else '(indep)',
        "channel": str(r['TradeChannel']).strip(),
        "ytd_cases": round(float(r['YTD_Cases']), 2),
        "last_order_date": last_str,
        "days_since": int(days),
        "status": status,
    })

# Sort: Red first, then Yellow, then Green; within each by days desc
status_order = {"Red": 0, "Yellow": 1, "Green": 2}
results.sort(key=lambda x: (status_order[x['status']], -x['days_since'], -x['ytd_cases']))

# Summary
from collections import Counter
status_counts = Counter(r['status'] for r in results)
print(f"\nStatus breakdown:")
for s in ['Red', 'Yellow', 'Green']:
    print(f"  {s}: {status_counts[s]}")
print(f"  Total: {len(results)}")

with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump({
        "as_of": AS_OF.strftime("%Y-%m-%d"),
        "snapshots_used": [parse_date(t).strftime("%Y-%m-%d") for t in dep_tabs],
        "earliest_snapshot": first_snap_date.strftime("%Y-%m-%d"),
        "thresholds": {"green_max_days": 60, "yellow_max_days": 90},
        "pods": results,
    }, f, indent=2)
print(f"\nWrote {OUT_JSON}")

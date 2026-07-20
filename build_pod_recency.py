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

PATH = r'C:\Users\AlexBerger\Downloads\Lucci_Product Locator File + Depletion report (15).xlsx'
AS_OF = datetime(2026, 7, 17)
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
    r'^[A-Z][a-z]+\s+[A-Z]\.|^[A-Z][a-z]+,\s+[A-Z][a-z]+$|'
    # Firstname McSomething or O'Something (mixed-case surname)
    r'^[A-Z][a-z]+\s+[A-Z][a-zA-Z]+$|'
    # Firstname Middle Lastname (three Title Case tokens)
    r'^[A-Z][a-z]+\s+[A-Z][a-z]*\s+[A-Z][a-zA-Z]+$|'
    # ALL-CAPS two-token names of length >= 4 each (LASTNAME  FIRSTNAME)
    r'^[A-Z]{4,}\s{1,4}[A-Z]{3,}$',
)
# Trade channels that are effectively sample / rep allocations, not real
# retail distribution points
NON_RETAIL_CHANNELS = {'NON-RETAIL'}
# Known sales-rep allocations that the regex can't safely detect
HARDCODED_EXCLUDES = {"KRATZKE  ROBERT", "KRATZKE ROBERT"}

xls = pd.ExcelFile(PATH)

def parse_date(sheet):
    m = re.search(r'(\d{2})\.(\d{2})\.(\d{2})', sheet)
    if m:
        mm, dd, yy = m.groups()
        return datetime(2000 + int(yy), int(mm), int(dd))
    return None

# Catch both plural 'Depletions ' and singular 'Depletion ' tabs (the newer
# July snapshots switched to the singular form).
dep_tabs = [s for s in xls.sheet_names
            if re.match(r'Depletions?\s+\d{2}\.\d{2}\.\d{2}$', s) and parse_date(s)]
dep_tabs.sort(key=parse_date)
print(f"Found {len(dep_tabs)} weekly snapshots:")
for t in dep_tabs:
    print(f"  {t} -> {parse_date(t).date()}")

def _find_header_row(df):
    """Return (header_row_index, first_data_col) by scanning rows 1-3 for
    Ethica's 'On/Off Premise' column-header signature."""
    for i in [1, 2]:
        row_vals = [str(v).lower().strip() for v in df.iloc[i].tolist()]
        if row_vals and 'premise' in row_vals[0]:
            for j, v in enumerate(row_vals):
                if '9 liter' in v:
                    return i, j
    return None, None

def load_snapshot(sheet):
    """Load a snapshot, auto-detecting the layout Ethica used in this tab.
    Different tabs have different column counts AND different row structures
    (07.03 vs 07.10 both have 33 cols but different entity col counts;
    old files have headers on row 1 with data on row 2; new files have
    date-descriptions on row 1, headers on row 2, data on row 3)."""
    df = pd.read_excel(xls, sheet, header=None)
    n = df.shape[1]
    header_row_idx, first_data_col = _find_header_row(df)
    if header_row_idx is None:
        print(f"  [WARN] {sheet}: could not locate header row, skipping")
        return None
    data_start_row = header_row_idx + 1

    # Entity col count = first_data_col
    if first_data_col == 7:
        entity_cols = ['Premise','State','TradeChannel','Chain','RetailAcct','Premise2','City']
    elif first_data_col == 6:
        entity_cols = ['Premise','State','TradeChannel','Chain','RetailAcct','City']
    else:
        print(f"  [WARN] {sheet}: unexpected entity col count {first_data_col}, skipping")
        return None

    # Compute how many month pairs and trailing filler columns
    remaining = n - first_data_col
    # Summary block is 8 cols (YTD_C, YTD_P, PY_C, PY_P, Diff_C, Diff_P, Pct_C, Pct_P)
    # Trailing nan column varies; if the math works with 0 trailing, use that
    for trailing in (0, 1):
        month_cols = remaining - 8 - trailing
        if month_cols >= 2 and month_cols % 2 == 0:
            n_months = month_cols // 2
            all_months = ['Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul']
            if 1 <= n_months <= len(all_months):
                months = all_months[:n_months]
                cols = list(entity_cols)
                for m in months:
                    cols += [f'{m}_Cases', f'{m}_PODs']
                cols += ['YTD_Cases','YTD_PODs','PY_Cases','PY_PODs',
                         'Diff_Cases','Diff_PODs','Pct_Cases','Pct_PODs']
                if trailing:
                    cols.append('_trailing')
                if len(cols) == n:
                    df.columns = cols
                    data = df.iloc[data_start_row:].copy()
                    data['YTD_Cases'] = pd.to_numeric(data['YTD_Cases'], errors='coerce').fillna(0)
                    data = data[(data['Chain']!='Total') & (data['State']!='Total') &
                                (data['TradeChannel']!='Total') & (data['RetailAcct']!='Total')]
                    return data
    print(f"  [WARN] {sheet}: could not fit layout to width {n}, skipping")
    return None

# Latest snapshot defines the universe of clean accounts.
latest = load_snapshot(dep_tabs[-1])
# Coerce monthly columns for the latest snapshot so we can copy them into results
_LATEST_MONTHS = ['Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul']
for _m in _LATEST_MONTHS:
    if f'{_m}_Cases' in latest.columns:
        latest[f'{_m}_Cases'] = pd.to_numeric(latest[f'{_m}_Cases'], errors='coerce').fillna(0)
def is_excluded(r):
    text = f"{r['Chain']} {r['RetailAcct']}"
    acct_clean = str(r['RetailAcct']).strip().upper()
    channel_clean = str(r['TradeChannel']).strip().upper()
    if SAMPLE_PATTERN.search(text): return True
    if PERSON_NAME_PATTERN.match(str(r['RetailAcct'])): return True
    if acct_clean in HARDCODED_EXCLUDES: return True
    if channel_clean in NON_RETAIL_CHANNELS: return True
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
    row = {
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
    }
    for m in _LATEST_MONTHS:
        col = f'{m}_Cases'
        row[m.lower()] = round(float(r[col]), 2) if col in r.index else 0
    results.append(row)

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

# ── DEDUP SANITY CHECKS ──────────────────────────────────────────────────────
# Big chains (Food Lion, Total Wine, BevMo, etc.) often have many stores in the
# same state. We want to confirm that any 'new this week' store and any 'stale
# Red' store within the same chain+state are GENUINELY different physical
# locations, not the same store double-counted via name-format dupes.
print("\n" + "=" * 80)
print("DEDUP SANITY CHECKS")
print("=" * 80)

# Identify accounts new-this-week by comparing latest snapshot to the second-latest
if len(dep_tabs) >= 2:
    prior_clean = load_snapshot(dep_tabs[-2])
    prior_clean['IsEx'] = prior_clean.apply(is_excluded, axis=1)
    prior_clean = prior_clean[~prior_clean['IsEx']]
    prior_keys = set(prior_clean.apply(key, axis=1))
    clean['Key'] = clean.apply(key, axis=1)
    clean['IsNewThisWeek'] = ~clean['Key'].isin(prior_keys)
else:
    clean['IsNewThisWeek'] = False

# Extract numeric store ID from account name (handles 'FOOD LION 1330',
# '#1330', 'TOTAL WINE & MORE #1503-MILFORD', etc.)
def extract_store_id(name):
    s = str(name).upper().replace('#', '').strip()
    m = re.search(r'\b(\d{2,5})\b(?!\s*\d)', s)
    return m.group(1) if m else None

clean['StoreID'] = clean['RetailAcct'].apply(extract_store_id)

# Attach status from results
results_lookup = {(p['account'].strip().upper(),
                   p['city'].strip().upper(),
                   p['state'].strip().upper()): p['status'] for p in results}
clean['Status'] = clean['Key'].map(lambda k: results_lookup.get(k))

# Check 1: within each chain+state, are there duplicate store IDs?
print("\nCheck 1 — Duplicate store IDs within same chain+state:")
dup_problems = 0
for (chn, st), grp in clean[clean['StoreID'].notna()].groupby(['Chain', 'State']):
    id_counts = grp['StoreID'].value_counts()
    dupes = id_counts[id_counts > 1]
    for sid, cnt in dupes.items():
        rows = grp[grp['StoreID'] == sid]
        accts = sorted(set(rows['RetailAcct'].astype(str)))
        if len(accts) > 1:  # different formats of same store ID
            dup_problems += 1
            print(f"  [WARN] {chn} {st} store ID {sid} appears {cnt}x with different names: {accts}")
if dup_problems == 0:
    print("  [OK] No duplicate store IDs within any chain+state.")

# Check 2: within each chain+state, do new-this-week store IDs overlap with stale Red store IDs?
print("\nCheck 2 — Same store ID flagged BOTH new-this-week AND stale (Red):")
overlap_problems = 0
for (chn, st), grp in clean[clean['StoreID'].notna()].groupby(['Chain', 'State']):
    new_ids = set(grp.loc[grp['IsNewThisWeek'], 'StoreID'].dropna())
    red_ids = set(grp.loc[grp['Status'] == 'Red', 'StoreID'].dropna())
    overlap = new_ids & red_ids
    if overlap:
        overlap_problems += 1
        print(f"  [WARN] {chn} {st}: store IDs in BOTH new and Red: {sorted(overlap)}")
if overlap_problems == 0:
    print("  [OK] No store ID overlap between new-this-week and stale buckets.")

# Check 3: for the biggest chains (>=10 stores in any state), print a chain-state summary
print("\nCheck 3 — Big-chain summary (chains with 10+ stores in a single state):")
big_groups = clean.groupby(['Chain', 'State']).size().reset_index(name='n')
big_groups = big_groups[big_groups['n'] >= 10].sort_values('n', ascending=False)
for _, row in big_groups.iterrows():
    grp = clean[(clean['Chain'] == row['Chain']) & (clean['State'] == row['State'])]
    n_new = int(grp['IsNewThisWeek'].sum())
    n_red = int((grp['Status'] == 'Red').sum())
    n_yel = int((grp['Status'] == 'Yellow').sum())
    n_grn = int((grp['Status'] == 'Green').sum())
    n_ids = grp['StoreID'].notna().sum()
    n_unique_ids = grp['StoreID'].dropna().nunique()
    note = ""
    if n_ids != n_unique_ids:
        note = f"  [WARN] {n_ids - n_unique_ids} duplicate store ID(s)"
    print(f"  {row['Chain']!s:<28} {row['State']}: {int(row['n'])} total · "
          f"new={n_new} · Red={n_red} · Yellow={n_yel} · Green={n_grn} · "
          f"unique_store_ids={n_unique_ids}/{n_ids}{note}")

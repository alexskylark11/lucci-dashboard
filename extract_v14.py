"""Extract clean depletion data from Lucci report (14).xlsx (through 7/10/26)."""
import pandas as pd
import re
from datetime import datetime

path = r'C:\Users\AlexBerger\Downloads\Lucci_Product Locator File + Depletion report (14).xlsx'
xls = pd.ExcelFile(path)

def parse_date(s):
    m = re.search(r'(\d{2})\.(\d{2})\.(\d{2})', s)
    if m:
        mm, dd, yy = m.groups()
        return datetime(2000 + int(yy), int(mm), int(dd))
    return None

# Catch both 'Depletions ' (plural) and 'Depletion ' (singular) tabs
dep_tabs = [s for s in xls.sheet_names if re.match(r'Depletions?\s+\d{2}\.\d{2}\.\d{2}$', s)]
dep_tabs.sort(key=parse_date)
latest = dep_tabs[-1]
print(f"All snapshot tabs ({len(dep_tabs)}):")
for t in dep_tabs:
    print(f"  {t}")
print(f"\nUsing latest: {latest}")

df_raw = pd.read_excel(xls, latest, header=None)
n = df_raw.shape[1]
print(f"Shape: {df_raw.shape}")

# The 07.10.26 file introduced a new layout: a duplicate Premise column at
# index 5, data starts on row 3 instead of row 2, and Jul columns.
months_by_width = {
    24: (['Nov','Dec','Jan','Feb','Mar'], False, 2),
    26: (['Nov','Dec','Jan','Feb','Mar','Apr'], False, 2),
    28: (['Nov','Dec','Jan','Feb','Mar','Apr','May'], False, 2),
    30: (['Nov','Dec','Jan','Feb','Mar','Apr','May','Jun'], False, 2),
    33: (['Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul'], True, 3),
}
if n not in months_by_width:
    print(f"[WARN] Unexpected width {n}, checking first 3 rows...")
    print(df_raw.iloc[0:3].to_string())
    raise SystemExit
months, has_extra_premise_col, data_start_row = months_by_width[n]
if has_extra_premise_col:
    cols = ['Premise','State','TradeChannel','Chain','RetailAcct','Premise2','City']
else:
    cols = ['Premise','State','TradeChannel','Chain','RetailAcct','City']
for m in months:
    cols += [f'{m}_Cases', f'{m}_PODs']
cols += ['YTD_Cases','YTD_PODs','PY_Cases','PY_PODs',
         'Diff_Cases','Diff_PODs','Pct_Cases','Pct_PODs']
df_raw.columns = cols

HAS_JUL = 'Jul' in months
HAS_JUN = 'Jun' in months
print(f"Has Jul: {HAS_JUL}, Has Jun: {HAS_JUN}")
print(f"Months: {months}")

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
    r'^[A-Z][a-z]+\s+[A-Z][a-zA-Z]+$|'
    r'^[A-Z][a-z]+\s+[A-Z][a-z]*\s+[A-Z][a-zA-Z]+$|'
    r'^[A-Z]{4,}\s{1,4}[A-Z]{3,}$',
)
NON_RETAIL_CHANNELS = {'NON-RETAIL'}
HARDCODED_EXCLUDES = {"KRATZKE  ROBERT", "KRATZKE ROBERT"}

data = df_raw.iloc[data_start_row:].copy()
for m in months:
    data[f'{m}_Cases'] = pd.to_numeric(data[f'{m}_Cases'], errors='coerce').fillna(0)
    data[f'{m}_PODs'] = pd.to_numeric(data[f'{m}_PODs'], errors='coerce').fillna(0)
data['YTD_Cases'] = pd.to_numeric(data['YTD_Cases'], errors='coerce').fillna(0)
data['YTD_PODs'] = pd.to_numeric(data['YTD_PODs'], errors='coerce').fillna(0)

detail = data[(data['Chain'] != 'Total') & (data['State'] != 'Total') &
              (data['TradeChannel'] != 'Total') & (data['RetailAcct'] != 'Total')].copy()

def is_excluded(r):
    text = f"{r['Chain']} {r['RetailAcct']}"
    acct = str(r['RetailAcct']).strip().upper()
    channel = str(r['TradeChannel']).strip().upper()
    if SAMPLE_PATTERN.search(text): return True
    if PERSON_NAME_PATTERN.match(str(r['RetailAcct'])): return True
    if acct in HARDCODED_EXCLUDES: return True
    if channel in NON_RETAIL_CHANNELS: return True
    if r['YTD_Cases'] < 0.083: return True
    return False

detail['IsEx'] = detail.apply(is_excluded, axis=1)
clean = detail[~detail['IsEx']].copy()
print(f"\nEXCLUDED: {detail['IsEx'].sum()} rows / "
      f"{detail[detail['IsEx']]['YTD_Cases'].sum():.2f} cases / "
      f"{int(detail[detail['IsEx']]['YTD_PODs'].sum())} PODs")
print(f"CLEAN: {len(clean)} PODs / {clean['YTD_Cases'].sum():.2f} cases")

print("\n" + "=" * 80)
print("CLEAN GRAND TOTALS")
for prem_label in ['ALL', 'ON', 'OFF']:
    sub = clean if prem_label == 'ALL' else clean[clean['Premise'].str.strip()==prem_label]
    print(f"\n{prem_label}:")
    for m in months:
        c = sub[f'{m}_Cases'].sum()
        p = sub[f'{m}_PODs'].sum()
        print(f"  {m}: Cases={c:.2f} PODs={int(p)}")
    print(f"  YTD: Cases={sub['YTD_Cases'].sum():.2f}, PODs={int(sub['YTD_PODs'].sum())}")

print("\n" + "=" * 80)
print("STATE-LEVEL CLEAN")
for prem in ['ON', 'OFF']:
    sub = clean[clean['Premise'].str.strip()==prem]
    print(f"\n{prem}-PREMISE:")
    agg = {'YTD_Cases':'sum','YTD_PODs':'sum'}
    for m in ['Apr','May','Jun','Jul']:
        if m in months:
            agg[f'{m}_Cases'] = 'sum'
            agg[f'{m}_PODs'] = 'sum'
    sg = sub.groupby('State').agg(agg).sort_values('YTD_Cases', ascending=False)
    for st, r in sg.iterrows():
        line = f"  {st}: YTD={r['YTD_Cases']:.2f}({int(r['YTD_PODs'])})"
        for m in ['Apr','May','Jun','Jul']:
            if m in months and f'{m}_Cases' in r.index:
                line += f", {m}={r[f'{m}_Cases']:.2f}({int(r[f'{m}_PODs'])})"
        print(line)

print("\n" + "=" * 80)
print("TOP CHAINS (clean)")
sub = clean[clean['Chain'] != 'INDEPENDENTS']
agg = {'YTD_Cases':'sum','YTD_PODs':'sum'}
for m in ['Apr','May','Jun','Jul']:
    if m in months:
        agg[f'{m}_Cases'] = 'sum'
cg = sub.groupby(['Chain','Premise']).agg(agg).reset_index().sort_values('YTD_Cases', ascending=False).head(30)
for _, r in cg.iterrows():
    line = f"  {r['Chain']} ({r['Premise'].strip()}): YTD={r['YTD_Cases']:.2f}({int(r['YTD_PODs'])})"
    for m in ['Apr','May','Jun','Jul']:
        if m in months:
            line += f", {m}={r[f'{m}_Cases']:.2f}"
    print(line)

print("\n" + "=" * 80)
print("KEY STATES TOP ACCOUNTS")
sub = clean[clean['Chain'] != 'INDEPENDENTS']
for st in ['CA','NY','NJ','FL','IL','TX']:
    print(f"\n--- {st} ---")
    ss = sub[sub['State']==st]
    agg2 = {'YTD_Cases':'sum','YTD_PODs':'sum'}
    for m in ['Apr','May','Jun','Jul']:
        if m in months:
            agg2[f'{m}_Cases'] = 'sum'
    sa = ss.groupby(['Chain','Premise']).agg(agg2).reset_index().sort_values('YTD_Cases', ascending=False).head(13)
    for _, r in sa.iterrows():
        line = f"  {r['Chain']} ({r['Premise'].strip()}): YTD={r['YTD_Cases']:.2f}({int(r['YTD_PODs'])})"
        for m in ['Apr','May','Jun','Jul']:
            if m in months:
                line += f", {m}={r[f'{m}_Cases']:.2f}"
        print(line)

print("\n" + "=" * 80)
print("TOP RESTAURANTS / BARS (clean)")
rest = clean[clean['TradeChannel'].str.strip().str.upper().isin(['RESTAURANT','BAR/TAVERN','FINE DINING/ WHITE TABLECLOTH'])].copy()
agg3 = {'YTD_Cases':'sum','YTD_PODs':'sum'}
for m in ['Mar','Apr','May','Jun','Jul']:
    if m in months:
        agg3[f'{m}_Cases'] = 'sum'
top = rest.groupby(['RetailAcct','Chain','State','City','TradeChannel']).agg(agg3).reset_index().sort_values('YTD_Cases', ascending=False).head(15)
for i, (_, r) in enumerate(top.iterrows(), 1):
    chain = r['Chain'] if r['Chain'] != 'INDEPENDENTS' else '(indep)'
    print(f"{i}. {r['RetailAcct']} - {r['City']}, {r['State']} [{chain} / {r['TradeChannel']}]")
    parts = []
    for m in ['Mar','Apr','May','Jun','Jul']:
        if m in months:
            parts.append(f"{m}={r[f'{m}_Cases']:.2f}")
    print(f"   YTD: {r['YTD_Cases']:.2f} - " + " ".join(parts))

print("\n" + "=" * 80)
print("TRADE CHANNELS (clean)")
for prem in ['ON','OFF']:
    sub = clean[clean['Premise'].str.strip()==prem]
    agg4 = {'YTD_Cases':'sum'}
    for m in ['Dec','Jan','Feb','Mar','Apr','May','Jun','Jul']:
        if m in months:
            agg4[f'{m}_Cases'] = 'sum'
    tc = sub.groupby('TradeChannel').agg(agg4).sort_values('YTD_Cases', ascending=False)
    print(f"\n{prem}-PREMISE:")
    for tcn, r in tc.iterrows():
        line = f"  {tcn}: YTD={r['YTD_Cases']:.2f}"
        for m in ['Dec','Jan','Feb','Mar','Apr','May','Jun','Jul']:
            if m in months:
                line += f", {m}={r[f'{m}_Cases']:.2f}"
        print(line)

"""
Cross-check: are the 16 'new this week' Food Lion NC stores DIFFERENT physical
locations than the Food Lion NC stores flagged Red (90+ days stale)?

Approach:
1. Pull all Food Lion NC accounts from the latest (06.26.26) clean universe.
2. Tag each as new-this-week (delta from 06.19.26) or stale (last order pre-3/28).
3. Extract a numeric store ID from the account name (e.g., 'FOOD LION 1330' -> 1330).
4. Report:
   - Total Food Lion NC stores
   - New this week: count + list with store IDs
   - Stale (Red): count + list with store IDs
   - ANY overlap in store IDs (which would indicate a data quality / dedup bug)
"""
import pandas as pd
import re
import json
from datetime import datetime

PATH = r'C:\Users\AlexBerger\Downloads\Lucci_Product Locator File + Depletion report (13).xlsx'
RECENCY_JSON = r'C:\Users\AlexBerger\OneDrive - skylarkgrowth.com\Desktop\HRL Ratings System\lucci-dashboard\pod_recency.json'

xls = pd.ExcelFile(PATH)

def parse_date(s):
    m = re.search(r'(\d{2})\.(\d{2})\.(\d{2})', s)
    if m:
        mm, dd, yy = m.groups()
        return datetime(2000 + int(yy), int(mm), int(dd))
    return None

cols_30 = ['Premise','State','TradeChannel','Chain','RetailAcct','City',
           'Nov_Cases','Nov_PODs','Dec_Cases','Dec_PODs','Jan_Cases','Jan_PODs',
           'Feb_Cases','Feb_PODs','Mar_Cases','Mar_PODs','Apr_Cases','Apr_PODs',
           'May_Cases','May_PODs','Jun_Cases','Jun_PODs','YTD_Cases','YTD_PODs',
           'PY_Cases','PY_PODs','Diff_Cases','Diff_PODs','Pct_Cases','Pct_PODs']

def load(sheet):
    df = pd.read_excel(xls, sheet, header=None)
    df.columns = cols_30
    data = df.iloc[2:].copy()
    data['YTD_Cases'] = pd.to_numeric(data['YTD_Cases'], errors='coerce').fillna(0)
    return data[(data['Chain']!='Total') & (data['State']!='Total') &
                (data['TradeChannel']!='Total') & (data['RetailAcct']!='Total')]

curr = load('Depletions 06.26.26')
prior = load('Depletions 06.19.26')

# Food Lion NC universe in latest snapshot
fl_curr = curr[(curr['Chain'].astype(str).str.upper().str.contains('FOOD LION'))
               & (curr['State'] == 'NC')].copy()
fl_prior = prior[(prior['Chain'].astype(str).str.upper().str.contains('FOOD LION'))
                 & (prior['State'] == 'NC')].copy()

def key(r):
    return (str(r['RetailAcct']).strip().upper(),
            str(r['City']).strip().upper(),
            str(r['State']).strip().upper())

prior_keys = set(fl_prior.apply(key, axis=1))
fl_curr['Key'] = fl_curr.apply(key, axis=1)
fl_curr['IsNewThisWeek'] = ~fl_curr['Key'].isin(prior_keys)

def store_id(name):
    """Extract numeric store ID from 'FOOD LION 1330' / 'FOOD LION #1330'."""
    s = str(name).upper().replace('FOOD LION', '').replace('#', '').strip()
    m = re.search(r'\b(\d{3,5})\b', s)
    return m.group(1) if m else None

fl_curr['StoreID'] = fl_curr['RetailAcct'].apply(store_id)

# Load recency to flag stale stores
recency = json.load(open(RECENCY_JSON, encoding='utf-8'))
recency_map = {}
for p in recency['pods']:
    k = (p['account'].strip().upper(), p['city'].strip().upper(), p['state'].strip().upper())
    recency_map[k] = p

fl_curr['Status'] = fl_curr['Key'].map(lambda k: recency_map.get(k, {}).get('status', '?'))
fl_curr['LastOrder'] = fl_curr['Key'].map(lambda k: recency_map.get(k, {}).get('last_order_date', '?'))
fl_curr['DaysSince'] = fl_curr['Key'].map(lambda k: recency_map.get(k, {}).get('days_since', 0))

print("=" * 100)
print(f"FOOD LION NC AUDIT — Total stores in 06.26.26: {len(fl_curr)}")
print("=" * 100)
print(f"\nStatus breakdown:")
print(fl_curr.groupby('Status').size().to_string())

new_stores = fl_curr[fl_curr['IsNewThisWeek']]
red_stores = fl_curr[fl_curr['Status'] == 'Red']
yellow_stores = fl_curr[fl_curr['Status'] == 'Yellow']

print(f"\n— NEW this week (6/20-6/26): {len(new_stores)} stores —")
for _, r in new_stores.sort_values('YTD_Cases', ascending=False).iterrows():
    print(f"  StoreID={r['StoreID']!s:<6} | {r['RetailAcct']!s:<32} | {r['City']!s:<18} | YTD={r['YTD_Cases']:.2f} | last={r['LastOrder']}")

print(f"\n— STALE (Red, 90+d): {len(red_stores)} stores —")
for _, r in red_stores.sort_values('YTD_Cases', ascending=False).iterrows():
    print(f"  StoreID={r['StoreID']!s:<6} | {r['RetailAcct']!s:<32} | {r['City']!s:<18} | YTD={r['YTD_Cases']:.2f} | last={r['LastOrder']} ({r['DaysSince']}d)")

print(f"\n— YELLOW (60-90d): {len(yellow_stores)} stores —")
for _, r in yellow_stores.sort_values('YTD_Cases', ascending=False).iterrows():
    print(f"  StoreID={r['StoreID']!s:<6} | {r['RetailAcct']!s:<32} | {r['City']!s:<18} | YTD={r['YTD_Cases']:.2f} | last={r['LastOrder']} ({r['DaysSince']}d)")

# OVERLAP CHECK — Same store ID appearing in both 'new' AND 'stale' bucket
print("\n" + "=" * 100)
print("OVERLAP CHECK: same physical store flagged as BOTH new and stale?")
print("=" * 100)
new_ids = set(new_stores['StoreID'].dropna().tolist())
red_ids = set(red_stores['StoreID'].dropna().tolist())
yellow_ids = set(yellow_stores['StoreID'].dropna().tolist())
overlap_new_red = new_ids & red_ids
overlap_new_yellow = new_ids & yellow_ids
if overlap_new_red:
    print(f"  [WARN]  CONFLICT: store IDs in BOTH new-this-week AND stale-red: {overlap_new_red}")
    for sid in overlap_new_red:
        for _, r in fl_curr[fl_curr['StoreID'] == sid].iterrows():
            print(f"    StoreID={sid}: {r['RetailAcct']!s} | {r['City']} | new={r['IsNewThisWeek']} | status={r['Status']}")
else:
    print("  [OK] No overlap between 'new this week' and 'stale Red' store IDs.")

if overlap_new_yellow:
    print(f"  [WARN]  store IDs in BOTH new-this-week AND yellow: {overlap_new_yellow}")
else:
    print("  [OK] No overlap between 'new this week' and 'yellow' store IDs.")

# Also check: any duplicate store IDs within the FULL Food Lion NC list?
print("\n— DUPLICATE STORE ID CHECK (within all Food Lion NC) —")
id_counts = fl_curr['StoreID'].value_counts()
dupes = id_counts[id_counts > 1]
if len(dupes) > 0:
    print(f"  [WARN]  {len(dupes)} store IDs appear MULTIPLE times (likely format dupes):")
    for sid, cnt in dupes.items():
        print(f"    StoreID={sid} ({cnt}×):")
        for _, r in fl_curr[fl_curr['StoreID'] == sid].iterrows():
            print(f"      {r['RetailAcct']!s} | {r['City']} | YTD={r['YTD_Cases']:.2f} | status={r['Status']}")
else:
    print("  [OK] No duplicate store IDs in Food Lion NC.")

# How many stores have NO extractable ID?
no_id = fl_curr[fl_curr['StoreID'].isna()]
print(f"\n— Stores with no numeric ID extracted: {len(no_id)} —")
for _, r in no_id.iterrows():
    print(f"  {r['RetailAcct']!s} | {r['City']} | status={r['Status']}")

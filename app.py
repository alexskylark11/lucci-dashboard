import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LUCCI Dashboard",
    page_icon=":wine_glass:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── BRAND PALETTE ────────────────────────────────────────────────────────────
RED = "#8B1A1A"
RED_MID = "#A52020"
RED_PALE = "#C8897F"
RED_FAINT = "#EEDBD8"
CREAM = "#F2EDD7"
CREAM_DARK = "#E8E0C0"
WHITE = "#FFFDF5"
TEXT_DARK = "#2C1A0E"
TEXT_MID = "#5C3A1E"
TEXT_LIGHT = "#8B6347"

FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
FONT_DISPLAY = "'Inter', 'Helvetica Neue', Arial, sans-serif"

# ── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

html, body, [class*="css"] {{
    font-family: {FONT} !important;
}}
.main .block-container {{ padding-top: 0; }}

.lucci-header {{
    background: {RED};
    border-bottom: 4px solid {TEXT_DARK};
    padding: 20px 40px;
    margin: -1rem -1rem 1.5rem -1rem;
}}
.lucci-title {{
    font-family: {FONT_DISPLAY};
    font-size: 36px;
    font-weight: 900;
    color: white;
    letter-spacing: 0.06em;
    line-height: 1;
}}
.lucci-subtitle {{
    font-size: 12px;
    color: rgba(255,255,255,0.65);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-left: 14px;
    font-weight: 500;
}}
.lucci-period {{
    font-size: 11px;
    color: rgba(255,255,255,0.5);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4px;
}}

.kpi-card {{
    border: 2px solid {RED_FAINT};
    padding: 20px 22px;
    background: {WHITE};
    display: flex;
    flex-direction: column;
    gap: 4px;
    height: 100%;
    min-height: 110px;
    border-radius: 6px;
    box-sizing: border-box;
}}
.kpi-card-dark {{
    border: 2px solid {RED};
    padding: 20px 22px;
    background: {RED};
    display: flex;
    flex-direction: column;
    gap: 4px;
    height: 100%;
    min-height: 110px;
    border-radius: 6px;
    box-sizing: border-box;
}}
.kpi-label {{
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {TEXT_MID};
    font-weight: 600;
}}
.kpi-label-dark {{
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {RED_FAINT};
    font-weight: 600;
}}
.kpi-value {{
    font-size: 32px;
    font-weight: 900;
    color: {RED};
    font-family: {FONT_DISPLAY};
    line-height: 1.1;
}}
.kpi-value-dark {{
    font-size: 32px;
    font-weight: 900;
    color: white;
    font-family: {FONT_DISPLAY};
    line-height: 1.1;
}}
.kpi-sub {{
    font-size: 13px;
    color: {TEXT_MID};
}}
.kpi-sub-dark {{
    font-size: 13px;
    color: rgba(255,255,255,0.7);
}}

.section-title {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}}
.section-bar {{
    width: 4px;
    height: 22px;
    background: {RED};
    display: inline-block;
    border-radius: 2px;
}}
.section-text {{
    font-size: 13px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {RED};
    font-weight: 800;
}}

.highlight-banner {{
    background: {RED};
    border: 3px solid {TEXT_DARK};
    padding: 22px 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    margin-top: 1rem;
    border-radius: 6px;
}}

.footer-text {{
    text-align: center;
    color: {TEXT_MID};
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 2rem;
}}

/* Table legibility */
table {{ font-size: 13px !important; }}
thead tr th {{
    background: {RED} !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}}

/* Streamlit overrides for legibility */
.stDataFrame {{ font-size: 13px; }}
div[data-testid="stMetricValue"] {{ font-size: 28px !important; }}

/* Custom styled table */
.styled-table {{
    width: 100%;
    border-collapse: collapse;
    font-family: {FONT};
    font-size: 13px;
    margin-bottom: 1rem;
}}
.styled-table thead th {{
    background: {TEXT_DARK} !important;
    color: white !important;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 10px 12px;
    text-align: left;
    border: 1px solid {TEXT_DARK};
}}
.styled-table tbody td {{
    padding: 8px 12px;
    border: 1px solid {CREAM_DARK};
    color: {TEXT_DARK};
}}
.styled-table tbody tr:nth-child(odd) {{
    background: {CREAM};
}}
.styled-table tbody tr:nth-child(even) {{
    background: {WHITE};
}}
.styled-table .positive {{
    color: #1a7a1a;
    font-weight: 600;
}}
.styled-table .negative {{
    color: {RED};
    font-weight: 600;
}}
</style>
""", unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="lucci-header">
    <div style="display:flex; align-items:baseline; justify-content:space-between;">
        <div style="display:flex; align-items:baseline;">
            <span class="lucci-title">LUCCI</span>
            <span class="lucci-subtitle">Lambrusco Reggiano DOC</span>
        </div>
        <div style="text-align:right;">
            <p style="margin:0; font-size:10px; color:rgba(255,255,255,0.55); letter-spacing:0.12em; text-transform:uppercase;">Data as of</p>
            <p style="margin:0; font-size:13px; color:rgba(255,255,255,0.95); font-weight:700;">Depletions: 7/24/26 &middot; Gopuff: 4/25/26 &middot; ReserveBar: 4/25/26</p>
        </div>
    </div>
    <p class="lucci-period">Sales Intelligence Dashboard &middot; Samples / internal accounts excluded from depletions</p>
</div>
""", unsafe_allow_html=True)


# ── HELPERS ──────────────────────────────────────────────────────────────────
def kpi(label, value, sub="", dark=False):
    s = "-dark" if dark else ""
    sub_text = sub if sub else "&nbsp;"
    return f"""
    <div class="kpi-card{s}">
        <span class="kpi-label{s}">{label}</span>
        <span class="kpi-value{s}">{value}</span>
        <span class="kpi-sub{s}">{sub_text}</span>
    </div>"""


def section_title(text):
    st.markdown(f"""
    <div class="section-title">
        <span class="section-bar"></span>
        <span class="section-text">{text}</span>
    </div>""", unsafe_allow_html=True)


CHART_FONT = dict(family=FONT, color=TEXT_DARK, size=12)
CHART_LAYOUT = dict(
    plot_bgcolor=WHITE,
    paper_bgcolor=WHITE,
    font=CHART_FONT,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(showgrid=False, showline=False),
    yaxis=dict(showgrid=True, gridcolor=CREAM_DARK, showline=False),
    showlegend=False,
    height=280,
)


def bar_chart(df, x, y, color=RED, horizontal=False):
    if horizontal:
        fig = px.bar(df, y=x, x=y, orientation="h", color_discrete_sequence=[color])
    else:
        fig = px.bar(df, x=x, y=y, color_discrete_sequence=[color])
    fig.update_layout(**CHART_LAYOUT)
    if horizontal:
        fig.update_layout(
            xaxis=dict(showgrid=True, gridcolor=CREAM_DARK, showline=False),
            yaxis=dict(showgrid=False, showline=False, autorange="reversed"),
        )
    return fig


def grouped_bar(df, x, y1, y2, name1, name2, color1=RED, color2=RED_PALE, horizontal=False):
    fig = go.Figure()
    if horizontal:
        fig.add_trace(go.Bar(y=df[x], x=df[y1], name=name1, marker_color=color1, orientation="h"))
        fig.add_trace(go.Bar(y=df[x], x=df[y2], name=name2, marker_color=color2, orientation="h"))
    else:
        fig.add_trace(go.Bar(x=df[x], y=df[y1], name=name1, marker_color=color1))
        fig.add_trace(go.Bar(x=df[x], y=df[y2], name=name2, marker_color=color2))
    layout = {**CHART_LAYOUT, "barmode": "group", "showlegend": True}
    layout["legend"] = dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=11))
    fig.update_layout(**layout)
    if horizontal:
        fig.update_layout(
            xaxis=dict(showgrid=True, gridcolor=CREAM_DARK, showline=False),
            yaxis=dict(showgrid=False, showline=False, autorange="reversed"),
            height=360,
        )
    return fig


def dual_axis_line(df, x, y1, y2, name1, name2, color1=RED, color2="#8B6347"):
    """Dual-axis line chart: y1 on left axis, y2 on right axis."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[x], y=df[y1], name=name1, mode="lines+markers",
                             line=dict(color=color1, width=2.5), marker=dict(size=7)))
    fig.add_trace(go.Scatter(x=df[x], y=df[y2], name=name2, mode="lines+markers",
                             line=dict(color=color2, width=2.5, dash="dot"),
                             marker=dict(size=7), yaxis="y2"))
    layout = {**CHART_LAYOUT, "showlegend": True}
    layout["legend"] = dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=11))
    layout["yaxis"]  = dict(title=name1, showgrid=True, gridcolor=CREAM_DARK,
                            showline=False, tickfont=dict(size=11))
    layout["yaxis2"] = dict(title=name2, overlaying="y", side="right",
                             showgrid=False, showline=False, tickfont=dict(size=11))
    layout["height"] = 340
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=False, showline=False, tickfont=dict(size=11))
    return fig


def styled_table(df, columns=None, fmt=None):
    """Render a DataFrame as a styled HTML table with alternating row colors.
    fmt: dict of column -> format function for cell values.
    """
    if columns is None:
        columns = df.columns.tolist()
    html = '<table class="styled-table"><thead><tr>'
    for col in columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in columns:
            val = row[col]
            cell = ""
            if fmt and col in fmt:
                cell = fmt[col](val)
            elif isinstance(val, float):
                cell = f"{val:,.2f}"
            else:
                cell = str(val)
            # Color coding for change columns
            css_class = ""
            if "change" in col.lower() or "% " in col.lower() or "growth" in col.lower():
                try:
                    num = float(str(val).replace(",", "").replace("%", "").replace("+", ""))
                    if num > 0:
                        css_class = ' class="positive"'
                    elif num < 0:
                        css_class = ' class="negative"'
                except (ValueError, TypeError):
                    pass
            html += f"<td{css_class}>{cell}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html


def change_fmt(val):
    """Format a numeric change value with +/- sign."""
    if pd.isna(val) or val == "—":
        return "—"
    v = float(val)
    if v > 0:
        return f"+{v:,.2f}"
    elif v < 0:
        return f"{v:,.2f}"
    return "0.00"


def pct_change_fmt(val):
    """Format a percentage change value."""
    if pd.isna(val) or val == "—" or val == float("inf") or val == float("-inf"):
        return "—"
    v = float(val)
    if v > 0:
        return f"+{v:.1f}%"
    elif v < 0:
        return f"{v:.1f}%"
    return "0.0%"


# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

# Source: Ethica Depletions 06.26.26 tab (data through Jun 26, 2026)
# June is now complete. July is partial (10 days).
# TIGHTENED EXCLUSIONS — A POD must represent REAL distribution. Excluded:
#   1) Samples: SAMPLE, F&F Fine Wine, SGWS-HOUSE/SGWS-TEAM, TEAM #, REP # / SALES REP,
#      ETHICA WINES, UNCLASSIFIED ACCOUNT, BERKELEY BOWL - WAREHOUSE, CORPORATE WITHDRAWAL.
#   2) Person-name accounts (Mixed Case + ALL-CAPS "LASTNAME  FIRSTNAME") — DTC samples.
#   3) NON-RETAIL trade channel (Ethica's rep/DTC allocation channel).
#   4) Zero-bottle YTD accounts (cancelled/reversed orders).
# Total excluded: 186 rows / 95.33 cases / 186 PODs.
# PODs are unique distribution points (no double-counting repeat purchases).
# "New PODs" = accounts activated for the FIRST time in a given month.
DEPLETION_AS_OF = "8/28/2026"

grand_monthly = pd.DataFrame([
    {"Month": "Nov", "Cases": 0, "PODs": 0},
    {"Month": "Dec", "Cases": 26.47, "PODs": 27},
    {"Month": "Jan", "Cases": 262.86, "PODs": 202},
    {"Month": "Feb", "Cases": 777.46, "PODs": 392},
    {"Month": "Mar", "Cases": 575.66, "PODs": 566},
    {"Month": "Apr", "Cases": 484.12, "PODs": 365},
    {"Month": "May", "Cases": 669.81, "PODs": 544},
    {"Month": "Jun", "Cases": 710.94, "PODs": 549},
    {"Month": "Jul", "Cases": 741.04, "PODs": 537},
    {"Month": "Aug", "Cases": 476.12, "PODs": 426},
])

combined_monthly = pd.DataFrame([
    {"Month": "Nov", "On-Premise": 0, "Off-Premise": 0},
    {"Month": "Dec", "On-Premise": 16.32, "Off-Premise": 10.15},
    {"Month": "Jan", "On-Premise": 28.32, "Off-Premise": 223.63},
    {"Month": "Feb", "On-Premise": 121.19, "Off-Premise": 491.02},
    {"Month": "Mar", "On-Premise": 164.16, "Off-Premise": 410.92},
    {"Month": "Apr", "On-Premise": 206.79, "Off-Premise": 276.91},
    {"Month": "May", "On-Premise": 259.08, "Off-Premise": 408.48},
    {"Month": "Jun", "On-Premise": 247.41, "Off-Premise": 462.45},
    {"Month": "Jul", "On-Premise": 231.36, "Off-Premise": 508.26},
    {"Month": "Aug", "On-Premise": 160.01, "Off-Premise": 315.19},
])

# Channel breakdown — chronological (oldest → newest)
channel_detail = pd.DataFrame([
    {"Month": "Nov 2025", "Short": "Nov", "Total Depletions": 0, "Total PODs": 0, "On-Premise": 0, "Off-Premise": 0},
    {"Month": "Dec 2025", "Short": "Dec", "Total Depletions": 26.47, "Total PODs": 27, "On-Premise": 16.32, "Off-Premise": 10.15},
    {"Month": "Jan 2026", "Short": "Jan", "Total Depletions": 262.86, "Total PODs": 202, "On-Premise": 28.32, "Off-Premise": 223.63},
    {"Month": "Feb 2026", "Short": "Feb", "Total Depletions": 777.46, "Total PODs": 392, "On-Premise": 121.19, "Off-Premise": 491.02},
    {"Month": "Mar 2026", "Short": "Mar", "Total Depletions": 575.66, "Total PODs": 566, "On-Premise": 164.16, "Off-Premise": 410.92},
    {"Month": "Apr 2026", "Short": "Apr", "Total Depletions": 484.12, "Total PODs": 365, "On-Premise": 206.79, "Off-Premise": 276.91},
    {"Month": "May 2026", "Short": "May", "Total Depletions": 669.81, "Total PODs": 544, "On-Premise": 259.08, "Off-Premise": 408.48},
    {"Month": "Jun 2026", "Short": "Jun", "Total Depletions": 710.94, "Total PODs": 549, "On-Premise": 247.41, "Off-Premise": 462.45},
    {"Month": "Jul 2026", "Short": "Jul", "Total Depletions": 741.04, "Total PODs": 537, "On-Premise": 231.36, "Off-Premise": 508.26},
    {"Month": "Aug 2026 (partial)", "Short": "Aug", "Total Depletions": 476.12, "Total PODs": 426, "On-Premise": 160.01, "Off-Premise": 315.19},
])

# Same-period MTD comparison for partial months.
# For partial Aug (1-28), the comparison is vs Jul 1-28 (NOT full Jul).
# Jul 1-28 actuals (interpolated from 07.24.26 and 07.31.26 snapshots, samples excluded):
#   Total: 602.57 cases / 450 PODs · ON: 197.50 · OFF: 403.90
PRIOR_MTD = {
    "Aug": {"cases": 602.57, "pods": 450, "on": 197.50, "off": 403.90, "ref": "Jul 1-28"},
}

# Compute change vs last month. For partial months, use same-period MTD instead of full prior month.
depl_vals = channel_detail["Total Depletions"].tolist()
pod_vals = channel_detail["Total PODs"].tolist()
short_vals = channel_detail["Short"].tolist()
changes, pct_changes, pod_changes, pod_pct_changes, prior_refs = [], [], [], [], []
for i in range(len(depl_vals)):
    if i > 0:
        short = short_vals[i]
        if short in PRIOR_MTD:
            prev_cases = PRIOR_MTD[short]["cases"]
            prev_pods = PRIOR_MTD[short]["pods"]
            ref_label = PRIOR_MTD[short]["ref"]
        else:
            prev_cases = depl_vals[i - 1]
            prev_pods = pod_vals[i - 1]
            ref_label = "vs full LM"
        chg = depl_vals[i] - prev_cases
        pct = (chg / prev_cases * 100) if prev_cases > 0 else float("inf")
        pchg = pod_vals[i] - prev_pods
        ppct = (pchg / prev_pods * 100) if prev_pods > 0 else float("inf")
        changes.append(chg)
        pct_changes.append(pct)
        pod_changes.append(pchg)
        pod_pct_changes.append(ppct)
        prior_refs.append(ref_label)
    else:
        changes.append(None)
        pct_changes.append(None)
        pod_changes.append(None)
        pod_pct_changes.append(None)
        prior_refs.append("")
channel_detail["Depl Change vs LM"] = changes
channel_detail["% Change vs LM"] = pct_changes
channel_detail["PODs Change vs LM"] = pod_changes
channel_detail["PODs % Change"] = pod_pct_changes
channel_detail["Compare Ref"] = prior_refs

# ON-PREMISE state data (Depletions 08.28.26, tight scrub applied)
on_states = pd.DataFrame([
    {"State": "CA", "YTD Cases": 398.74, "YTD PODs": 159, "Mar Cases": 60.58, "Mar PODs": 35, "Apr Cases": 54.58, "Apr PODs": 35, "May Cases": 89.92, "May PODs": 50, "Jun Cases": 55.83, "Jun PODs": 30, "Jul Cases": 53.58, "Jul PODs": 33, "Aug Cases": 41.08, "Aug PODs": 32, "New Jun PODs": 11, "New Jul PODs": 14, "New Aug PODs": 13},
    {"State": "NY", "YTD Cases": 188.32, "YTD PODs": 48, "Mar Cases": 19.17, "Mar PODs": 12, "Apr Cases": 18.17, "Apr PODs": 10, "May Cases": 32.75, "May PODs": 14, "Jun Cases": 52.08, "Jun PODs": 12, "Jul Cases": 29.00, "Jul PODs": 13, "Aug Cases": 18.08, "Aug PODs": 12, "New Jun PODs": 5, "New Jul PODs": 4, "New Aug PODs": 7},
    {"State": "IL", "YTD Cases": 173.60, "YTD PODs": 126, "Mar Cases": 21.76, "Mar PODs": 26, "Apr Cases": 24.40, "Apr PODs": 9, "May Cases": 20.04, "May PODs": 18, "Jun Cases": 29.03, "Jun PODs": 23, "Jul Cases": 38.97, "Jul PODs": 17, "Aug Cases": 10.39, "Aug PODs": 14, "New Jun PODs": 18, "New Jul PODs": 11, "New Aug PODs": 9},
    {"State": "FL", "YTD Cases": 113.73, "YTD PODs": 60, "Mar Cases": 8.67, "Mar PODs": 12, "Apr Cases": 35.08, "Apr PODs": 11, "May Cases": 10.66, "May PODs": 13, "Jun Cases": 9.50, "Jun PODs": 10, "Jul Cases": 23.16, "Jul PODs": 15, "Aug Cases": 12.08, "Aug PODs": 8, "New Jun PODs": 6, "New Jul PODs": 6, "New Aug PODs": 1},
    {"State": "NJ", "YTD Cases": 110.49, "YTD PODs": 30, "Mar Cases": 9.00, "Mar PODs": 6, "Apr Cases": 6.25, "Apr PODs": 6, "May Cases": 21.66, "May PODs": 13, "Jun Cases": 15.00, "Jun PODs": 7, "Jul Cases": 25.42, "Jul PODs": 15, "Aug Cases": 12.17, "Aug PODs": 7, "New Jun PODs": 1, "New Jul PODs": 5, "New Aug PODs": 1},
    {"State": "TX", "YTD Cases": 88.17, "YTD PODs": 35, "Mar Cases": 12.25, "Mar PODs": 6, "Apr Cases": 18.75, "Apr PODs": 13, "May Cases": 15.17, "May PODs": 13, "Jun Cases": 14.50, "Jun PODs": 12, "Jul Cases": 9.42, "Jul PODs": 8, "Aug Cases": 7.99, "Aug PODs": 9, "New Jun PODs": 1, "New Jul PODs": 2, "New Aug PODs": 3},
    {"State": "NV", "YTD Cases": 62.00, "YTD PODs": 8, "Mar Cases": 6.00, "Mar PODs": 1, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 25.00, "May PODs": 3, "Jun Cases": 17.00, "Jun PODs": 2, "Jul Cases": 4.00, "Jul PODs": 3, "Aug Cases": 10.00, "Aug PODs": 2, "New Jun PODs": 2, "New Jul PODs": 3, "New Aug PODs": 0},
    {"State": "AZ", "YTD Cases": 56.45, "YTD PODs": 52, "Mar Cases": 8.75, "Mar PODs": 9, "Apr Cases": 10.25, "Apr PODs": 7, "May Cases": 0.57, "May PODs": 5, "Jun Cases": 8.58, "Jun PODs": 9, "Jul Cases": 4.16, "Jul PODs": 4, "Aug Cases": 4.08, "Aug PODs": 4, "New Jun PODs": 7, "New Jul PODs": 3, "New Aug PODs": 1},
    {"State": "CO", "YTD Cases": 45.83, "YTD PODs": 16, "Mar Cases": 4.50, "Mar PODs": 2, "Apr Cases": 5.00, "Apr PODs": 3, "May Cases": 11.33, "May PODs": 7, "Jun Cases": 9.00, "Jun PODs": 7, "Jul Cases": 9.50, "Jul PODs": 7, "Aug Cases": 5.50, "Aug PODs": 6, "New Jun PODs": 3, "New Jul PODs": 2, "New Aug PODs": 2},
    {"State": "MA", "YTD Cases": 28.64, "YTD PODs": 24, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 5.08, "Apr PODs": 3, "May Cases": 2.33, "May PODs": 5, "Jun Cases": 12.58, "Jun PODs": 12, "Jul Cases": 1.16, "Jul PODs": 3, "Aug Cases": 7.49, "Aug PODs": 9, "New Jun PODs": 11, "New Jul PODs": 2, "New Aug PODs": 4},
    {"State": "VA", "YTD Cases": 26.66, "YTD PODs": 15, "Mar Cases": 4.08, "Mar PODs": 5, "Apr Cases": 3.00, "Apr PODs": 2, "May Cases": 8.50, "May PODs": 4, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 0, "Jul PODs": 0, "Aug Cases": 10.00, "Aug PODs": 4, "New Jun PODs": 0, "New Jul PODs": 0, "New Aug PODs": 3},
    {"State": "NC", "YTD Cases": 18.33, "YTD PODs": 20, "Mar Cases": 0.33, "Mar PODs": 2, "Apr Cases": 6.33, "Apr PODs": 6, "May Cases": 2.83, "May PODs": 7, "Jun Cases": 1.08, "Jun PODs": 4, "Jul Cases": 4.67, "Jul PODs": 7, "Aug Cases": 3.08, "Aug PODs": 5, "New Jun PODs": 1, "New Jul PODs": 4, "New Aug PODs": 2},
    {"State": "MI", "YTD Cases": 15.75, "YTD PODs": 9, "Mar Cases": 1.00, "Mar PODs": 1, "Apr Cases": 4.58, "Apr PODs": 4, "May Cases": 2.67, "May PODs": 3, "Jun Cases": 5.50, "Jun PODs": 5, "Jul Cases": 2.00, "Jul PODs": 2, "Aug Cases": 0, "Aug PODs": 0, "New Jun PODs": 2, "New Jul PODs": 1, "New Aug PODs": 0},
    {"State": "OH", "YTD Cases": 15.31, "YTD PODs": 18, "Mar Cases": 2.50, "Mar PODs": 4, "Apr Cases": 1.66, "Apr PODs": 6, "May Cases": 0.66, "May PODs": 3, "Jun Cases": 2.41, "Jun PODs": 4, "Jul Cases": 3.16, "Jul PODs": 4, "Aug Cases": 1.25, "Aug PODs": 2, "New Jun PODs": 4, "New Jul PODs": 0, "New Aug PODs": 0},
    {"State": "MD", "YTD Cases": 14.58, "YTD PODs": 9, "Mar Cases": 3.08, "Mar PODs": 3, "Apr Cases": 5.17, "Apr PODs": 3, "May Cases": 1.33, "May PODs": 2, "Jun Cases": 3.08, "Jun PODs": 3, "Jul Cases": 0, "Jul PODs": 0, "Aug Cases": 1.33, "Aug PODs": 2, "New Jun PODs": 1, "New Jul PODs": 0, "New Aug PODs": 0},
    {"State": "KY", "YTD Cases": 12.99, "YTD PODs": 11, "Mar Cases": 1.00, "Mar PODs": 1, "Apr Cases": 3.00, "Apr PODs": 1, "May Cases": 1.08, "May PODs": 2, "Jun Cases": 3.58, "Jun PODs": 6, "Jul Cases": 3.08, "Jul PODs": 3, "Aug Cases": 1.25, "Aug PODs": 2, "New Jun PODs": 4, "New Jul PODs": 2, "New Aug PODs": 1},
    {"State": "WA", "YTD Cases": 11.81, "YTD PODs": 11, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0.32, "Apr PODs": 4, "May Cases": 4.00, "May PODs": 3, "Jun Cases": 3.00, "Jun PODs": 2, "Jul Cases": 1.08, "Jul PODs": 2, "Aug Cases": 3.41, "Aug PODs": 5, "New Jun PODs": 1, "New Jul PODs": 1, "New Aug PODs": 3},
    {"State": "DE", "YTD Cases": 10.08, "YTD PODs": 4, "Mar Cases": 1.00, "Mar PODs": 1, "Apr Cases": 1.00, "Apr PODs": 1, "May Cases": 1.00, "May PODs": 1, "Jun Cases": 1.00, "Jun PODs": 1, "Jul Cases": 5.00, "Jul PODs": 3, "Aug Cases": 1.00, "Aug PODs": 1, "New Jun PODs": 0, "New Jul PODs": 2, "New Aug PODs": 0},
    {"State": "GA", "YTD Cases": 9.75, "YTD PODs": 6, "Mar Cases": 0.25, "Mar PODs": 1, "Apr Cases": 0.50, "Apr PODs": 1, "May Cases": 2.00, "May PODs": 1, "Jun Cases": 1.00, "Jun PODs": 2, "Jul Cases": 3.00, "Jul PODs": 2, "Aug Cases": 3.00, "Aug PODs": 1, "New Jun PODs": 2, "New Jul PODs": 1, "New Aug PODs": 0},
    {"State": "NM", "YTD Cases": 7.92, "YTD PODs": 11, "Mar Cases": 0.16, "Mar PODs": 2, "Apr Cases": 1.17, "Apr PODs": 2, "May Cases": 1.25, "May PODs": 2, "Jun Cases": 1.00, "Jun PODs": 1, "Jul Cases": 1.58, "Jul PODs": 3, "Aug Cases": 2.58, "Aug PODs": 4, "New Jun PODs": 1, "New Jul PODs": 2, "New Aug PODs": 3},
    {"State": "CT", "YTD Cases": 6.00, "YTD PODs": 4, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 2.00, "Apr PODs": 2, "May Cases": 0, "May PODs": 0, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 2.00, "Jul PODs": 2, "Aug Cases": 1.00, "Aug PODs": 1, "New Jun PODs": 0, "New Jul PODs": 1, "New Aug PODs": 0},
    {"State": "DC", "YTD Cases": 5.50, "YTD PODs": 5, "Mar Cases": 0.08, "Mar PODs": 1, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 3.08, "May PODs": 2, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 0, "Jul PODs": 0, "Aug Cases": 1.00, "Aug PODs": 1, "New Jun PODs": 0, "New Jul PODs": 0, "New Aug PODs": 0},
    {"State": "IN", "YTD Cases": 4.82, "YTD PODs": 7, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 1.25, "May PODs": 3, "Jun Cases": 1.41, "Jun PODs": 4, "Jul Cases": 2.17, "Jul PODs": 3, "Aug Cases": 0, "Aug PODs": 0, "New Jun PODs": 3, "New Jul PODs": 1, "New Aug PODs": 0},
    {"State": "MO", "YTD Cases": 4.33, "YTD PODs": 4, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 0, "May PODs": 0, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 3.33, "Jul PODs": 3, "Aug Cases": 1.00, "Aug PODs": 1, "New Jun PODs": 0, "New Jul PODs": 3, "New Aug PODs": 1},
    {"State": "SC", "YTD Cases": 4.08, "YTD PODs": 5, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0.50, "Apr PODs": 1, "May Cases": 0, "May PODs": 0, "Jun Cases": 1.00, "Jun PODs": 1, "Jul Cases": 1.50, "Jul PODs": 2, "Aug Cases": 1.08, "Aug PODs": 2, "New Jun PODs": 1, "New Jul PODs": 2, "New Aug PODs": 1},
    {"State": "ME", "YTD Cases": 0.58, "YTD PODs": 1, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 0, "May PODs": 0, "Jun Cases": 0.25, "Jun PODs": 1, "Jul Cases": 0.17, "Jul PODs": 1, "Aug Cases": 0.17, "Aug PODs": 1, "New Jun PODs": 1, "New Jul PODs": 0, "New Aug PODs": 0},
    {"State": "NE", "YTD Cases": 0.25, "YTD PODs": 1, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 0, "May PODs": 0, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 0.25, "Jul PODs": 1, "Aug Cases": 0, "Aug PODs": 0, "New Jun PODs": 0, "New Jul PODs": 1, "New Aug PODs": 0},
])

# OFF-PREMISE state data (Depletions 08.28.26, tight scrub applied)
off_states = pd.DataFrame([
    {"State": "CA", "YTD Cases": 835.50, "YTD PODs": 264, "Mar Cases": 128.00, "Mar PODs": 98, "Apr Cases": 89.92, "Apr PODs": 48, "May Cases": 82.33, "May PODs": 48, "Jun Cases": 108.34, "Jun PODs": 55, "Jul Cases": 116.24, "Jul PODs": 67, "Aug Cases": 76.17, "Aug PODs": 55, "New Jun PODs": 3, "New Jul PODs": 3, "New Aug PODs": 5},
    {"State": "NJ", "YTD Cases": 349.59, "YTD PODs": 90, "Mar Cases": 20.25, "Mar PODs": 13, "Apr Cases": 17.50, "Apr PODs": 10, "May Cases": 23.08, "May PODs": 20, "Jun Cases": 42.58, "Jun PODs": 30, "Jul Cases": 47.34, "Jul PODs": 26, "Aug Cases": 23.75, "Aug PODs": 18, "New Jun PODs": 13, "New Jul PODs": 2, "New Aug PODs": 1},
    {"State": "NY", "YTD Cases": 342.68, "YTD PODs": 114, "Mar Cases": 22.17, "Mar PODs": 16, "Apr Cases": 28.17, "Apr PODs": 17, "May Cases": 26.17, "May PODs": 17, "Jun Cases": 50.08, "Jun PODs": 34, "Jul Cases": 62.75, "Jul PODs": 37, "Aug Cases": 47.17, "Aug PODs": 28, "New Jun PODs": 21, "New Jul PODs": 20, "New Aug PODs": 8},
    {"State": "FL", "YTD Cases": 307.76, "YTD PODs": 82, "Mar Cases": 17.74, "Mar PODs": 24, "Apr Cases": 26.43, "Apr PODs": 19, "May Cases": 80.99, "May PODs": 32, "Jun Cases": 23.09, "Jun PODs": 22, "Jul Cases": 33.10, "Jul PODs": 28, "Aug Cases": 24.92, "Aug PODs": 20, "New Jun PODs": 1, "New Jul PODs": 5, "New Aug PODs": 3},
    {"State": "IL", "YTD Cases": 277.27, "YTD PODs": 104, "Mar Cases": 46.72, "Mar PODs": 29, "Apr Cases": 24.32, "Apr PODs": 24, "May Cases": 30.00, "May PODs": 27, "Jun Cases": 24.66, "Jun PODs": 22, "Jul Cases": 71.24, "Jul PODs": 36, "Aug Cases": 20.00, "Aug PODs": 18, "New Jun PODs": 5, "New Jul PODs": 6, "New Aug PODs": 2},
    {"State": "NC", "YTD Cases": 209.63, "YTD PODs": 228, "Mar Cases": 34.65, "Mar PODs": 79, "Apr Cases": 8.08, "Apr PODs": 23, "May Cases": 43.41, "May PODs": 76, "Jun Cases": 46.33, "Jun PODs": 91, "Jul Cases": 44.90, "Jul PODs": 68, "Aug Cases": 32.26, "Aug PODs": 54, "New Jun PODs": 62, "New Jul PODs": 21, "New Aug PODs": 16},
    {"State": "TX", "YTD Cases": 129.44, "YTD PODs": 41, "Mar Cases": 19.66, "Mar PODs": 17, "Apr Cases": 11.58, "Apr PODs": 13, "May Cases": 17.67, "May PODs": 20, "Jun Cases": 24.51, "Jun PODs": 20, "Jul Cases": 36.25, "Jul PODs": 21, "Aug Cases": 10.17, "Aug PODs": 9, "New Jun PODs": 0, "New Jul PODs": 1, "New Aug PODs": 1},
    {"State": "VA", "YTD Cases": 107.67, "YTD PODs": 111, "Mar Cases": 43.50, "Mar PODs": 79, "Apr Cases": 5.50, "Apr PODs": 9, "May Cases": 15.34, "May PODs": 25, "Jun Cases": 13.25, "Jun PODs": 23, "Jul Cases": 1.50, "Jul PODs": 3, "Aug Cases": 22.00, "Aug PODs": 32, "New Jun PODs": 11, "New Jul PODs": 3, "New Aug PODs": 11},
    {"State": "MA", "YTD Cases": 90.40, "YTD PODs": 31, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 7.00, "Apr PODs": 6, "May Cases": 19.08, "May PODs": 18, "Jun Cases": 27.08, "Jun PODs": 12, "Jul Cases": 22.08, "Jul PODs": 10, "Aug Cases": 15.16, "Aug PODs": 8, "New Jun PODs": 6, "New Jul PODs": 4, "New Aug PODs": 1},
    {"State": "SC", "YTD Cases": 87.43, "YTD PODs": 76, "Mar Cases": 8.33, "Mar PODs": 18, "Apr Cases": 5.25, "Apr PODs": 6, "May Cases": 25.99, "May PODs": 40, "Jun Cases": 30.45, "Jun PODs": 28, "Jul Cases": 9.43, "Jul PODs": 18, "Aug Cases": 8.01, "Aug PODs": 10, "New Jun PODs": 13, "New Jul PODs": 8, "New Aug PODs": 1},
    {"State": "CT", "YTD Cases": 63.16, "YTD PODs": 37, "Mar Cases": 30.16, "Mar PODs": 17, "Apr Cases": 8.17, "Apr PODs": 8, "May Cases": 6.00, "May PODs": 5, "Jun Cases": 6.75, "Jun PODs": 8, "Jul Cases": 8.42, "Jul PODs": 8, "Aug Cases": 0, "Aug PODs": 0, "New Jun PODs": 6, "New Jul PODs": 1, "New Aug PODs": 0},
    {"State": "MI", "YTD Cases": 47.42, "YTD PODs": 34, "Mar Cases": 6.08, "Mar PODs": 8, "Apr Cases": 21.92, "Apr PODs": 25, "May Cases": 3.50, "May PODs": 5, "Jun Cases": 7.00, "Jun PODs": 8, "Jul Cases": 8.92, "Jul PODs": 10, "Aug Cases": 0, "Aug PODs": 0, "New Jun PODs": 1, "New Jul PODs": 0, "New Aug PODs": 0},
    {"State": "OH", "YTD Cases": 35.76, "YTD PODs": 23, "Mar Cases": 4.58, "Mar PODs": 8, "Apr Cases": 4.25, "Apr PODs": 6, "May Cases": 3.09, "May PODs": 6, "Jun Cases": 6.42, "Jun PODs": 5, "Jul Cases": 4.50, "Jul PODs": 8, "Aug Cases": 1.58, "Aug PODs": 2, "New Jun PODs": 0, "New Jul PODs": 2, "New Aug PODs": 0},
    {"State": "KY", "YTD Cases": 34.00, "YTD PODs": 5, "Mar Cases": 3.00, "Mar PODs": 1, "Apr Cases": 1.00, "Apr PODs": 1, "May Cases": 6.00, "May PODs": 4, "Jun Cases": 17.00, "Jun PODs": 3, "Jul Cases": 6.00, "Jul PODs": 4, "Aug Cases": 1.00, "Aug PODs": 1, "New Jun PODs": 0, "New Jul PODs": 0, "New Aug PODs": 0},
    {"State": "CO", "YTD Cases": 30.00, "YTD PODs": 21, "Mar Cases": 1.00, "Mar PODs": 1, "Apr Cases": 2.25, "Apr PODs": 4, "May Cases": 4.08, "May PODs": 4, "Jun Cases": 5.17, "Jun PODs": 4, "Jul Cases": 9.42, "Jul PODs": 10, "Aug Cases": 6.00, "Aug PODs": 4, "New Jun PODs": 3, "New Jul PODs": 8, "New Aug PODs": 1},
    {"State": "MD", "YTD Cases": 28.91, "YTD PODs": 17, "Mar Cases": 8.00, "Mar PODs": 8, "Apr Cases": 4.00, "Apr PODs": 4, "May Cases": 3.00, "May PODs": 3, "Jun Cases": 1.00, "Jun PODs": 1, "Jul Cases": 4.00, "Jul PODs": 4, "Aug Cases": 3.00, "Aug PODs": 3, "New Jun PODs": 0, "New Jul PODs": 1, "New Aug PODs": 0},
    {"State": "DE", "YTD Cases": 27.00, "YTD PODs": 16, "Mar Cases": 13.00, "Mar PODs": 13, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 1.00, "May PODs": 1, "Jun Cases": 5.00, "Jun PODs": 2, "Jul Cases": 0, "Jul PODs": 0, "Aug Cases": 0, "Aug PODs": 0, "New Jun PODs": 0, "New Jul PODs": 0, "New Aug PODs": 0},
    {"State": "WA", "YTD Cases": 17.50, "YTD PODs": 9, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0.08, "Apr PODs": 1, "May Cases": 6.00, "May PODs": 3, "Jun Cases": 6.17, "Jun PODs": 4, "Jul Cases": 1.00, "Jul PODs": 1, "Aug Cases": 4.25, "Aug PODs": 5, "New Jun PODs": 2, "New Jul PODs": 0, "New Aug PODs": 3},
    {"State": "AZ", "YTD Cases": 17.00, "YTD PODs": 7, "Mar Cases": 1.00, "Mar PODs": 1, "Apr Cases": 0.25, "Apr PODs": 1, "May Cases": 2.00, "May PODs": 2, "Jun Cases": 5.00, "Jun PODs": 2, "Jul Cases": 2.50, "Jul PODs": 3, "Aug Cases": 6.00, "Aug PODs": 4, "New Jun PODs": 0, "New Jul PODs": 1, "New Aug PODs": 1},
    {"State": "GA", "YTD Cases": 15.75, "YTD PODs": 10, "Mar Cases": 3.00, "Mar PODs": 3, "Apr Cases": 7.00, "Apr PODs": 2, "May Cases": 1.25, "May PODs": 2, "Jun Cases": 3.00, "Jun PODs": 2, "Jul Cases": 1.00, "Jul PODs": 1, "Aug Cases": 0, "Aug PODs": 0, "New Jun PODs": 1, "New Jul PODs": 1, "New Aug PODs": 0},
    {"State": "NM", "YTD Cases": 10.24, "YTD PODs": 11, "Mar Cases": 0.08, "Mar PODs": 1, "Apr Cases": 0.24, "Apr PODs": 3, "May Cases": 0.17, "May PODs": 1, "Jun Cases": 3.83, "Jun PODs": 5, "Jul Cases": 4.58, "Jul PODs": 4, "Aug Cases": 1.00, "Aug PODs": 1, "New Jun PODs": 4, "New Jul PODs": 1, "New Aug PODs": 1},
    {"State": "NV", "YTD Cases": 10.00, "YTD PODs": 4, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 2.00, "May PODs": 2, "Jun Cases": 2.00, "Jun PODs": 2, "Jul Cases": 2.00, "Jul PODs": 2, "Aug Cases": 4.00, "Aug PODs": 3, "New Jun PODs": 1, "New Jul PODs": 0, "New Aug PODs": 1},
    {"State": "IN", "YTD Cases": 9.07, "YTD PODs": 9, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 2.33, "May PODs": 4, "Jun Cases": 0.16, "Jun PODs": 2, "Jul Cases": 5.00, "Jul PODs": 2, "Aug Cases": 1.58, "Aug PODs": 5, "New Jun PODs": 1, "New Jul PODs": 0, "New Aug PODs": 4},
    {"State": "DC", "YTD Cases": 9.00, "YTD PODs": 4, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 4.00, "Apr PODs": 3, "May Cases": 2.00, "May PODs": 2, "Jun Cases": 2.00, "Jun PODs": 2, "Jul Cases": 0, "Jul PODs": 0, "Aug Cases": 1.00, "Aug PODs": 1, "New Jun PODs": 0, "New Jul PODs": 0, "New Aug PODs": 0},
    {"State": "MN", "YTD Cases": 7.85, "YTD PODs": 8, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 0, "May PODs": 0, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 4.34, "Jul PODs": 5, "Aug Cases": 3.51, "Aug PODs": 3, "New Jun PODs": 0, "New Jul PODs": 5, "New Aug PODs": 3},
    {"State": "MO", "YTD Cases": 5.25, "YTD PODs": 4, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 1.00, "May PODs": 1, "Jun Cases": 1.00, "Jun PODs": 1, "Jul Cases": 1.00, "Jul PODs": 1, "Aug Cases": 2.25, "Aug PODs": 3, "New Jun PODs": 0, "New Jul PODs": 0, "New Aug PODs": 3},
    {"State": "ME", "YTD Cases": 2.17, "YTD PODs": 1, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 1.00, "May PODs": 1, "Jun Cases": 0.58, "Jun PODs": 1, "Jul Cases": 0.25, "Jul PODs": 1, "Aug Cases": 0.33, "Aug PODs": 1, "New Jun PODs": 0, "New Jul PODs": 0, "New Aug PODs": 0},
    {"State": "NE", "YTD Cases": 0.58, "YTD PODs": 2, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 0, "May PODs": 0, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 0.50, "Jul PODs": 1, "Aug Cases": 0.08, "Aug PODs": 1, "New Jun PODs": 0, "New Jul PODs": 1, "New Aug PODs": 1},
])

# Add change vs last month (Apr vs Mar) to state data
for df in [on_states, off_states]:
    # Apr is now a full month, so we can compare Apr full vs Mar full natively (apples-to-apples).
    df["MoM Chg"] = df["Apr Cases"] - df["Mar Cases"]

# Compute combined state totals
combined_states = pd.merge(
    on_states[["State", "YTD Cases", "YTD PODs"]].rename(columns={"YTD Cases": "On Cases", "YTD PODs": "On PODs"}),
    off_states[["State", "YTD Cases", "YTD PODs"]].rename(columns={"YTD Cases": "Off Cases", "YTD PODs": "Off PODs"}),
    on="State", how="outer",
).fillna(0)
combined_states["Total Cases"] = combined_states["On Cases"] + combined_states["Off Cases"]
combined_states["Total PODs"] = combined_states["On PODs"] + combined_states["Off PODs"]
combined_states = combined_states.sort_values("Total Cases", ascending=False).reset_index(drop=True)
top3_states = combined_states.head(3)

# ── GOPUFF DATA (from Gopuff Lucci 4.25.26 file; latest weekly bucket = week ending 4/13) ──
GOPUFF_AS_OF = "4/25/2026"
GOPUFF_LATEST_WEEK = "4/13/2026"

gopuff_monthly = pd.DataFrame([
    {"Month": "Jan", "Units": 11},
    {"Month": "Feb", "Units": 70},
    {"Month": "Mar", "Units": 67},
    {"Month": "Apr", "Units": 21},
])

gopuff_states = pd.DataFrame([
    {"State": "NY", "Units": 120, "Pct": 71.0, "Locations": 6},
    {"State": "CA", "Units": 31, "Pct": 18.3, "Locations": 18},
    {"State": "FL", "Units": 18, "Pct": 10.7, "Locations": 5},
])

gopuff_top_locations = pd.DataFrame([
    {"Location": "JFK New York 880", "State": "NY", "YTD": 44},
    {"Location": "JFK Brooklyn 554", "State": "NY", "YTD": 33},
    {"Location": "JFK New York 975", "State": "NY", "YTD": 24},
    {"Location": "JFK New York 807", "State": "NY", "YTD": 12},
    {"Location": "BUR Pasadena 416", "State": "CA", "YTD": 9},
    {"Location": "MIA Miami 183", "State": "FL", "YTD": 8},
    {"Location": "JFK Brooklyn 629", "State": "NY", "YTD": 6},
    {"Location": "MIA Miami Beach 911", "State": "FL", "YTD": 4},
    {"Location": "SAN Point Loma 446", "State": "CA", "YTD": 3},
    {"Location": "SFO San Mateo 496", "State": "CA", "YTD": 3},
    {"Location": "MIA Miami 330", "State": "FL", "YTD": 3},
])

gopuff_location_detail = pd.DataFrame([
    {"Rank": 1, "Location": "JFK_New-York_880", "ST": "NY", "Jan": 0, "Feb": 11, "Mar": 17, "Apr": 16, "YTD": 44},
    {"Rank": 2, "Location": "JFK_Brooklyn_554", "ST": "NY", "Jan": 4, "Feb": 10, "Mar": 14, "Apr": 5, "YTD": 33},
    {"Rank": 3, "Location": "JFK_New-York_975", "ST": "NY", "Jan": 4, "Feb": 9, "Mar": 11, "Apr": 0, "YTD": 24},
    {"Rank": 4, "Location": "JFK_New-York_807", "ST": "NY", "Jan": 0, "Feb": 3, "Mar": 5, "Apr": 4, "YTD": 12},
    {"Rank": 5, "Location": "BUR_Pasadena_416", "ST": "CA", "Jan": 0, "Feb": 9, "Mar": 0, "Apr": 0, "YTD": 9},
    {"Rank": 6, "Location": "MIA_Miami_183", "ST": "FL", "Jan": 0, "Feb": 4, "Mar": 1, "Apr": 3, "YTD": 8},
    {"Rank": 7, "Location": "JFK_Brooklyn_629", "ST": "NY", "Jan": 2, "Feb": 4, "Mar": 0, "Apr": 0, "YTD": 6},
    {"Rank": 8, "Location": "MIA_Miami-Beach_911", "ST": "FL", "Jan": 0, "Feb": 3, "Mar": 1, "Apr": 0, "YTD": 4},
    {"Rank": 9, "Location": "SAN_Point-Loma_446", "ST": "CA", "Jan": 0, "Feb": 3, "Mar": 0, "Apr": 0, "YTD": 3},
    {"Rank": 10, "Location": "SFO_San-Mateo_496", "ST": "CA", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "YTD": 3},
    {"Rank": 11, "Location": "MIA_Miami_330", "ST": "FL", "Jan": 0, "Feb": 2, "Mar": 1, "Apr": 0, "YTD": 3},
    {"Rank": 12, "Location": "OAK_Danville_487", "ST": "CA", "Jan": 0, "Feb": 2, "Mar": 0, "Apr": 0, "YTD": 2},
    {"Rank": 13, "Location": "SAN_La-Mesa_404", "ST": "CA", "Jan": 0, "Feb": 0, "Mar": 2, "Apr": 0, "YTD": 2},
    {"Rank": 14, "Location": "MIA_Miami_376", "ST": "FL", "Jan": 1, "Feb": 0, "Mar": 0, "Apr": 0, "YTD": 1},
    {"Rank": 15, "Location": "SFO_San-Francisco_434", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "Apr": 0, "YTD": 1},
    {"Rank": 16, "Location": "OAK_San-Leandro_497", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "Apr": 0, "YTD": 1},
    {"Rank": 17, "Location": "SFO_Colma_405", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "Apr": 0, "YTD": 1},
    {"Rank": 18, "Location": "LAX_Santa-Monica_427", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "Apr": 0, "YTD": 1},
    {"Rank": 19, "Location": "SMF_Sacramento_445", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "Apr": 0, "YTD": 1},
    {"Rank": 20, "Location": "SJC_San-Jose_459", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "Apr": 0, "YTD": 1},
    {"Rank": 21, "Location": "LAX_Torrance_462", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "Apr": 0, "YTD": 1},
    {"Rank": 22, "Location": "RDD_Redding_777", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "Apr": 0, "YTD": 1},
    {"Rank": 23, "Location": "SJC_Los-Altos_1019", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "Apr": 0, "YTD": 1},
    {"Rank": 24, "Location": "SAN_La-Jolla_1016", "ST": "CA", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 0, "YTD": 1},
    {"Rank": 25, "Location": "OAK_Oakland_403", "ST": "CA", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 0, "YTD": 1},
    {"Rank": 26, "Location": "LAX_Culver-City_423", "ST": "CA", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 0, "YTD": 1},
    {"Rank": 27, "Location": "BUR_Glendale_495", "ST": "CA", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 0, "YTD": 1},
    {"Rank": 28, "Location": "MIA_Miami_602", "ST": "FL", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 0, "YTD": 1},
    {"Rank": 29, "Location": "JFK_New-York_839", "ST": "NY", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 0, "YTD": 1},
])

# ── RESERVEBAR DATA ──────────────────────────────────────────────────────────
rb_order_range = pd.DataFrame([
    {"Range": "<$100", "Pct": 66.7}, {"Range": "$100-200", "Pct": 22.2},
    {"Range": "$200-500", "Pct": 7.4}, {"Range": "$500-1K", "Pct": 3.7},
    {"Range": "$1K-2K", "Pct": 0}, {"Range": ">$2K", "Pct": 0},
])

rb_dow = pd.DataFrame([
    {"Day": "Mon", "Pct": 11.1}, {"Day": "Tue", "Pct": 11.1},
    {"Day": "Wed", "Pct": 14.8}, {"Day": "Thu", "Pct": 22.2},
    {"Day": "Fri", "Pct": 22.2}, {"Day": "Sat", "Pct": 14.8},
    {"Day": "Sun", "Pct": 3.7},
])

rb_discounts = pd.DataFrame([
    {"Code": "shiplucci", "Orders": 8, "Share": "57%"},
    {"Code": "lastminlove", "Orders": 2, "Share": "14%"},
    {"Code": "cheers10", "Orders": 1, "Share": "7%"},
    {"Code": "reservebar10", "Orders": 1, "Share": "7%"},
    {"Code": "feb26 codes", "Orders": 1, "Share": "7%"},
    {"Code": "welcome10off", "Orders": 1, "Share": "7%"},
])

rb_monthly = pd.DataFrame([
    {"Month": "Feb '26", "Units": 62},
    {"Month": "Mar '26", "Units": 21},
    {"Month": "Apr '26", "Units": 3},
])

rb_bottles = pd.DataFrame([
    {"Bottles": "2", "Pct": 40.7},
    {"Bottles": "1", "Pct": 22.2},
    {"Bottles": "10+", "Pct": 7.4},
    {"Bottles": "3", "Pct": 7.4},
    {"Bottles": "4", "Pct": 7.4},
    {"Bottles": "7", "Pct": 7.4},
    {"Bottles": "5", "Pct": 3.7},
    {"Bottles": "6", "Pct": 3.7},
])

# ── SHIPMENTS DATA (from Payment Process Excel) ─────────────────────────────
# Revenue/credit memo data removed from dashboard per request.
ship_monthly_cases = pd.DataFrame([
    {"Month": "Dec '25", "Cases": 2302},
    {"Month": "Jan '26", "Cases": 1447},
    {"Month": "Feb '26", "Cases": 683},
    {"Month": "Mar '26", "Cases": 379},
    {"Month": "Apr '26", "Cases": 310},
    {"Month": "May '26", "Cases": 490},
])

# Top accounts — chain data from Ethica 05.11.26 (samples removed)
top_accounts = pd.DataFrame([
    {"Account": "Total Wine & More", "Premise": "Off", "States": "Multi", "YTD Cases": 477.86, "YTD PODs": 134, "Mar Cases": 36.16, "Apr Cases": 36.01, "May Cases": 85.99, "Jun Cases": 128.10, "Jul Cases": 93.77, "Aug Cases": 62.67},
    {"Account": "Eataly", "Premise": "On", "States": "CA, FL, IL, MA, NJ, NY, TX", "YTD Cases": 318.08, "YTD PODs": 14, "Mar Cases": 50.00, "Apr Cases": 46.08, "May Cases": 60.00, "Jun Cases": 48.00, "Jul Cases": 65.00, "Aug Cases": 23.00},
    {"Account": "BevMo!", "Premise": "Off", "States": "CA", "YTD Cases": 297.00, "YTD PODs": 145, "Mar Cases": 50.00, "Apr Cases": 9.00, "May Cases": 18.00, "Jun Cases": 36.00, "Jul Cases": 54.00, "Aug Cases": 29.00},
    {"Account": "Food Lion", "Premise": "Off", "States": "NC, SC, VA", "YTD Cases": 222.56, "YTD PODs": 345, "Mar Cases": 75.98, "Apr Cases": 6.83, "May Cases": 45.66, "Jun Cases": 48.53, "Jul Cases": 23.16, "Aug Cases": 22.43},
    {"Account": "Binny's", "Premise": "Off", "States": "IL", "YTD Cases": 174.99, "YTD PODs": 45, "Mar Cases": 8.40, "Apr Cases": 14.24, "May Cases": 29.00, "Jun Cases": 17.00, "Jul Cases": 56.08, "Aug Cases": 16.00},
    {"Account": "Wine.com", "Premise": "Off", "States": "CA, MA, NJ, NY, OH, TX", "YTD Cases": 115.00, "YTD PODs": 7, "Mar Cases": 4.00, "Apr Cases": 15.00, "May Cases": 8.00, "Jun Cases": 19.00, "Jul Cases": 20.00, "Aug Cases": 19.00},
    {"Account": "Albertsons Warehouse", "Premise": "Off", "States": "CA", "YTD Cases": 111.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 22.00, "May Cases": 11.00, "Jun Cases": 11.00, "Jul Cases": 11.00, "Aug Cases": 11.00},
    {"Account": "Trader Joe's", "Premise": "Off", "States": "KY, NC, SC", "YTD Cases": 99.00, "YTD PODs": 15, "Mar Cases": 0, "Apr Cases": 2.00, "May Cases": 23.00, "Jun Cases": 29.00, "Jul Cases": 25.00, "Aug Cases": 20.00},
    {"Account": "Gary's Wine", "Premise": "Off", "States": "NJ", "YTD Cases": 77.00, "YTD PODs": 3, "Mar Cases": 1.00, "Apr Cases": 1.00, "May Cases": 1.00, "Jun Cases": 1.00, "Jul Cases": 0, "Aug Cases": 1.00},
    {"Account": "Milam's Markets", "Premise": "Off", "States": "FL", "YTD Cases": 72.00, "YTD PODs": 6, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"Account": "Trader Joe's Warehouse", "Premise": "Off", "States": "FL", "YTD Cases": 56.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 56.00, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"Account": "Stew Leonard's Wines", "Premise": "Off", "States": "CT, NY", "YTD Cases": 55.00, "YTD PODs": 5, "Mar Cases": 17.00, "Apr Cases": 2.00, "May Cases": 1.00, "Jun Cases": 1.00, "Jul Cases": 3.00, "Aug Cases": 1.00},
    {"Account": "Stew Leonard's", "Premise": "Off", "States": "NJ", "YTD Cases": 42.00, "YTD PODs": 2, "Mar Cases": 2.00, "Apr Cases": 4.00, "May Cases": 1.00, "Jun Cases": 3.00, "Jul Cases": 2.00, "Aug Cases": 3.00},
    {"Account": "H-E-B Central Market", "Premise": "Off", "States": "TX", "YTD Cases": 23.42, "YTD PODs": 6, "Mar Cases": 1.00, "Apr Cases": 2.25, "May Cases": 4.00, "Jun Cases": 2.00, "Jul Cases": 8.00, "Aug Cases": 6.00},
    {"Account": "Trader Joe's Liquor", "Premise": "Off", "States": "KY", "YTD Cases": 23.00, "YTD PODs": 2, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 4.00, "Jun Cases": 16.00, "Jul Cases": 2.00, "Aug Cases": 1.00},
    {"Account": "VIN Chicago", "Premise": "Off", "States": "IL", "YTD Cases": 20.16, "YTD PODs": 2, "Mar Cases": 20.00, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"Account": "Bottle King", "Premise": "Off", "States": "NJ", "YTD Cases": 20.00, "YTD PODs": 12, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 12.00, "Jul Cases": 7.00, "Aug Cases": 1.00},
    {"Account": "BevMax", "Premise": "Off", "States": "CT", "YTD Cases": 17.00, "YTD PODs": 11, "Mar Cases": 8.00, "Apr Cases": 3.00, "May Cases": 1.00, "Jun Cases": 2.00, "Jul Cases": 2.00, "Aug Cases": 0},
    {"Account": "Spec's Wine & Spirits", "Premise": "Off", "States": "TX", "YTD Cases": 14.08, "YTD PODs": 8, "Mar Cases": 7.00, "Apr Cases": 2.08, "May Cases": 0, "Jun Cases": 3.00, "Jul Cases": 1.00, "Aug Cases": 1.00},
    {"Account": "ShopRite Liquors", "Premise": "Off", "States": "NJ", "YTD Cases": 14.00, "YTD PODs": 6, "Mar Cases": 5.00, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 1.00},
    {"Account": "Oliver's Market", "Premise": "Off", "States": "CA", "YTD Cases": 13.00, "YTD PODs": 4, "Mar Cases": 11.00, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 0},
    {"Account": "Harris Teeter", "Premise": "Off", "States": "FL, NC, SC", "YTD Cases": 12.10, "YTD PODs": 18, "Mar Cases": 0, "Apr Cases": 0.25, "May Cases": 0.50, "Jun Cases": 3.33, "Jul Cases": 4.01, "Aug Cases": 4.01},
    {"Account": "Eataly", "Premise": "Off", "States": "MA", "YTD Cases": 12.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 2.00, "Jun Cases": 5.00, "Jul Cases": 2.00, "Aug Cases": 3.00},
    {"Account": "Gopuff", "Premise": "Off", "States": "FL", "YTD Cases": 12.00, "YTD PODs": 6, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 1.00, "Jul Cases": 2.00, "Aug Cases": 2.00},
    {"Account": "Spec's Wholesale", "Premise": "Off", "States": "TX", "YTD Cases": 11.17, "YTD PODs": 2, "Mar Cases": 3.00, "Apr Cases": 2.00, "May Cases": 1.00, "Jun Cases": 2.00, "Jul Cases": 1.00, "Aug Cases": 2.00},
])

# State-level top accounts for key 6 states (CA, TX, FL, NY, NJ, IL) — as of 7/31/26 (samples removed)
state_top_accounts = pd.DataFrame([
    # CA
    {"State": "CA", "Account": "BevMo!", "Premise": "Off", "YTD Cases": 297.00, "YTD PODs": 145, "Mar Cases": 50.00, "Apr Cases": 9.00, "May Cases": 18.00, "Jun Cases": 36.00, "Jul Cases": 54.00, "Aug Cases": 29.00},
    {"State": "CA", "Account": "Albertsons Warehouse", "Premise": "Off", "YTD Cases": 111.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 22.00, "May Cases": 11.00, "Jun Cases": 11.00, "Jul Cases": 11.00, "Aug Cases": 11.00},
    {"State": "CA", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 75.08, "YTD PODs": 15, "Mar Cases": 1.00, "Apr Cases": 5.00, "May Cases": 11.00, "Jun Cases": 35.08, "Jul Cases": 6.00, "Aug Cases": 7.00},
    {"State": "CA", "Account": "Eataly", "Premise": "On", "YTD Cases": 59.00, "YTD PODs": 2, "Mar Cases": 13.00, "Apr Cases": 4.00, "May Cases": 14.00, "Jun Cases": 9.00, "Jul Cases": 8.00, "Aug Cases": 6.00},
    {"State": "CA", "Account": "Wine.com", "Premise": "Off", "YTD Cases": 25.00, "YTD PODs": 2, "Mar Cases": 0, "Apr Cases": 5.00, "May Cases": 2.00, "Jun Cases": 4.00, "Jul Cases": 4.00, "Aug Cases": 3.00},
    {"State": "CA", "Account": "Oliver's Market", "Premise": "Off", "YTD Cases": 13.00, "YTD PODs": 4, "Mar Cases": 11.00, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 0},
    {"State": "CA", "Account": "Buona Forchetta", "Premise": "On", "YTD Cases": 11.00, "YTD PODs": 4, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 9.00, "Jun Cases": 0, "Jul Cases": 2.00, "Aug Cases": 0},
    {"State": "CA", "Account": "Sodexo Live!", "Premise": "On", "YTD Cases": 8.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 3.00, "Jun Cases": 0, "Jul Cases": 3.00, "Aug Cases": 2.00},
    {"State": "CA", "Account": "ClubProcure", "Premise": "On", "YTD Cases": 3.25, "YTD PODs": 3, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 2.00, "Jul Cases": 0, "Aug Cases": 0.25},
    {"State": "CA", "Account": "Invited", "Premise": "On", "YTD Cases": 3.00, "YTD PODs": 1, "Mar Cases": 2.00, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "CA", "Account": "Troon Golf", "Premise": "On", "YTD Cases": 3.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 2.00, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "CA", "Account": "Waldorf Collection", "Premise": "On", "YTD Cases": 2.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 2.00, "Aug Cases": 0},
    {"State": "CA", "Account": "Auberge Resorts Collection", "Premise": "On", "YTD Cases": 1.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 1.00, "Jul Cases": 0, "Aug Cases": 0},
    # TX
    {"State": "TX", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 57.60, "YTD PODs": 17, "Mar Cases": 4.58, "Apr Cases": 1.08, "May Cases": 10.67, "Jun Cases": 14.51, "Jul Cases": 25.17, "Aug Cases": 0.17},
    {"State": "TX", "Account": "Eataly", "Premise": "On", "YTD Cases": 28.00, "YTD PODs": 2, "Mar Cases": 4.00, "Apr Cases": 7.00, "May Cases": 5.00, "Jun Cases": 4.00, "Jul Cases": 6.00, "Aug Cases": 2.00},
    {"State": "TX", "Account": "H-E-B Central Market", "Premise": "Off", "YTD Cases": 23.42, "YTD PODs": 6, "Mar Cases": 1.00, "Apr Cases": 2.25, "May Cases": 4.00, "Jun Cases": 2.00, "Jul Cases": 8.00, "Aug Cases": 6.00},
    {"State": "TX", "Account": "Spec's Wine & Spirits", "Premise": "Off", "YTD Cases": 14.08, "YTD PODs": 8, "Mar Cases": 7.00, "Apr Cases": 2.08, "May Cases": 0, "Jun Cases": 3.00, "Jul Cases": 1.00, "Aug Cases": 1.00},
    {"State": "TX", "Account": "Wine.com", "Premise": "Off", "YTD Cases": 13.00, "YTD PODs": 1, "Mar Cases": 1.00, "Apr Cases": 3.00, "May Cases": 2.00, "Jun Cases": 2.00, "Jul Cases": 0, "Aug Cases": 1.00},
    {"State": "TX", "Account": "Spec's Wholesale", "Premise": "Off", "YTD Cases": 11.17, "YTD PODs": 2, "Mar Cases": 3.00, "Apr Cases": 2.00, "May Cases": 1.00, "Jun Cases": 2.00, "Jul Cases": 1.00, "Aug Cases": 2.00},
    {"State": "TX", "Account": "Miraval", "Premise": "On", "YTD Cases": 4.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 2.00, "May Cases": 0, "Jun Cases": 2.00, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "TX", "Account": "Royal Blue Grocery", "Premise": "On", "YTD Cases": 1.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 1.00, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "TX", "Account": "Aloft Hotels", "Premise": "On", "YTD Cases": 0.17, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0.08, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0.08, "Aug Cases": 0},
    # FL
    {"State": "FL", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 85.68, "YTD PODs": 31, "Mar Cases": 9.33, "Apr Cases": 4.76, "May Cases": 16.41, "Jun Cases": 18.59, "Jul Cases": 16.51, "Aug Cases": 12.50},
    {"State": "FL", "Account": "Milam's Markets", "Premise": "Off", "YTD Cases": 72.00, "YTD PODs": 6, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "FL", "Account": "Trader Joe's Warehouse", "Premise": "Off", "YTD Cases": 56.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 56.00, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "FL", "Account": "Eataly", "Premise": "On", "YTD Cases": 13.08, "YTD PODs": 3, "Mar Cases": 3.00, "Apr Cases": 0.08, "May Cases": 2.00, "Jun Cases": 2.00, "Jul Cases": 3.00, "Aug Cases": 3.00},
    {"State": "FL", "Account": "Gopuff", "Premise": "Off", "YTD Cases": 12.00, "YTD PODs": 6, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 1.00, "Jul Cases": 2.00, "Aug Cases": 2.00},
    {"State": "FL", "Account": "Amex Centurion Lounge", "Premise": "On", "YTD Cases": 8.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 6.00, "Aug Cases": 2.00},
    {"State": "FL", "Account": "Shores", "Premise": "Off", "YTD Cases": 4.00, "YTD PODs": 4, "Mar Cases": 0, "Apr Cases": 4.00, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "FL", "Account": "Doris Italian Market", "Premise": "Off", "YTD Cases": 3.17, "YTD PODs": 1, "Mar Cases": 1.00, "Apr Cases": 1.00, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0.17, "Aug Cases": 1.00},
    {"State": "FL", "Account": "Soho House", "Premise": "On", "YTD Cases": 1.83, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "FL", "Account": "Bice Ristorante", "Premise": "On", "YTD Cases": 1.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 0},
    {"State": "FL", "Account": "Harris Teeter", "Premise": "Off", "YTD Cases": 0.42, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0.42},
    {"State": "FL", "Account": "ABC Fine Wine & Spirits", "Premise": "Off", "YTD Cases": 0.17, "YTD PODs": 1, "Mar Cases": 0.17, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    # NY
    {"State": "NY", "Account": "Eataly", "Premise": "On", "YTD Cases": 70.00, "YTD PODs": 4, "Mar Cases": 11.00, "Apr Cases": 9.00, "May Cases": 19.00, "Jun Cases": 10.00, "Jul Cases": 19.00, "Aug Cases": 2.00},
    {"State": "NY", "Account": "Wine.com", "Premise": "Off", "YTD Cases": 50.00, "YTD PODs": 1, "Mar Cases": 1.00, "Apr Cases": 5.00, "May Cases": 3.00, "Jun Cases": 5.00, "Jul Cases": 13.00, "Aug Cases": 10.00},
    {"State": "NY", "Account": "Stew Leonard's Wines", "Premise": "Off", "YTD Cases": 32.00, "YTD PODs": 2, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 1.00},
    {"State": "NY", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 19.00, "YTD PODs": 1, "Mar Cases": 2.00, "Apr Cases": 3.00, "May Cases": 2.00, "Jun Cases": 4.00, "Jul Cases": 5.00, "Aug Cases": 2.00},
    {"State": "NY", "Account": "Moxy Hotels", "Premise": "On", "YTD Cases": 11.00, "YTD PODs": 2, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 11.00, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "NY", "Account": "Hilton", "Premise": "On", "YTD Cases": 2.00, "YTD PODs": 2, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 1.00},
    {"State": "NY", "Account": "ClubProcure", "Premise": "On", "YTD Cases": 1.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 0},
    # NJ
    {"State": "NJ", "Account": "Gary's Wine & Marketplace", "Premise": "Off", "YTD Cases": 77.00, "YTD PODs": 3, "Mar Cases": 1.00, "Apr Cases": 1.00, "May Cases": 1.00, "Jun Cases": 1.00, "Jul Cases": 0, "Aug Cases": 1.00},
    {"State": "NJ", "Account": "Stew Leonard's", "Premise": "Off", "YTD Cases": 42.00, "YTD PODs": 2, "Mar Cases": 2.00, "Apr Cases": 4.00, "May Cases": 1.00, "Jun Cases": 3.00, "Jul Cases": 2.00, "Aug Cases": 3.00},
    {"State": "NJ", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 37.00, "YTD PODs": 7, "Mar Cases": 5.00, "Apr Cases": 2.00, "May Cases": 8.00, "Jun Cases": 7.00, "Jul Cases": 8.00, "Aug Cases": 2.00},
    {"State": "NJ", "Account": "Eataly", "Premise": "On", "YTD Cases": 28.00, "YTD PODs": 1, "Mar Cases": 4.00, "Apr Cases": 2.00, "May Cases": 4.00, "Jun Cases": 4.00, "Jul Cases": 6.00, "Aug Cases": 4.00},
    {"State": "NJ", "Account": "Bottle King", "Premise": "Off", "YTD Cases": 20.00, "YTD PODs": 12, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 12.00, "Jul Cases": 7.00, "Aug Cases": 1.00},
    {"State": "NJ", "Account": "Wine.com", "Premise": "Off", "YTD Cases": 16.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 5.00, "Jul Cases": 2.00, "Aug Cases": 5.00},
    {"State": "NJ", "Account": "ShopRite Liquors", "Premise": "Off", "YTD Cases": 14.00, "YTD PODs": 6, "Mar Cases": 5.00, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 1.00},
    {"State": "NJ", "Account": "ShopRite Wines & Spirits", "Premise": "Off", "YTD Cases": 8.00, "YTD PODs": 4, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 3.00, "Jun Cases": 1.00, "Jul Cases": 0, "Aug Cases": 1.00},
    {"State": "NJ", "Account": "Canal's Liquor", "Premise": "Off", "YTD Cases": 4.00, "YTD PODs": 2, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 0},
    {"State": "NJ", "Account": "Bourbon Street Wine & Spirits", "Premise": "Off", "YTD Cases": 3.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 1.00, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 1.00},
    {"State": "NJ", "Account": "Joe Canals Discount Liquor", "Premise": "Off", "YTD Cases": 2.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 0},
    {"State": "NJ", "Account": "ShopRite", "Premise": "Off", "YTD Cases": 2.00, "YTD PODs": 2, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "NJ", "Account": "B2 Bistro And Bar", "Premise": "On", "YTD Cases": 1.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    # IL
    {"State": "IL", "Account": "Binny's Beverage Depot", "Premise": "Off", "YTD Cases": 174.99, "YTD PODs": 45, "Mar Cases": 8.40, "Apr Cases": 14.24, "May Cases": 29.00, "Jun Cases": 17.00, "Jul Cases": 56.08, "Aug Cases": 16.00},
    {"State": "IL", "Account": "Eataly (Brew Pub, Chicago)", "Premise": "On", "YTD Cases": 108.00, "YTD PODs": 1, "Mar Cases": 15.00, "Apr Cases": 20.00, "May Cases": 15.00, "Jun Cases": 14.00, "Jul Cases": 23.00, "Aug Cases": 4.00},
    {"State": "IL", "Account": "VIN Chicago", "Premise": "Off", "YTD Cases": 20.16, "YTD PODs": 2, "Mar Cases": 20.00, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "IL", "Account": "Midtown Athletic Club", "Premise": "On", "YTD Cases": 4.33, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 4.33, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "IL", "Account": "Heinen's", "Premise": "Off", "YTD Cases": 3.00, "YTD PODs": 1, "Mar Cases": 1.00, "Apr Cases": 1.00, "May Cases": 0, "Jun Cases": 1.00, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "IL", "Account": "Go Grocer", "Premise": "On", "YTD Cases": 2.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "IL", "Account": "ClubProcure", "Premise": "On", "YTD Cases": 1.49, "YTD PODs": 6, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0.32, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "IL", "Account": "South Loop Market", "Premise": "Off", "YTD Cases": 1.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 1.00, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "IL", "Account": "Garfield's Beverage Warehouse", "Premise": "Off", "YTD Cases": 1.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "IL", "Account": "Foxtrot", "Premise": "Off", "YTD Cases": 0.41, "YTD PODs": 4, "Mar Cases": 0.24, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0},
    {"State": "IL", "Account": "Armanetti Beverage Mart", "Premise": "Off", "YTD Cases": 0.25, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0.25, "Jul Cases": 0, "Aug Cases": 0},
])

# Top 15 Restaurants/Bars (clean — samples removed) from 08.28.26 tab
top_restaurants_bars = pd.DataFrame([
    {"Rank": 1, "Restaurant": "Eataly (brew Pub)", "City": "Chicago", "State": "IL", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 108.00, "Mar": 15.00, "Apr": 20.00, "May": 15.00, "Jun": 14.00, "Jul": 23.00, "Aug": 4.00},
    {"Rank": 2, "Restaurant": "Eataly Vino NYC Eataly Vino", "City": "New York", "State": "NY", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 35.00, "Mar": 2.00, "Apr": 3.00, "May": 9.00, "Jun": 10.00, "Jul": 10.00, "Aug": 1.00},
    {"Rank": 3, "Restaurant": "Eataly", "City": "Santa Clara", "State": "CA", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 32.00, "Mar": 10.00, "Apr": 0, "May": 9.00, "Jun": 3.00, "Jul": 4.00, "Aug": 1.00},
    {"Rank": 4, "Restaurant": "Eataly", "City": "Los Angeles", "State": "CA", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 27.00, "Mar": 3.00, "Apr": 4.00, "May": 5.00, "Jun": 6.00, "Jul": 4.00, "Aug": 5.00},
    {"Rank": 5, "Restaurant": "Eataly (shop)", "City": "Dallas", "State": "TX", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 18.00, "Mar": 0, "Apr": 6.00, "May": 3.00, "Jun": 3.00, "Jul": 5.00, "Aug": 1.00},
    {"Rank": 6, "Restaurant": "Eataly", "City": "New York", "State": "NY", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 16.00, "Mar": 5.00, "Apr": 0, "May": 5.00, "Jun": 0, "Jul": 6.00, "Aug": 0},
    {"Rank": 7, "Restaurant": "Vesta", "City": "Redwood City", "State": "CA", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 15.00, "Mar": 0, "Apr": 0, "May": 4.00, "Jun": 3.00, "Jul": 8.00, "Aug": 0},
    {"Rank": 8, "Restaurant": "Alta Calidad", "City": "Brooklyn", "State": "NY", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 14.00, "Mar": 0, "Apr": 0, "May": 0, "Jun": 3.00, "Jul": 2.00, "Aug": 3.00},
    {"Rank": 9, "Restaurant": "Fino All Is Well Good As Gold", "City": "Denver", "State": "CO", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 13.50, "Mar": 3.50, "Apr": 3.00, "May": 2.00, "Jun": 2.00, "Jul": 1.00, "Aug": 2.00},
    {"Rank": 10, "Restaurant": "Eataly NYC Flatiron", "City": "New York", "State": "NY", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 13.00, "Mar": 3.00, "Apr": 4.00, "May": 3.00, "Jun": 0, "Jul": 3.00, "Aug": 0},
    {"Rank": 11, "Restaurant": "Enoteca LA Storia", "City": "Los Gatos", "State": "CA", "Chain": "(independent)", "Channel": "Bar/Tavern", "YTD Cases": 13.00, "Mar": 0, "Apr": 4.00, "May": 0, "Jun": 4.00, "Jul": 2.00, "Aug": 3.00},
    {"Rank": 12, "Restaurant": "Marvito", "City": "West Hollywood", "State": "CA", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 13.00, "Mar": 5.00, "Apr": 5.00, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0},
    {"Rank": 13, "Restaurant": "Pizzeria Portofino", "City": "Chicago", "State": "IL", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 12.00, "Mar": 0, "Apr": 0, "May": 1.00, "Jun": 4.00, "Jul": 4.00, "Aug": 3.00},
    {"Rank": 14, "Restaurant": "Eataly - 1st Flr", "City": "Boston", "State": "MA", "Chain": "EATALY", "Channel": "Bar/Tavern", "YTD Cases": 12.00, "Mar": 0, "Apr": 4.00, "May": 1.00, "Jun": 5.00, "Jul": 0, "Aug": 2.00},
    {"Rank": 15, "Restaurant": "Wayward Fare", "City": "Brooklyn", "State": "NY", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 11.00, "Mar": 0, "Apr": 3.00, "May": 0, "Jun": 5.00, "Jul": 0, "Aug": 0},
])

# NEW PODs added this past week (07.24 → 07.31 snapshots)
new_pods_week = pd.DataFrame([
    # ON-PREMISE (15 new)
    {"Account": "True Food Kitchen-Reston", "City": "Reston", "State": "VA", "Premise": "On", "Chain": "True Food Kitchen", "Channel": "Restaurant", "Cases": 3},
    {"Account": "True Food Kitchen-Fairfax", "City": "Fairfax", "State": "VA", "Premise": "On", "Chain": "True Food Kitchen", "Channel": "Recreation/ Entertainment", "Cases": 3},
    {"Account": "True Food Kitchen-Arlington", "City": "Arlington", "State": "VA", "Premise": "On", "Chain": "True Food Kitchen", "Channel": "Restaurant", "Cases": 3},
    {"Account": "Vintage Wine Bar", "City": "Dallas", "State": "TX", "Premise": "On", "Chain": "(indep)", "Channel": "Other On Premise", "Cases": 2},
    {"Account": "Nyc 7TH Avenue Deli & Market", "City": "Seattle", "State": "WA", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 1},
    {"Account": "Trattoria Amici", "City": "Glendale", "State": "CA", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 1},
    {"Account": "South Beverly Grill", "City": "Beverly Hills", "State": "CA", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 1},
    {"Account": "Waterhawk", "City": "Rohnert Park", "State": "CA", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 1},
    {"Account": "Robey Hotel", "City": "Chicago", "State": "IL", "Premise": "On", "Chain": "(indep)", "Channel": "Hotel/Motel", "Cases": 0.58},
    {"Account": "Root Cellar Cafe And Catering", "City": "Chapel Hill", "State": "NC", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 0.5},
    {"Account": "Inn And Spa At Loretto", "City": "Santa Fe", "State": "NM", "Premise": "On", "Chain": "(indep)", "Channel": "Hotel/Motel", "Cases": 0.33},
    {"Account": "Serrano Country Club", "City": "El Dorado Hills", "State": "CA", "Premise": "On", "Chain": "ClubProcure", "Channel": "Golf / Country Club", "Cases": 0.25},
    {"Account": "Italian Brothers Restaurant", "City": "Los Gatos", "State": "CA", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 0.25},
    {"Account": "Fariner Bakery", "City": "Wahoo", "State": "NE", "Premise": "On", "Chain": "(indep)", "Channel": "Bar/Tavern", "Cases": 0.25},
    {"Account": "P Onde Juancho", "City": "Chelsea", "State": "MA", "Premise": "On", "Chain": "(indep)", "Channel": "Bar/Tavern", "Cases": 0.08},
    # OFF-PREMISE (33 new)
    {"Account": "Spring Street Wine Shop", "City": "New York", "State": "NY", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package", "Cases": 2},
    {"Account": "Super Spirits #46514", "City": "Pequot Lakes", "State": "MN", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package", "Cases": 1.17},
    {"Account": "Liquor Boy", "City": "Saint Louis Park", "State": "MN", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package", "Cases": 1.17},
    {"Account": "Elevated Beer Wine & Spir", "City": "Minneapolis", "State": "MN", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package", "Cases": 1.17},
    {"Account": "Savage City Liquors", "City": "Savage", "State": "MN", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package", "Cases": 1.17},
    {"Account": "Liquors On Allen", "City": "New York", "State": "NY", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package", "Cases": 1},
    {"Account": "39TH Street Wine Inc", "City": "New York", "State": "NY", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package", "Cases": 1},
    {"Account": "Huntington Wine Cellar", "City": "Huntington", "State": "NY", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package", "Cases": 1},
    {"Account": "Safeway #1019", "City": "Alexandria", "State": "VA", "Premise": "Off", "Chain": "Safeway", "Channel": "Supermarket", "Cases": 1},
    {"Account": "Safeway #1847", "City": "Alexandria", "State": "VA", "Premise": "Off", "Chain": "Safeway", "Channel": "Supermarket", "Cases": 1},
    {"Account": "Total Wine & More #1601", "City": "Bloomington", "State": "MN", "Premise": "Off", "Chain": "Total Wine & More", "Channel": "Liquor/Package", "Cases": 1},
    {"Account": "Total Wine & More #1602", "City": "Roseville", "State": "MN", "Premise": "Off", "Chain": "Total Wine & More", "Channel": "Liquor/Package", "Cases": 1},
    {"Account": "Total Wine & More #1606", "City": "Chanhassen", "State": "MN", "Premise": "Off", "Chain": "Total Wine & More", "Channel": "Liquor/Package", "Cases": 1},
    {"Account": "Food Lion # 0959", "City": "Palmyra", "State": "VA", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.5},
    {"Account": "Food Lion # 1322", "City": "Herndon", "State": "VA", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.5},
    {"Account": "Liquor Store The", "City": "Pierce", "State": "NE", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package", "Cases": 0.5},
    {"Account": "Food Lion # 1512", "City": "Suffolk", "State": "VA", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.5},
    {"Account": "Food Lion # 1320", "City": "Richmond", "State": "VA", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.5},
    {"Account": "Food Lion 1607", "City": "Calabash", "State": "NC", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.5},
    {"Account": "Food Lion 0809", "City": "Fayetteville", "State": "NC", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.5},
    {"Account": "Food Lion # 0555", "City": "Hampton", "State": "VA", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.5},
    {"Account": "Food Lion 2223", "City": "Southport", "State": "NC", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.5},
    {"Account": "Food Lion # 0943", "City": "Lorton", "State": "VA", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.5},
    {"Account": "Food Lion #2217", "City": "Charlotte", "State": "NC", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.25},
    {"Account": "Food Lion #0735", "City": "Oakboro", "State": "NC", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.25},
    {"Account": "Food Lion 1494", "City": "Jacksonville", "State": "NC", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.25},
    {"Account": "West Seattle Thriftway", "City": "Seattle", "State": "WA", "Premise": "Off", "Chain": "Thriftway Stores Of Washington", "Channel": "Supermarket", "Cases": 0.25},
    {"Account": "Food Lion #0925", "City": "High Point", "State": "NC", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.25},
    {"Account": "Harris Teeter 212", "City": "Carthage", "State": "NC", "Premise": "Off", "Chain": "Harris Teeter", "Channel": "Supermarket", "Cases": 0.25},
    {"Account": "Harris Teeter #182", "City": "Waxhaw", "State": "NC", "Premise": "Off", "Chain": "Harris Teeter", "Channel": "Supermarket", "Cases": 0.25},
    {"Account": "Food Lion # 0211", "City": "Virginia Beach", "State": "VA", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0.25},
    {"Account": "Total Wine & More #1608", "City": "Minnetonka", "State": "MN", "Premise": "Off", "Chain": "Total Wine & More", "Channel": "Liquor/Package", "Cases": 0.17},
    {"Account": "Alexander Wright--Smpl", "City": "Omaha", "State": "NE", "Premise": "Off", "Chain": "(indep)", "Channel": "Other Off Premise", "Cases": 0.08},
])
new_pods_week = new_pods_week.sort_values(["Premise", "Cases"], ascending=[True, False]).reset_index(drop=True)

# POD ORDER RECENCY — built by build_pod_recency.py from weekly Ethica snapshots
# Status: Green = last order ≤60d ago · Yellow = 60–90d · Red = 90+d (or pre-snapshot-history)
import json
import os
_recency_path = os.path.join(os.path.dirname(__file__), "pod_recency.json")
with open(_recency_path, "r", encoding="utf-8") as _f:
    _recency = json.load(_f)
pod_recency_df = pd.DataFrame(_recency["pods"])
POD_RECENCY_AS_OF = _recency["as_of"]
POD_RECENCY_EARLIEST_SNAPSHOT = _recency["earliest_snapshot"]

# IRI weekly retail-scan data (Ethica-provided IRI panel)
_iri_path = os.path.join(os.path.dirname(__file__), "iri.json")
with open(_iri_path, "r", encoding="utf-8") as _f:
    _iri = json.load(_f)
iri_df = pd.DataFrame(_iri["weeks"])
iri_df["week_ending"] = pd.to_datetime(iri_df["week_ending"])
IRI_AS_OF = _iri["as_of"]

# State-level WEEKLY ACTUALS (kept for reference but no longer used in main UI)
# State Performance now uses same-period comparison: Apr 1-24 vs Mar 1-27 from on_states/off_states.
state_weekly = pd.DataFrame([
    # ON-PREMISE
    {"Premise": "ON", "State": "AZ", "L7d Cases": 3.00, "P7d Cases": 3.00, "L7d PODs": 2, "P7d PODs": 1},
    {"Premise": "ON", "State": "CA", "L7d Cases": 3.09, "P7d Cases": 14.42, "L7d PODs": 3, "P7d PODs": 8},
    {"Premise": "ON", "State": "CO", "L7d Cases": 0, "P7d Cases": 1.00, "L7d PODs": 0, "P7d PODs": 1},
    {"Premise": "ON", "State": "CT", "L7d Cases": 0, "P7d Cases": 1.00, "L7d PODs": 0, "P7d PODs": 1},
    {"Premise": "ON", "State": "DC", "L7d Cases": 0, "P7d Cases": 0, "L7d PODs": 0, "P7d PODs": 0},
    {"Premise": "ON", "State": "DE", "L7d Cases": 0, "P7d Cases": 0.08, "L7d PODs": 0, "P7d PODs": 1},
    {"Premise": "ON", "State": "FL", "L7d Cases": 0, "P7d Cases": 16.08, "L7d PODs": 0, "P7d PODs": 4},
    {"Premise": "ON", "State": "GA", "L7d Cases": 0, "P7d Cases": 0, "L7d PODs": 0, "P7d PODs": 0},
    {"Premise": "ON", "State": "IL", "L7d Cases": 0, "P7d Cases": 0.08, "L7d PODs": 0, "P7d PODs": 1},
    {"Premise": "ON", "State": "KY", "L7d Cases": 3.50, "P7d Cases": 0, "L7d PODs": 6, "P7d PODs": 0},
    {"Premise": "ON", "State": "MD", "L7d Cases": 5.25, "P7d Cases": 0.08, "L7d PODs": 4, "P7d PODs": 0},
    {"Premise": "ON", "State": "NC", "L7d Cases": 0.33, "P7d Cases": 1.50, "L7d PODs": 1, "P7d PODs": 1},
    {"Premise": "ON", "State": "NJ", "L7d Cases": 1.42, "P7d Cases": 1.33, "L7d PODs": 2, "P7d PODs": 2},
    {"Premise": "ON", "State": "NM", "L7d Cases": 0.17, "P7d Cases": 0, "L7d PODs": 1, "P7d PODs": 0},
    {"Premise": "ON", "State": "NV", "L7d Cases": 0, "P7d Cases": 0, "L7d PODs": 0, "P7d PODs": 0},
    {"Premise": "ON", "State": "NY", "L7d Cases": 7.50, "P7d Cases": 1.17, "L7d PODs": 3, "P7d PODs": 2},
    {"Premise": "ON", "State": "OH", "L7d Cases": 1.09, "P7d Cases": 0.33, "L7d PODs": 2, "P7d PODs": 2},
    {"Premise": "ON", "State": "SC", "L7d Cases": 0.50, "P7d Cases": 0, "L7d PODs": 1, "P7d PODs": 0},
    {"Premise": "ON", "State": "TX", "L7d Cases": 1.66, "P7d Cases": 12.58, "L7d PODs": 2, "P7d PODs": 6},
    {"Premise": "ON", "State": "VA", "L7d Cases": 0, "P7d Cases": 0, "L7d PODs": 0, "P7d PODs": 0},
    {"Premise": "ON", "State": "WA", "L7d Cases": 0.16, "P7d Cases": 0.08, "L7d PODs": 2, "P7d PODs": 1},
    # OFF-PREMISE
    {"Premise": "OFF", "State": "AZ", "L7d Cases": 0, "P7d Cases": 0, "L7d PODs": 0, "P7d PODs": 0},
    {"Premise": "OFF", "State": "CA", "L7d Cases": 17.42, "P7d Cases": 13.08, "L7d PODs": 13, "P7d PODs": 11},
    {"Premise": "OFF", "State": "CO", "L7d Cases": 0, "P7d Cases": 0, "L7d PODs": 0, "P7d PODs": 0},
    {"Premise": "OFF", "State": "CT", "L7d Cases": 3.17, "P7d Cases": 2.00, "L7d PODs": 3, "P7d PODs": 2},
    {"Premise": "OFF", "State": "DC", "L7d Cases": 2.00, "P7d Cases": 1.00, "L7d PODs": 1, "P7d PODs": 1},
    {"Premise": "OFF", "State": "DE", "L7d Cases": 0, "P7d Cases": 0, "L7d PODs": 0, "P7d PODs": 0},
    {"Premise": "OFF", "State": "FL", "L7d Cases": -12.66, "P7d Cases": 6.42, "L7d PODs": 1, "P7d PODs": 8},
    {"Premise": "OFF", "State": "GA", "L7d Cases": 1.00, "P7d Cases": 0, "L7d PODs": 1, "P7d PODs": 0},
    {"Premise": "OFF", "State": "IL", "L7d Cases": 3.00, "P7d Cases": 6.00, "L7d PODs": 3, "P7d PODs": 4},
    {"Premise": "OFF", "State": "KY", "L7d Cases": 0, "P7d Cases": 0, "L7d PODs": 0, "P7d PODs": 0},
    {"Premise": "OFF", "State": "MD", "L7d Cases": 2.00, "P7d Cases": 1.08, "L7d PODs": 2, "P7d PODs": 2},
    {"Premise": "OFF", "State": "NC", "L7d Cases": 1.08, "P7d Cases": 2.42, "L7d PODs": 5, "P7d PODs": 8},
    {"Premise": "OFF", "State": "NJ", "L7d Cases": 4.25, "P7d Cases": 1.17, "L7d PODs": 1, "P7d PODs": 1},
    {"Premise": "OFF", "State": "NM", "L7d Cases": 0, "P7d Cases": 0.17, "L7d PODs": 0, "P7d PODs": 2},
    {"Premise": "OFF", "State": "NY", "L7d Cases": 6.00, "P7d Cases": 4.50, "L7d PODs": 2, "P7d PODs": 4},
    {"Premise": "OFF", "State": "OH", "L7d Cases": 1.00, "P7d Cases": 1.17, "L7d PODs": 0, "P7d PODs": 2},
    {"Premise": "OFF", "State": "SC", "L7d Cases": 1.50, "P7d Cases": 0.50, "L7d PODs": 2, "P7d PODs": 2},
    {"Premise": "OFF", "State": "TX", "L7d Cases": 1.00, "P7d Cases": 6.17, "L7d PODs": 0, "P7d PODs": 7},
    {"Premise": "OFF", "State": "VA", "L7d Cases": 3.34, "P7d Cases": 0.08, "L7d PODs": 4, "P7d PODs": 1},
])

# Trade channel breakdown (Ethica 07.24.26, samples / internal accounts removed)
off_trade_channels = pd.DataFrame([
    {"Trade Channel": "Liquor / Package Store", "YTD Cases": 1595.63, "Dec": 3.40, "Jan": 132.81, "Feb": 192.62, "Mar": 224.97, "Apr": 117.49, "May": 181.24, "Jun": 264.59, "Jul": 311.34, "Aug": 167.17},
    {"Trade Channel": "Supermarket", "YTD Cases": 770.41, "Dec": 0, "Jan": 51.50, "Feb": 86.66, "Mar": 125.22, "Apr": 70.58, "May": 156.50, "Jun": 109.94, "Jul": 86.34, "Aug": 83.69},
    {"Trade Channel": "Other Off Premise", "YTD Cases": 554.57, "Dec": 5.75, "Jan": 26.32, "Feb": 185.91, "Mar": 42.65, "Apr": 62.08, "May": 47.49, "Jun": 60.84, "Jul": 84.50, "Aug": 38.00},
    {"Trade Channel": "General Merchandise", "YTD Cases": 107.00, "Dec": 0, "Jan": 13.00, "Feb": 19.00, "Mar": 4.00, "Apr": 13.00, "May": 8.00, "Jun": 15.00, "Jul": 20.00, "Aug": 15.00},
    {"Trade Channel": "Wholesale Club", "YTD Cases": 40.25, "Dec": 0, "Jan": 0, "Feb": 4.00, "Mar": 8.00, "Apr": 3.17, "May": 8.08, "Jun": 6.00, "Jul": 3.00, "Aug": 8.00},
    {"Trade Channel": "Fine Wine Store", "YTD Cases": 15.33, "Dec": 0, "Jan": 0, "Feb": 1.08, "Mar": 2.25, "Apr": 2.00, "May": 4.67, "Jun": 2.08, "Jul": 0.91, "Aug": 2.33},
    {"Trade Channel": "Convenience / Gas", "YTD Cases": 14.09, "Dec": 1.00, "Jan": 0, "Feb": 1.25, "Mar": 3.83, "Apr": 2.59, "May": 1.25, "Jun": 2.00, "Jul": 2.17, "Aug": 0},
    {"Trade Channel": "Small Grocery Store", "YTD Cases": 9.00, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0, "Apr": 6.00, "May": 1.00, "Jun": 2.00, "Jul": 0, "Aug": 0},
    {"Trade Channel": "Retail Specialty Services", "YTD Cases": 1.75, "Dec": 0, "Jan": 0, "Feb": 0.50, "Mar": 0, "Apr": 0, "May": 0.25, "Jun": 0, "Jul": 0, "Aug": 1.00},
])

on_trade_channels = pd.DataFrame([
    {"Trade Channel": "Restaurant", "YTD Cases": 934.87, "Dec": 14.24, "Jan": 17.82, "Feb": 85.07, "Mar": 123.13, "Apr": 152.14, "May": 158.53, "Jun": 127.13, "Jul": 163.30, "Aug": 93.46},
    {"Trade Channel": "Bar / Tavern", "YTD Cases": 167.62, "Dec": 0.08, "Jan": 5.08, "Feb": 10.31, "Mar": 16.15, "Apr": 25.49, "May": 24.32, "Jun": 42.15, "Jul": 22.40, "Aug": 21.64},
    {"Trade Channel": "Other On Premise", "YTD Cases": 136.49, "Dec": 1.00, "Jan": 2.00, "Feb": 19.08, "Mar": 10.41, "Apr": 11.33, "May": 27.50, "Jun": 20.50, "Jul": 29.50, "Aug": 15.17},
    {"Trade Channel": "Hotel / Motel", "YTD Cases": 108.80, "Dec": 0, "Jan": 0.42, "Feb": 4.49, "Mar": 3.57, "Apr": 10.33, "May": 14.08, "Jun": 49.83, "Jul": 8.16, "Aug": 17.91},
    {"Trade Channel": "Golf / Country Club", "YTD Cases": 70.02, "Dec": 1.00, "Jan": 3.00, "Feb": 1.99, "Mar": 10.57, "Apr": 5.25, "May": 30.65, "Jun": 7.22, "Jul": 3.50, "Aug": 6.83},
    {"Trade Channel": "Concessionaire", "YTD Cases": 8.50, "Dec": 0, "Jan": 0, "Feb": 0.25, "Mar": 0, "Apr": 0.25, "May": 3.00, "Jun": 0, "Jul": 3.00, "Aug": 2.00},
    {"Trade Channel": "Special Event / Temp License", "YTD Cases": 4.50, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0, "Apr": 2.00, "May": 1.00, "Jun": 0.50, "Jul": 1.00, "Aug": 0},
    {"Trade Channel": "Recreation / Entertainment", "YTD Cases": 3.66, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0.08, "Apr": 0, "May": 0, "Jun": 0.08, "Jul": 0.50, "Aug": 3.00},
    {"Trade Channel": "Fine Dining / White Tablecloth", "YTD Cases": 0.25, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0.25, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0},
])
top_accounts["Chg vs LM"] = top_accounts["Apr Cases"] - top_accounts["Mar Cases"]
top_accounts["% Growth"] = top_accounts.apply(
    lambda r: ((r["Apr Cases"] - r["Mar Cases"]) / r["Mar Cases"] * 100) if r["Mar Cases"] > 0 else (float("inf") if r["Apr Cases"] > 0 else 0),
    axis=1,
)


# ══════════════════════════════════════════════════════════════════════════════
# NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
active_tab = st.radio(
    "Dashboard",
    ["Overview", "Shipments", "Depletions", "Account Explorer", "Gopuff", "ReserveBar"],
    horizontal=True,
    label_visibility="collapsed",
)

st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# SHARED MONTH OPTIONS
# ══════════════════════════════════════════════════════════════════════════════
DEPL_MONTHS = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
SHIP_MONTHS = ["Dec '25", "Jan '26", "Feb '26", "Mar '26", "Apr '26", "May '26"]
ALL_STATES = sorted(set(on_states["State"].tolist() + off_states["State"].tolist()))

# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW — master cross-channel summary
# ══════════════════════════════════════════════════════════════════════════════
if active_tab == "Overview":
    ov_months = st.multiselect("Filter by Month", DEPL_MONTHS, default=DEPL_MONTHS, key="ov_months")
    gm_filt = grand_monthly[grand_monthly["Month"].isin(ov_months)]
    cm_filt = combined_monthly[combined_monthly["Month"].isin(ov_months)]

    total_cases = gm_filt["Cases"].sum()
    total_on = cm_filt["On-Premise"].sum()
    total_off = cm_filt["Off-Premise"].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(kpi("Total Depletions YTD", f"{total_cases:,.2f}", f"Cases · samples excl · as of {DEPLETION_AS_OF}", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Total YTD PODs", "2,069", "28 active states", dark=True), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Cases Shipped YTD", "5,611", "Dec '25 - May '26"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Gopuff YTD Units", "169", f"29 locations · as of {GOPUFF_AS_OF}"), unsafe_allow_html=True)
    with c5:
        st.markdown(kpi("ReserveBar Units", "86", "27 orders · as of 4/25/26"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        section_title("Monthly Depletions (Cases)")
        st.plotly_chart(bar_chart(gm_filt, "Month", "Cases"), use_container_width=True)

    with col2:
        section_title("On-Premise vs Off-Premise by Month")
        st.plotly_chart(
            grouped_bar(cm_filt, "Month", "On-Premise", "Off-Premise", "On-Premise", "Off-Premise"),
            use_container_width=True,
        )

    # Channel breakdown table — redesigned with same-period MoM
    section_title("Channel Breakdown")
    st.caption("ℹ️ Partial months compare to same-period prior month (e.g., Aug (1-28) vs Jul 1-28), NOT full prior month")
    cd_filt = channel_detail[channel_detail["Short"].isin(ov_months)].copy()
    cd_display = cd_filt[["Month", "Total Depletions", "Compare Ref", "Depl Change vs LM", "% Change vs LM", "On-Premise", "Off-Premise"]].copy()

    fmt_map = {
        "Total Depletions": lambda v: f"{v:,.2f}",
        "Compare Ref": lambda v: str(v) if v else "—",
        "Depl Change vs LM": lambda v: change_fmt(v),
        "% Change vs LM": lambda v: pct_change_fmt(v),
        "On-Premise": lambda v: f"{v:,.2f}",
        "Off-Premise": lambda v: f"{v:,.2f}",
    }
    st.markdown(styled_table(cd_display, fmt=fmt_map), unsafe_allow_html=True)

    # Top 3 States
    section_title("Top 3 States by Depletions")
    top3_display = top3_states[["State", "Total Cases", "Total PODs", "On Cases", "Off Cases"]].copy()
    top3_fmt = {
        "Total Cases": lambda v: f"{v:,.2f}",
        "Total PODs": lambda v: f"{int(v):,}",
        "On Cases": lambda v: f"{v:,.2f}",
        "Off Cases": lambda v: f"{v:,.2f}",
    }
    st.markdown(styled_table(top3_display, fmt=top3_fmt), unsafe_allow_html=True)

    # ── NEW PODs THIS PAST WEEK ──────────────────────────────────────────────
    section_title("New PODs This Past Week")
    n_total = len(new_pods_week)
    n_on = int((new_pods_week["Premise"] == "On").sum())
    n_off = int((new_pods_week["Premise"] == "Off").sum())
    cs_total = new_pods_week["Cases"].sum()
    cs_on = new_pods_week.loc[new_pods_week["Premise"] == "On", "Cases"].sum()
    cs_off = new_pods_week.loc[new_pods_week["Premise"] == "Off", "Cases"].sum()
    state_count = new_pods_week["State"].nunique()
    st.caption(
        f"📍 {NEW_POD_WEEK_RANGE} · samples excluded · accounts that first depleted Lucci during this week"
    )

    npk1, npk2, npk3, npk4 = st.columns(4)
    with npk1:
        st.markdown(kpi("New PODs (Total)", f"{n_total}", f"Across {state_count} states", dark=True), unsafe_allow_html=True)
    with npk2:
        st.markdown(kpi("New PODs · On-Premise", f"{n_on}", f"{cs_on:.2f} cases"), unsafe_allow_html=True)
    with npk3:
        st.markdown(kpi("New PODs · Off-Premise", f"{n_off}", f"{cs_off:.2f} cases"), unsafe_allow_html=True)
    with npk4:
        st.markdown(kpi("New-Acct Volume", f"{cs_total:.2f}", "Cases this week"), unsafe_allow_html=True)

    npk_display = new_pods_week[["Account", "City", "State", "Premise", "Chain", "Channel", "Cases"]].copy()
    npk_fmt = {"Cases": lambda v: f"{v:,.2f}"}
    st.markdown(styled_table(npk_display, fmt=npk_fmt), unsafe_allow_html=True)

    # Highlight banner
    st.markdown(f"""
    <div class="highlight-banner">
        <div>
            <p style="margin:0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.15em; text-transform:uppercase;">Filtered Period Summary &middot; Depletions as of {DEPLETION_AS_OF}</p>
            <p style="margin:8px 0 0; font-size:18px; color:white; font-weight:900; letter-spacing:0.02em;">Lucci performance across all channels</p>
            <p style="margin:4px 0 0; font-size:13px; color:rgba(255,255,255,0.7);">{total_cases:,.2f} depletion cases (samples excluded) &middot; {total_on:,.2f} on-premise &middot; {total_off:,.2f} off-premise</p>
        </div>
        <div style="display:flex; gap:32px; flex-shrink:0;">
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">{total_cases:,.1f}</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">TOTAL CASES</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">2,069</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">TOTAL PODS</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">24</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">STATES</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SHIPMENTS & REVENUE
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Shipments":
    st.caption("📅 Shipment data through May 2026 · Source: Lucci Payment Process file")
    sh_months = st.multiselect("Filter by Month", SHIP_MONTHS, default=SHIP_MONTHS, key="sh_months")
    sc_filt = ship_monthly_cases[ship_monthly_cases["Month"].isin(sh_months)].reset_index(drop=True)

    filt_cases = int(sc_filt["Cases"].sum())
    avg_cases = round(filt_cases / max(len(sc_filt), 1))
    biggest_row = sc_filt.loc[sc_filt["Cases"].idxmax()] if len(sc_filt) > 0 else None

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(kpi("Total Cases Shipped", f"{filt_cases:,}", f"Filtered period · {len(sc_filt)} month(s)", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Avg Cases / Month", f"{avg_cases:,}", "In filtered period"), unsafe_allow_html=True)
    with c3:
        if biggest_row is not None:
            st.markdown(kpi("Biggest Month", str(biggest_row["Month"]), f"{int(biggest_row['Cases']):,} cases shipped"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    section_title("Monthly Cases Shipped")
    fig = bar_chart(sc_filt, "Month", "Cases")
    fig.update_traces(text=sc_filt["Cases"].apply(lambda x: f"{x:,.0f}"), textposition="outside")
    fig.update_layout(height=360)
    st.plotly_chart(fig, use_container_width=True)

    section_title("Monthly Shipment Detail")
    sc_filt["Chg vs LM"] = sc_filt["Cases"].diff()
    st.markdown(styled_table(sc_filt[["Month", "Cases", "Chg vs LM"]], fmt={
        "Cases": lambda v: f"{int(v):,}",
        "Chg vs LM": lambda v: "—" if pd.isna(v) else (f"+{int(v):,}" if v > 0 else f"{int(v):,}"),
    }), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DEPLETIONS — merged On + Off Premise
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Depletions":
    st.caption(f"📅 Depletion data as of **{DEPLETION_AS_OF}** · Samples / internal accounts excluded · Source: Ethica weekly snapshots")
    fc1, fc2 = st.columns(2)
    with fc1:
        dp_months = st.multiselect("Filter by Month", DEPL_MONTHS, default=DEPL_MONTHS, key="dp_months")
    with fc2:
        dp_states = st.multiselect("Filter by State", ALL_STATES, default=ALL_STATES, key="dp_states")

    cm_filt = combined_monthly[combined_monthly["Month"].isin(dp_months)]
    on_filt = on_states[on_states["State"].isin(dp_states)]
    off_filt = off_states[off_states["State"].isin(dp_states)]

    total_on = on_filt["YTD Cases"].sum()
    total_off = off_filt["YTD Cases"].sum()
    total_all = total_on + total_off
    total_on_pods = int(on_filt["YTD PODs"].sum())
    total_off_pods = int(off_filt["YTD PODs"].sum())
    total_pods = total_on_pods + total_off_pods
    on_pct = round(total_on / total_all * 100) if total_all > 0 else 0
    off_pct = 100 - on_pct

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi("Total YTD (Cases)", f"{total_all:,.2f}", f"as of {DEPLETION_AS_OF}", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Total PODs", f"{total_pods:,}", f"as of {DEPLETION_AS_OF}"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("On-Premise YTD", f"{total_on:,.2f}", f"{total_on_pods} PODs · {on_pct}% of total"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Off-Premise YTD", f"{total_off:,.2f}", f"{total_off_pods} PODs · {off_pct}% of total"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Depletions + Active PODs trend (new line chart) ──
    section_title("Depletions & Active PODs by Month")
    st.caption("Monthly depletions (cases, left axis) alongside monthly active POD count (accounts that ordered that month, right axis).")
    st.plotly_chart(
        dual_axis_line(gm_filt, "Month", "Cases", "PODs",
                        "Depletions (Cases)", "Active PODs"),
        use_container_width=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    section_title("On-Premise vs Off-Premise by Month")
    st.plotly_chart(
        grouped_bar(cm_filt, "Month", "On-Premise", "Off-Premise", "On-Premise", "Off-Premise"),
        use_container_width=True,
    )

    # Monthly detail table — same-period MoM for partial months
    section_title("Monthly Depletion Detail")
    st.caption(f"Samples excluded · as of {DEPLETION_AS_OF} · ℹ️ Partial months compare to same-period prior month (e.g., Aug (1-28) vs Jul 1-28)")
    cd_filt = channel_detail[channel_detail["Short"].isin(dp_months)].copy()
    cd_display = cd_filt[["Month", "Total Depletions", "Total PODs", "Compare Ref", "Depl Change vs LM", "% Change vs LM", "On-Premise", "Off-Premise"]].copy()
    st.markdown(styled_table(cd_display, fmt={
        "Total Depletions": lambda v: f"{v:,.2f}",
        "Total PODs": lambda v: f"{int(v):,}",
        "Compare Ref": lambda v: str(v) if v else "—",
        "Depl Change vs LM": lambda v: change_fmt(v),
        "% Change vs LM": lambda v: pct_change_fmt(v),
        "On-Premise": lambda v: f"{v:,.2f}",
        "Off-Premise": lambda v: f"{v:,.2f}",
    }), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── State Performance — Jun / Jul / Aug with new PODs ──
    section_title("State Performance — Jun / Jul / Aug")
    st.caption(f"As of {DEPLETION_AS_OF}. Jun & Jul are full months (apples-to-apples MoM); Aug is partial (1–21). PODs are cumulative: 'YTD PODs' = total unique distribution points active YTD (repeat purchases don't add a new POD). 'New Jul/Aug PODs' = retail accounts activated for the FIRST time that month. Samples / internal accounts excluded.")

    state_view = st.radio(
        "View",
        ["Total", "On-Premise", "Off-Premise"],
        horizontal=True,
        key="state_view_toggle",
        label_visibility="collapsed",
    )

    on_f = on_states[on_states["State"].isin(dp_states)].copy()
    off_f = off_states[off_states["State"].isin(dp_states)].copy()

    sp_cols = ["Jun Cases", "Jul Cases", "Aug Cases", "YTD PODs", "New Jul PODs", "New Aug PODs"]
    if state_view == "On-Premise":
        sp = on_f[["State"] + sp_cols].copy()
    elif state_view == "Off-Premise":
        sp = off_f[["State"] + sp_cols].copy()
    else:
        on_agg = on_f.groupby("State", as_index=False)[sp_cols].sum()
        off_agg = off_f.groupby("State", as_index=False)[sp_cols].sum()
        sp = pd.concat([on_agg, off_agg]).groupby("State", as_index=False).sum()

    sp = sp.sort_values("Jul Cases", ascending=False).reset_index(drop=True)

    sp_display = sp[["State", "Jun Cases", "Jul Cases", "Aug Cases", "YTD PODs", "New Jul PODs", "New Aug PODs"]].copy()

    st.caption("Click any column header to sort · e.g. sort by YTD PODs to find top-POD states, or Aug Cases to spot top current-period movers")
    st.dataframe(
        sp_display, use_container_width=True, hide_index=True, height=520,
        column_config={
            "Jun Cases": st.column_config.NumberColumn("Jun Cases", format="%.2f"),
            "Jul Cases": st.column_config.NumberColumn("Jul Cases", format="%.2f"),
            "Aug Cases": st.column_config.NumberColumn("Aug MTD", format="%.2f"),
            "YTD PODs":  st.column_config.NumberColumn("YTD PODs", format="%d"),
            "New Jul PODs": st.column_config.NumberColumn("New Jul PODs", format="%d"),
            "New Aug PODs": st.column_config.NumberColumn("New Aug PODs", format="%d"),
        },
    )

    # ── State Drill-Down: Top accounts within key 5 states ──
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Top Accounts by Key State")
    st.caption(f"Top accounts within the top 6 states by combined depletions · sorted by YTD cases · as of {DEPLETION_AS_OF} · Samples excluded")

    drill_state = st.radio(
        "Drill-down state",
        ["CA", "NY", "NJ", "FL", "IL", "TX"],
        horizontal=True,
        key="state_drill",
        label_visibility="collapsed",
    )
    sda = state_top_accounts[state_top_accounts["State"] == drill_state].copy()
    sda["Chg vs LM"] = sda["Jul Cases"] - sda["Jun Cases"]
    sda["% Growth"] = sda.apply(
        lambda r: ((r["Jul Cases"] - r["Jun Cases"]) / r["Jun Cases"] * 100) if r["Jun Cases"] > 0 else (float("inf") if r["Jul Cases"] > 0 else 0),
        axis=1,
    )
    st.dataframe(
        sda[["Account", "Premise", "YTD Cases", "YTD PODs", "Jun Cases", "Jul Cases", "Aug Cases"]],
        use_container_width=True, hide_index=True, height=480,
        column_config={
            "YTD Cases": st.column_config.NumberColumn("YTD Cases", format="%.2f"),
            "YTD PODs":  st.column_config.NumberColumn("YTD PODs", format="%d"),
            "Jun Cases": st.column_config.NumberColumn("Jun Cases", format="%.2f"),
            "Jul Cases": st.column_config.NumberColumn("Jul Cases", format="%.2f"),
            "Aug Cases": st.column_config.NumberColumn("Aug MTD",   format="%.2f"),
        },
    )

    # ── Top 10 Restaurants / Bars ──
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Top 10 Restaurants & Bars by YTD Depletions")
    st.caption(f"On-premise restaurants, bars, and fine-dining accounts · sorted by YTD cases · as of {DEPLETION_AS_OF} · Samples excluded")
    st.dataframe(
        top_restaurants_bars[["Rank", "Restaurant", "City", "State", "Chain", "Channel", "YTD Cases", "Jun", "Jul", "Aug"]],
        use_container_width=True, hide_index=True, height=560,
        column_config={
            "Rank":      st.column_config.NumberColumn("Rank", format="%d"),
            "YTD Cases": st.column_config.NumberColumn("YTD Cases", format="%.2f"),
            "Jun":       st.column_config.NumberColumn("Jun", format="%.2f"),
            "Jul":       st.column_config.NumberColumn("Jul", format="%.2f"),
            "Aug":       st.column_config.NumberColumn("Aug MTD", format="%.2f"),
        },
    )

    # Trade channel breakdown — Jan through current, with MTD + %vs Jul same-period
    st.markdown("<br>", unsafe_allow_html=True)

    def _tc_with_mtd(df):
        """Add 'Jul 1-28' (Jul scaled to same-period MTD as Aug) and '% vs Jul' columns."""
        out = df.copy()
        out["Jul 1-28"] = out["Jul"] * (28/31)
        out["% vs Jul"] = out.apply(
            lambda r: ((r["Aug"] - r["Jul 1-28"]) / r["Jul 1-28"] * 100) if r["Jul 1-28"] > 0 else 0,
            axis=1,
        )
        return out

    section_title("Off-Premise by Trade Channel")
    st.caption(f"As of {DEPLETION_AS_OF} · Jan 2026 → Aug MTD · '% vs Jul' compares Aug 1-28 to Jul scaled to 28 days (same-period). Click any column to sort. Samples / internal excluded.")
    tc_off = _tc_with_mtd(off_trade_channels)
    st.dataframe(
        tc_off[["Trade Channel", "YTD Cases", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "% vs Jul"]],
        use_container_width=True, hide_index=True, height=360,
        column_config={
            "YTD Cases": st.column_config.NumberColumn("YTD Cases", format="%.2f"),
            "Jan": st.column_config.NumberColumn("Jan", format="%.2f"),
            "Feb": st.column_config.NumberColumn("Feb", format="%.2f"),
            "Mar": st.column_config.NumberColumn("Mar", format="%.2f"),
            "Apr": st.column_config.NumberColumn("Apr", format="%.2f"),
            "May": st.column_config.NumberColumn("May", format="%.2f"),
            "Jun": st.column_config.NumberColumn("Jun", format="%.2f"),
            "Jul": st.column_config.NumberColumn("Jul", format="%.2f"),
            "Aug": st.column_config.NumberColumn("Aug MTD", format="%.2f"),
            "% vs Jul": st.column_config.NumberColumn("% vs Jul 1-28", format="%+.1f%%"),
        },
    )

    section_title("On-Premise by Trade Channel")
    st.caption(f"As of {DEPLETION_AS_OF} · Jan 2026 → Aug MTD · '% vs Jul' compares Aug 1-28 to Jul scaled to 28 days (same-period). Click any column to sort. Samples / internal excluded.")
    tc_on = _tc_with_mtd(on_trade_channels)
    st.dataframe(
        tc_on[["Trade Channel", "YTD Cases", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "% vs Jul"]],
        use_container_width=True, hide_index=True, height=360,
        column_config={
            "YTD Cases": st.column_config.NumberColumn("YTD Cases", format="%.2f"),
            "Jan": st.column_config.NumberColumn("Jan", format="%.2f"),
            "Feb": st.column_config.NumberColumn("Feb", format="%.2f"),
            "Mar": st.column_config.NumberColumn("Mar", format="%.2f"),
            "Apr": st.column_config.NumberColumn("Apr", format="%.2f"),
            "May": st.column_config.NumberColumn("May", format="%.2f"),
            "Jun": st.column_config.NumberColumn("Jun", format="%.2f"),
            "Jul": st.column_config.NumberColumn("Jul", format="%.2f"),
            "Aug": st.column_config.NumberColumn("Aug MTD", format="%.2f"),
            "% vs Jul": st.column_config.NumberColumn("% vs Jul 1-28", format="%+.1f%%"),
        },
    )

    # Top 15 accounts - toggleable (Overall / On / Off)
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Top 15 Accounts by YTD Depletions")
    st.caption(f"As of {DEPLETION_AS_OF} · Apr is full month · Samples / internal accounts excluded · Source: Ethica depletion report")

    acct_view = st.radio(
        "Account view",
        ["Overall", "On-Premise", "Off-Premise"],
        horizontal=True,
        key="acct_view_toggle",
        label_visibility="collapsed",
    )
    if acct_view == "On-Premise":
        ta_filt = top_accounts[top_accounts["Premise"] == "On"].copy()
    elif acct_view == "Off-Premise":
        ta_filt = top_accounts[top_accounts["Premise"] == "Off"].copy()
    else:
        ta_filt = top_accounts.copy()
    ta_filt = ta_filt.sort_values("YTD Cases", ascending=False).head(15).reset_index(drop=True)

    # Top 15 chart
    st.plotly_chart(
        bar_chart(ta_filt, "Account", "YTD Cases", horizontal=True),
        use_container_width=True,
    )

    acct_display = ta_filt[["Account", "Premise", "States", "YTD Cases", "YTD PODs", "Mar Cases", "Apr Cases", "May Cases"]].copy()
    st.markdown(styled_table(acct_display, fmt={
        "YTD Cases": lambda v: f"{v:,.2f}",
        "YTD PODs": lambda v: f"{int(v):,}",
        "Mar Cases": lambda v: f"{v:,.2f}",
        "Apr Cases": lambda v: f"{v:,.2f}",
        "May Cases": lambda v: f"{v:,.2f}",
    }), unsafe_allow_html=True)

    # ── POD ORDER RECENCY — all PODs flagged by last order date ──
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("POD Order Recency — All Accounts")
    st.caption(
        f"All {len(pod_recency_df):,} active PODs flagged by days since last order (samples excluded). "
        f"🟢 Green = ordered within 60d · 🟡 Yellow = 60–90d · 🔴 Red = 90+d. "
        f"Built from weekly Ethica snapshots (earliest: {POD_RECENCY_EARLIEST_SNAPSHOT}); accounts whose first visible activity predates that date are conservatively flagged Red."
    )

    n_red = int((pod_recency_df["status"] == "Red").sum())
    n_yel = int((pod_recency_df["status"] == "Yellow").sum())
    n_grn = int((pod_recency_df["status"] == "Green").sum())
    n_total_recency = len(pod_recency_df)
    pct_atrisk = round((n_red + n_yel) / n_total_recency * 100, 1) if n_total_recency else 0

    rk1, rk2, rk3, rk4 = st.columns(4)
    with rk1:
        st.markdown(kpi("Total Active PODs", f"{n_total_recency:,}", "Samples excluded", dark=True), unsafe_allow_html=True)
    with rk2:
        st.markdown(kpi("🔴 Stale (90+ days)", f"{n_red:,}", f"{round(n_red/n_total_recency*100,1)}% of PODs"), unsafe_allow_html=True)
    with rk3:
        st.markdown(kpi("🟡 Warming (60–90d)", f"{n_yel:,}", f"{round(n_yel/n_total_recency*100,1)}% of PODs"), unsafe_allow_html=True)
    with rk4:
        st.markdown(kpi("🟢 Active (≤60 days)", f"{n_grn:,}", f"{round(n_grn/n_total_recency*100,1)}% of PODs"), unsafe_allow_html=True)

    st.markdown(f"<p style='margin:8px 0; font-size:13px; color:#6b7280;'><strong>At-risk:</strong> {n_red + n_yel:,} PODs ({pct_atrisk}%) haven't ordered in 60+ days.</p>", unsafe_allow_html=True)

    # Filters
    rec_states = sorted(pod_recency_df["state"].unique().tolist())
    rec_premises = sorted(pod_recency_df["premise"].unique().tolist())
    rc1, rc2, rc3, rc4 = st.columns([1.2, 1.4, 1.4, 1.6])
    with rc1:
        rec_status = st.multiselect("Status", ["Red", "Yellow", "Green"], default=["Red", "Yellow"], key="rec_status")
    with rc2:
        rec_state_filt = st.multiselect("State", rec_states, default=rec_states, key="rec_state_filt")
    with rc3:
        rec_prem_filt = st.multiselect("Premise", rec_premises, default=rec_premises, key="rec_prem_filt")
    with rc4:
        rec_search = st.text_input("Search account / city / chain", key="rec_search", placeholder="e.g. Marvito, Asheville, Eataly")

    rec_filt = pod_recency_df.copy()
    if rec_status:
        rec_filt = rec_filt[rec_filt["status"].isin(rec_status)]
    if rec_state_filt:
        rec_filt = rec_filt[rec_filt["state"].isin(rec_state_filt)]
    if rec_prem_filt:
        rec_filt = rec_filt[rec_filt["premise"].isin(rec_prem_filt)]
    if rec_search:
        s = rec_search.strip().lower()
        mask = (
            rec_filt["account"].astype(str).str.lower().str.contains(s, na=False) |
            rec_filt["city"].astype(str).str.lower().str.contains(s, na=False) |
            rec_filt["chain"].astype(str).str.lower().str.contains(s, na=False)
        )
        rec_filt = rec_filt[mask]

    st.caption(f"Showing **{len(rec_filt):,}** of {n_total_recency:,} PODs")

    # Color-coded display with Pandas Styler
    rec_display = rec_filt[["account", "city", "state", "premise", "chain", "channel", "ytd_cases", "last_order_date", "days_since", "status"]].copy()
    rec_display.columns = ["Account", "City", "State", "Premise", "Chain", "Channel", "YTD Cases", "Last Order", "Days Since", "Status"]

    def _row_color(row):
        s = row["Status"]
        if s == "Red":
            return ["background-color: #fee2e2; color: #7f1d1d"] * len(row)
        if s == "Yellow":
            return ["background-color: #fef3c7; color: #78350f"] * len(row)
        return ["background-color: #dcfce7; color: #14532d"] * len(row)

    styled = (rec_display.style
              .apply(_row_color, axis=1)
              .format({"YTD Cases": "{:,.2f}", "Days Since": "{:,}"})
              .hide(axis="index"))
    st.dataframe(styled, use_container_width=True, height=600)

    # ── IRI RETAIL SCAN DATA — 12-week trend ──
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("IRI Retail Scan — Weekly Trend")
    st.caption(
        f"IRI panel data provided by Ethica · latest week ending {IRI_AS_OF} · "
        f"Note: IRI's 'Stores Selling' is the scanned-panel store count, distinct from our full POD universe."
    )

    _iri_latest = iri_df.iloc[-1]
    ir1, ir2, ir3, ir4, ir5 = st.columns(5)
    with ir1:
        st.markdown(kpi("Dollar Sales (Latest 52-wk)", f"${_iri_latest['dollar_sales']:,.0f}",
                         f"Wk ending {_iri_latest['week_ending'].strftime('%m/%d/%y')}", dark=True), unsafe_allow_html=True)
    with ir2:
        st.markdown(kpi("Unit Sales", f"{int(_iri_latest['unit_sales']):,}",
                         f"9L equiv: {int(_iri_latest['volume_sales']):,}"), unsafe_allow_html=True)
    with ir3:
        st.markdown(kpi("Stores Selling", f"{int(_iri_latest['stores_selling']):,}",
                         f"{_iri_latest['cat_wtd_dist']:.2f}% category weighted"), unsafe_allow_html=True)
    with ir4:
        st.markdown(kpi("Avg Weekly $/Store", f"${_iri_latest['avg_wk_dollars_per_store']:.2f}",
                         f"{_iri_latest['avg_wk_units_per_store']:.2f} units/store"), unsafe_allow_html=True)
    with ir5:
        st.markdown(kpi("Weeks in Distribution", f"{int(_iri_latest['weeks_in_dist'])}",
                         f"Base price ${_iri_latest['wtd_avg_base_price']:.2f}"), unsafe_allow_html=True)

    # Compact trend charts — dollar sales, stores selling, and velocity
    ic1, ic2 = st.columns(2)
    with ic1:
        section_title("Dollar Sales · Stores Selling (weekly)")
        st.plotly_chart(
            dual_axis_line(iri_df, "week_ending", "dollar_sales", "stores_selling",
                            "Dollar Sales ($)", "Stores Selling"),
            use_container_width=True,
        )
    with ic2:
        section_title("Category Weighted Distribution · Avg $/Store")
        st.plotly_chart(
            dual_axis_line(iri_df, "week_ending", "cat_wtd_dist", "avg_wk_dollars_per_store",
                            "Cat Wtd Dist (%)", "Avg $/Store"),
            use_container_width=True,
        )

    # Full weekly table
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Weekly IRI Detail")
    iri_display = iri_df[[
        "week_ending", "dollar_sales", "unit_sales", "volume_sales",
        "stores_selling", "cat_wtd_dist",
        "avg_wk_dollars_per_store", "avg_wk_units_per_store",
        "wtd_avg_base_price", "wtd_avg_pct_price_reduction",
        "pct_any_merch", "weeks_in_dist",
    ]].copy()
    iri_display.columns = [
        "Week Ending", "$ Sales", "Units", "Volume (9L)",
        "Stores", "Cat Wtd Dist %",
        "Avg Wk $/Store", "Avg Wk Units/Store",
        "Base $", "Avg % Price Reduction",
        "% Volume on Merch", "Wks in Dist",
    ]
    iri_display["Week Ending"] = iri_display["Week Ending"].dt.strftime("%Y-%m-%d")
    st.dataframe(iri_display, use_container_width=True, height=420, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# ACCOUNT EXPLORER — full account-level performance with YTD + monthly rollups
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Account Explorer":
    st.caption(f"📅 Depletion data as of **{DEPLETION_AS_OF}** · Samples / internal accounts excluded · Source: Ethica weekly snapshots")

    section_title("Account Explorer — Search by name, premise, type, state")
    st.caption(
        f"All {len(pod_recency_df):,} active accounts (samples excluded) with YTD cases and full monthly rollup through {DEPLETION_AS_OF}. "
        f"Filter by any combination below. Table is sortable by clicking column headers."
    )

    ae_states = sorted(pod_recency_df["state"].unique().tolist())
    ae_channels = sorted(pod_recency_df["channel"].unique().tolist())
    ae_premises = sorted(pod_recency_df["premise"].unique().tolist())

    ae_search = st.text_input(
        "Search account / chain / city",
        key="ae_search",
        placeholder="e.g. Eataly, Wine.com, Chicago, Buona Forchetta",
    )

    aef_3, aef_4, aef_5 = st.columns(3)
    with aef_3:
        ae_prem = st.multiselect("Premise", ae_premises, default=ae_premises, key="ae_prem")
    with aef_4:
        ae_chn = st.multiselect("Trade Channel", ae_channels, default=ae_channels, key="ae_chn")
    with aef_5:
        ae_state = st.multiselect("State", ae_states, default=ae_states, key="ae_state")

    ae_filt = pod_recency_df.copy()
    if ae_prem:
        ae_filt = ae_filt[ae_filt["premise"].isin(ae_prem)]
    if ae_chn:
        ae_filt = ae_filt[ae_filt["channel"].isin(ae_chn)]
    if ae_state:
        ae_filt = ae_filt[ae_filt["state"].isin(ae_state)]
    if ae_search:
        s = ae_search.strip().lower()
        mask = (
            ae_filt["account"].astype(str).str.lower().str.contains(s, na=False) |
            ae_filt["chain"].astype(str).str.lower().str.contains(s, na=False) |
            ae_filt["city"].astype(str).str.lower().str.contains(s, na=False)
        )
        ae_filt = ae_filt[mask]

    # Summary metrics for the current filter
    ae_cases = ae_filt["ytd_cases"].sum()
    ae_aug_cases = ae_filt["aug"].sum() if "aug" in ae_filt.columns else 0
    ae_count = len(ae_filt)
    ae_states_filt = ae_filt["state"].nunique()
    aek1, aek2, aek3, aek4, aek5 = st.columns(5)
    with aek1:
        st.markdown(kpi("Accounts (filtered)", f"{ae_count:,}", f"of {len(pod_recency_df):,} total", dark=True), unsafe_allow_html=True)
    with aek2:
        st.markdown(kpi("Filtered YTD Cases", f"{ae_cases:,.2f}", f"Across {ae_states_filt} state(s)"), unsafe_allow_html=True)
    with aek3:
        st.markdown(kpi("Aug MTD Cases", f"{ae_aug_cases:,.2f}", "Through 8/28"), unsafe_allow_html=True)
    with aek4:
        active = int((ae_filt["status"] == "Green").sum())
        st.markdown(kpi("🟢 Active (≤60d)", f"{active:,}", f"{round(active/max(ae_count,1)*100,1)}% of filtered"), unsafe_allow_html=True)
    with aek5:
        stale = int((ae_filt["status"] == "Red").sum())
        st.markdown(kpi("🔴 Stale (90+d)", f"{stale:,}", f"{round(stale/max(ae_count,1)*100,1)}% of filtered"), unsafe_allow_html=True)

    # Prep display DataFrame — sortable via st.dataframe native click-to-sort
    ae_display = ae_filt[[
        "account", "city", "state", "premise", "chain", "channel",
        "ytd_cases", "jul", "aug",
        "last_order_date", "days_since", "status",
    ]].copy()
    ae_display.columns = [
        "Account", "City", "State", "Premise", "Chain", "Channel",
        "YTD Cases", "Jul", "Aug MTD",
        "Last Order", "Days Since", "Status",
    ]
    ae_display = ae_display.sort_values("YTD Cases", ascending=False)

    st.markdown(f"<p style='margin:4px 0; font-size:13px; color:#6b7280;'>Showing <strong>{len(ae_display):,}</strong> of {len(pod_recency_df):,} accounts · click column headers to sort</p>", unsafe_allow_html=True)
    st.dataframe(
        ae_display,
        use_container_width=True, height=650, hide_index=True,
        column_config={
            "YTD Cases": st.column_config.NumberColumn("YTD Cases", format="%.2f"),
            "Jul":       st.column_config.NumberColumn("Jul", format="%.2f"),
            "Aug MTD":   st.column_config.NumberColumn("Aug MTD", format="%.2f"),
            "Days Since": st.column_config.NumberColumn("Days Since", format="%d"),
        },
    )


# ══════════════════════════════════════════════════════════════════════════════
# GOPUFF (Updated with March 2026 Excel data)
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Gopuff":
    st.caption(f"📅 Gopuff data as of **{GOPUFF_AS_OF}** · Latest weekly bucket: week ending {GOPUFF_LATEST_WEEK} · Source: Gopuff weekly Lucci report")
    gp_all_states = gopuff_states["State"].tolist()
    gp_states = st.multiselect("Filter by State", gp_all_states, default=gp_all_states, key="gp_states")

    gs_filt = gopuff_states[gopuff_states["State"].isin(gp_states)]
    gl_filt = gopuff_location_detail[gopuff_location_detail["ST"].isin(gp_states)]
    filt_units = int(gs_filt["Units"].sum())
    filt_locs = int(gs_filt["Locations"].sum())

    gt_filt = gopuff_top_locations[gopuff_top_locations["State"].isin(gp_states)].head(5)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi("YTD Units Sold", str(filt_units), f"Jan - Apr 2026 · as of {GOPUFF_AS_OF}", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Active Locations", str(filt_locs), f"Across {len(gp_states)} state(s)"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Apr MTD Units", "21", f"Through week ending {GOPUFF_LATEST_WEEK}"), unsafe_allow_html=True)
    with c4:
        top_st = gs_filt.iloc[0] if len(gs_filt) > 0 else {"State": "-", "Units": 0, "Pct": 0}
        st.markdown(kpi("Top State", str(top_st["State"]), f"{int(top_st['Units'])} units · {top_st['Pct']}%"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.65, 1])

    with col1:
        section_title("Monthly Units Sold")
        fig = bar_chart(gopuff_monthly, "Month", "Units")
        fig.update_traces(
            text=gopuff_monthly["Units"].apply(lambda x: f"{x:,}"),
            textposition="outside",
            textfont=dict(size=14, color=TEXT_DARK),
        )
        fig.update_layout(height=300, yaxis=dict(range=[0, max(gopuff_monthly["Units"]) * 1.2]))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("Units by State")
        for _, row in gs_filt.iterrows():
            st.markdown(f"**{row['State']}** — {row['Units']} units ({row['Pct']}%)")
            st.progress(row["Pct"] / 100)
            st.caption(f"{row['Locations']} locations")

    section_title("Top Locations by YTD Units")
    if len(gt_filt) > 0:
        fig = bar_chart(gt_filt, "Location", "YTD", horizontal=True)
        fig.update_traces(
            text=gt_filt["YTD"].apply(lambda x: f"{x}"),
            textposition="outside",
            textfont=dict(size=12, color=TEXT_DARK),
        )
        fig.update_layout(height=220)
        st.plotly_chart(fig, use_container_width=True)

    section_title(f"Location Detail — Monthly Units (as of {GOPUFF_AS_OF}; thru week ending {GOPUFF_LATEST_WEEK})")
    detail_display = gl_filt[["Rank", "Location", "ST", "Jan", "Feb", "Mar", "Apr", "YTD"]].copy()
    detail_display = detail_display.replace(0, "-")
    st.markdown(styled_table(detail_display, fmt={
        "Rank": lambda v: str(v),
        "Jan": lambda v: str(v),
        "Feb": lambda v: str(v),
        "Mar": lambda v: str(v),
        "Apr": lambda v: str(v),
        "YTD": lambda v: f"<strong>{v}</strong>" if v != "-" else "-",
    }), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RESERVEBAR
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "ReserveBar":
    st.caption("📅 ReserveBar data as of **4/25/2026** · Source: ReserveBar partner dashboard")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(kpi("Revenue", "$1.74K", "Feb-Apr 2026", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Orders", "27", "27 unique customers"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Qty Sold", "86", "Units"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("AOV", "$64.35", "Avg order value"), unsafe_allow_html=True)
    with c5:
        st.markdown(kpi("AUO", "3.19", "Avg units/order"), unsafe_allow_html=True)
    with c6:
        st.markdown(kpi("Repeat Buyers", "4", "of 27 customers"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Monthly trend
    section_title("Monthly Units Sold")
    fig = bar_chart(rb_monthly, "Month", "Units")
    fig.update_traces(text=rb_monthly["Units"].apply(lambda x: f"{x}"), textposition="outside")
    fig.update_layout(height=260)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        section_title("Sales by Order Amount")
        st.plotly_chart(bar_chart(rb_order_range, "Range", "Pct"), use_container_width=True)

    with col2:
        section_title("Sales by Day of Week")
        st.plotly_chart(bar_chart(rb_dow, "Day", "Pct"), use_container_width=True)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        section_title("Share of Sales by # of Bottles")
        st.plotly_chart(bar_chart(rb_bottles, "Bottles", "Pct"), use_container_width=True)
    with col_b2:
        section_title("Key Stats")
        st.markdown(f"""
        <div style="background:{CREAM}; padding:16px; border-radius:6px; border:2px solid {RED_FAINT};">
            <p style="margin:0; font-size:13px; color:{TEXT_DARK};"><strong>2-bottle orders dominate</strong> — 40.7% of orders, followed by 1-bottle (22.2%)</p>
            <p style="margin:8px 0 0; font-size:13px; color:{TEXT_DARK};"><strong>Thu + Fri</strong> are peak days (22.2% each, 44% of weekly sales)</p>
            <p style="margin:8px 0 0; font-size:13px; color:{TEXT_DARK};"><strong>Feb was the strongest month</strong> at 62 units; Apr has slowed to 3 units MTD</p>
            <p style="margin:8px 0 0; font-size:13px; color:{TEXT_DARK};"><strong>Repeat rate: 14.8%</strong> (4 of 27 customers)</p>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        section_title("Customer Acquisition")
        acq1, acq2 = st.columns(2)
        with acq1:
            st.markdown(f"""
            <div style="background:{RED}; padding:22px 16px; text-align:center; border-radius:6px;">
                <span style="font-size:48px; font-weight:900; color:white; line-height:1;">23</span><br>
                <span style="font-size:11px; color:rgba(255,255,255,0.75); letter-spacing:0.1em; text-transform:uppercase;">New Customers</span><br>
                <span style="font-size:22px; color:white; font-weight:900;">85%</span>
            </div>""", unsafe_allow_html=True)
        with acq2:
            st.markdown(f"""
            <div style="background:{RED_MID}; padding:22px 16px; text-align:center; border-radius:6px;">
                <span style="font-size:48px; font-weight:900; color:white; line-height:1;">4</span><br>
                <span style="font-size:11px; color:rgba(255,255,255,0.75); letter-spacing:0.1em; text-transform:uppercase;">Repeat Customers</span><br>
                <span style="font-size:22px; color:white; font-weight:900;">15%</span>
            </div>""", unsafe_allow_html=True)

    with col4:
        section_title("Discount Code Usage")
        st.dataframe(rb_discounts, hide_index=True, use_container_width=True)
        st.caption("* All coupons had $0.00 discount value")

    st.markdown(f"""
    <div class="highlight-banner">
        <div>
            <p style="margin:0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.15em; text-transform:uppercase;">Top Item Sold</p>
            <p style="margin:8px 0 0; font-size:18px; color:white; font-weight:900; letter-spacing:0.02em;">Lucci Lambrusco Reggiano DOC Dry Sparkling Wine</p>
            <p style="margin:4px 0 0; font-size:13px; color:rgba(255,255,255,0.7);">Only SKU - 100% of Champagne & Sparkling category</p>
        </div>
        <div style="display:flex; gap:32px; flex-shrink:0;">
            <div style="text-align:center;">
                <p style="margin:0; font-size:32px; font-weight:900; color:white; line-height:1;">86</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">UNITS</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:32px; font-weight:900; color:white; line-height:1;">$1,737</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">REVENUE</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(f'<p class="footer-text">Data Period: Dec 2025 – Apr 2026 &middot; Depletions thru {DEPLETION_AS_OF} &middot; Gopuff thru {GOPUFF_AS_OF} &middot; Samples / internal accounts excluded &middot; Lucci Sales Intelligence</p>', unsafe_allow_html=True)

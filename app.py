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
            <p style="margin:0; font-size:13px; color:rgba(255,255,255,0.95); font-weight:700;">Depletions: 10/2/26 &middot; Gopuff: 4/25/26 &middot; ReserveBar: 4/25/26</p>
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
# Total excluded: 642 rows / 166.27 cases / 642 PODs.
# PODs are unique distribution points (no double-counting repeat purchases).
# "New PODs" = accounts activated for the FIRST time in a given month.
DEPLETION_AS_OF = "10/2/2026"

grand_monthly = pd.DataFrame([
    {"Month": "Nov", "Cases": 0, "PODs": 0},
    {"Month": "Dec", "Cases": 25.99, "PODs": 21},
    {"Month": "Jan", "Cases": 261.30, "PODs": 190},
    {"Month": "Feb", "Cases": 766.55, "PODs": 310},
    {"Month": "Mar", "Cases": 568.70, "PODs": 508},
    {"Month": "Apr", "Cases": 479.17, "PODs": 325},
    {"Month": "May", "Cases": 662.22, "PODs": 489},
    {"Month": "Jun", "Cases": 699.11, "PODs": 481},
    {"Month": "Jul", "Cases": 734.11, "PODs": 494},
    {"Month": "Aug", "Cases": 513.68, "PODs": 414},
    {"Month": "Sep", "Cases": 698.42, "PODs": 417},
    {"Month": "Oct", "Cases": 30.24, "PODs": 20},
])

combined_monthly = pd.DataFrame([
    {"Month": "Nov", "On-Premise": 0, "Off-Premise": 0},
    {"Month": "Dec", "On-Premise": 16.00, "Off-Premise": 9.99},
    {"Month": "Jan", "On-Premise": 27.33, "Off-Premise": 223.06},
    {"Month": "Feb", "On-Premise": 114.50, "Off-Premise": 486.80},
    {"Month": "Mar", "On-Premise": 160.92, "Off-Premise": 407.28},
    {"Month": "Apr", "On-Premise": 204.24, "Off-Premise": 274.51},
    {"Month": "May", "On-Premise": 255.15, "Off-Premise": 404.82},
    {"Month": "Jun", "On-Premise": 242.90, "Off-Premise": 455.13},
    {"Month": "Jul", "On-Premise": 227.00, "Off-Premise": 505.69},
    {"Month": "Aug", "On-Premise": 164.91, "Off-Premise": 347.85},
    {"Month": "Sep", "On-Premise": 225.26, "Off-Premise": 472.41},
    {"Month": "Oct", "On-Premise": 11.33, "Off-Premise": 18.91},
])

# Channel breakdown — chronological (oldest → newest)
channel_detail = pd.DataFrame([
    {"Month": "Nov 2025", "Short": "Nov", "Total Depletions": 0, "Total PODs": 0, "On-Premise": 0, "Off-Premise": 0},
    {"Month": "Dec 2025", "Short": "Dec", "Total Depletions": 25.99, "Total PODs": 21, "On-Premise": 16.00, "Off-Premise": 9.99},
    {"Month": "Jan 2026", "Short": "Jan", "Total Depletions": 261.30, "Total PODs": 190, "On-Premise": 27.33, "Off-Premise": 223.06},
    {"Month": "Feb 2026", "Short": "Feb", "Total Depletions": 766.55, "Total PODs": 310, "On-Premise": 114.50, "Off-Premise": 486.80},
    {"Month": "Mar 2026", "Short": "Mar", "Total Depletions": 568.70, "Total PODs": 508, "On-Premise": 160.92, "Off-Premise": 407.28},
    {"Month": "Apr 2026", "Short": "Apr", "Total Depletions": 479.17, "Total PODs": 325, "On-Premise": 204.24, "Off-Premise": 274.51},
    {"Month": "May 2026", "Short": "May", "Total Depletions": 662.22, "Total PODs": 489, "On-Premise": 255.15, "Off-Premise": 404.82},
    {"Month": "Jun 2026", "Short": "Jun", "Total Depletions": 699.11, "Total PODs": 481, "On-Premise": 242.90, "Off-Premise": 455.13},
    {"Month": "Jul 2026", "Short": "Jul", "Total Depletions": 734.11, "Total PODs": 494, "On-Premise": 227.00, "Off-Premise": 505.69},
    {"Month": "Aug 2026", "Short": "Aug", "Total Depletions": 513.68, "Total PODs": 414, "On-Premise": 164.91, "Off-Premise": 347.85},
    {"Month": "Sep 2026", "Short": "Sep", "Total Depletions": 698.42, "Total PODs": 417, "On-Premise": 225.26, "Off-Premise": 472.41},
    {"Month": "Oct 2026 (1-2)", "Short": "Oct", "Total Depletions": 30.24, "Total PODs": 20, "On-Premise": 11.33, "Off-Premise": 18.91},
])

# Same-period MTD comparison for partial months.
# For partial Oct (1-2), the comparison is vs Sep 1-2 (NOT full Sep).
# Sep 1-2 actuals interpolated between 09.04.26 (Sep 1-4) and 09.11.26 (Sep 1-11) snapshots.
PRIOR_MTD = {
    "Oct": {"cases": 56.09, "on": 12.62, "off": 43.46, "pods": 36, "ref": "Sep 1-2"},
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

# ON-PREMISE state data (from latest depletion tab, tight scrub applied)
on_states = pd.DataFrame([
    {"State": "CA", "YTD Cases": 457.50, "YTD PODs": 152, "Apr Cases": 54.25, "Apr PODs": 32, "May Cases": 89.67, "May PODs": 48, "Jun Cases": 55.83, "Jun PODs": 30, "Jul Cases": 52.33, "Jul PODs": 30, "Aug Cases": 46.17, "Aug PODs": 27, "Sep Cases": 53.66, "Sep PODs": 26, "Oct Cases": 2.00, "Oct PODs": 1, "New Aug PODs": 8, "New Sep PODs": 7, "New Oct PODs": 0},
    {"State": "NY", "YTD Cases": 233.59, "YTD PODs": 44, "Apr Cases": 18.00, "Apr PODs": 9, "May Cases": 32.75, "May PODs": 14, "Jun Cases": 52.00, "Jun PODs": 11, "Jul Cases": 28.75, "Jul PODs": 11, "Aug Cases": 18.00, "Aug PODs": 11, "Sep Cases": 45.17, "Sep PODs": 13, "Oct Cases": 1.33, "Oct PODs": 2, "New Aug PODs": 6, "New Sep PODs": 4, "New Oct PODs": 2},
    {"State": "IL", "YTD Cases": 179.07, "YTD PODs": 21, "Apr Cases": 24.00, "Apr PODs": 4, "May Cases": 19.00, "May PODs": 5, "Jun Cases": 27.41, "Jun PODs": 7, "Jul Cases": 38.00, "Jul PODs": 8, "Aug Cases": 9.58, "Aug PODs": 5, "Sep Cases": 14.00, "Sep PODs": 4, "Oct Cases": 1.00, "Oct PODs": 1, "New Aug PODs": 1, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "NJ", "YTD Cases": 125.41, "YTD PODs": 29, "Apr Cases": 6.25, "Apr PODs": 6, "May Cases": 21.58, "May PODs": 12, "Jun Cases": 15.00, "Jun PODs": 7, "Jul Cases": 25.34, "Jul PODs": 14, "Aug Cases": 13.17, "Aug PODs": 7, "Sep Cases": 12.08, "Sep PODs": 7, "Oct Cases": 2.00, "Oct PODs": 2, "New Aug PODs": 1, "New Sep PODs": 0, "New Oct PODs": 1},
    {"State": "FL", "YTD Cases": 124.58, "YTD PODs": 46, "Apr Cases": 35.00, "Apr PODs": 10, "May Cases": 10.08, "May PODs": 8, "Jun Cases": 9.08, "Jun PODs": 7, "Jul Cases": 23.08, "Jul PODs": 14, "Aug Cases": 12.08, "Aug PODs": 8, "Sep Cases": 10.00, "Sep PODs": 8, "Oct Cases": 3.00, "Oct PODs": 1, "New Aug PODs": 1, "New Sep PODs": 3, "New Oct PODs": 1},
    {"State": "TX", "YTD Cases": 100.50, "YTD PODs": 34, "Apr Cases": 18.50, "Apr PODs": 11, "May Cases": 15.00, "May PODs": 12, "Jun Cases": 14.25, "Jun PODs": 11, "Jul Cases": 9.00, "Jul PODs": 5, "Aug Cases": 7.83, "Aug PODs": 7, "Sep Cases": 13.92, "Sep PODs": 8, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 7, "New Sep PODs": 3, "New Oct PODs": 0},
    {"State": "NV", "YTD Cases": 83.00, "YTD PODs": 9, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 25.00, "May PODs": 3, "Jun Cases": 17.00, "Jun PODs": 2, "Jul Cases": 4.00, "Jul PODs": 3, "Aug Cases": 12.00, "Aug PODs": 2, "Sep Cases": 19.00, "Sep PODs": 4, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "AZ", "YTD Cases": 57.16, "YTD PODs": 29, "Apr Cases": 10.08, "Apr PODs": 6, "May Cases": 0, "May PODs": 0, "Jun Cases": 8.50, "Jun PODs": 8, "Jul Cases": 4.08, "Jul PODs": 3, "Aug Cases": 4.00, "Aug PODs": 3, "Sep Cases": 4.08, "Sep PODs": 4, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 2, "New Oct PODs": 0},
    {"State": "CO", "YTD Cases": 51.83, "YTD PODs": 17, "Apr Cases": 5.00, "Apr PODs": 3, "May Cases": 11.33, "May PODs": 7, "Jun Cases": 9.00, "Jun PODs": 7, "Jul Cases": 9.50, "Jul PODs": 7, "Aug Cases": 5.50, "Aug PODs": 6, "Sep Cases": 6.00, "Sep PODs": 5, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 2, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "MA", "YTD Cases": 33.08, "YTD PODs": 10, "Apr Cases": 5.00, "Apr PODs": 2, "May Cases": 2.08, "May PODs": 3, "Jun Cases": 12.00, "Jun PODs": 7, "Jul Cases": 1.00, "Jul PODs": 1, "Aug Cases": 7.00, "Aug PODs": 5, "Sep Cases": 6.00, "Sep PODs": 3, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "VA", "YTD Cases": 29.50, "YTD PODs": 13, "Apr Cases": 3.00, "Apr PODs": 2, "May Cases": 8.50, "May PODs": 4, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 0, "Jul PODs": 0, "Aug Cases": 7.00, "Aug PODs": 3, "Sep Cases": 6.00, "Sep PODs": 1, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 2, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "WA", "YTD Cases": 24.16, "YTD PODs": 6, "Apr Cases": 0.16, "Apr PODs": 2, "May Cases": 4.00, "May PODs": 3, "Jun Cases": 3.00, "Jun PODs": 2, "Jul Cases": 1.00, "Jul PODs": 1, "Aug Cases": 3.00, "Aug PODs": 3, "Sep Cases": 12.00, "Sep PODs": 3, "Oct Cases": 1.00, "Oct PODs": 1, "New Aug PODs": 1, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "NC", "YTD Cases": 23.33, "YTD PODs": 12, "Apr Cases": 6.00, "Apr PODs": 4, "May Cases": 2.33, "May PODs": 5, "Jun Cases": 1.00, "Jun PODs": 3, "Jul Cases": 4.50, "Jul PODs": 6, "Aug Cases": 4.08, "Aug PODs": 5, "Sep Cases": 5.42, "Sep PODs": 4, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 2, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "MI", "YTD Cases": 17.25, "YTD PODs": 9, "Apr Cases": 4.58, "Apr PODs": 4, "May Cases": 2.67, "May PODs": 3, "Jun Cases": 5.50, "Jun PODs": 5, "Jul Cases": 2.00, "Jul PODs": 2, "Aug Cases": 1.50, "Aug PODs": 2, "Sep Cases": 0, "Sep PODs": 0, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "MD", "YTD Cases": 16.50, "YTD PODs": 7, "Apr Cases": 5.00, "Apr PODs": 2, "May Cases": 1.33, "May PODs": 2, "Jun Cases": 3.08, "Jun PODs": 3, "Jul Cases": 0, "Jul PODs": 0, "Aug Cases": 1.33, "Aug PODs": 2, "Sep Cases": 2.17, "Sep PODs": 2, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "OH", "YTD Cases": 16.32, "YTD PODs": 10, "Apr Cases": 1.25, "Apr PODs": 3, "May Cases": 0.58, "May PODs": 2, "Jun Cases": 2.00, "Jun PODs": 2, "Jul Cases": 3.08, "Jul PODs": 3, "Aug Cases": 1.25, "Aug PODs": 2, "Sep Cases": 2.42, "Sep PODs": 3, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "KY", "YTD Cases": 13.00, "YTD PODs": 8, "Apr Cases": 3.00, "Apr PODs": 1, "May Cases": 1.00, "May PODs": 1, "Jun Cases": 3.00, "Jun PODs": 3, "Jul Cases": 3.00, "Jul PODs": 2, "Aug Cases": 1.00, "Aug PODs": 1, "Sep Cases": 1.00, "Sep PODs": 1, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 1, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "GA", "YTD Cases": 11.50, "YTD PODs": 5, "Apr Cases": 0.50, "Apr PODs": 1, "May Cases": 2.00, "May PODs": 1, "Jun Cases": 1.00, "Jun PODs": 2, "Jul Cases": 3.00, "Jul PODs": 2, "Aug Cases": 3.00, "Aug PODs": 1, "Sep Cases": 2.00, "Sep PODs": 1, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "DE", "YTD Cases": 11.00, "YTD PODs": 3, "Apr Cases": 1.00, "Apr PODs": 1, "May Cases": 1.00, "May PODs": 1, "Jun Cases": 1.00, "Jun PODs": 1, "Jul Cases": 5.00, "Jul PODs": 3, "Aug Cases": 1.00, "Aug PODs": 1, "Sep Cases": 1.00, "Sep PODs": 1, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "CT", "YTD Cases": 8.00, "YTD PODs": 5, "Apr Cases": 2.00, "Apr PODs": 2, "May Cases": 0, "May PODs": 0, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 2.00, "Jul PODs": 2, "Aug Cases": 1.00, "Aug PODs": 1, "Sep Cases": 2.00, "Sep PODs": 2, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "NM", "YTD Cases": 7.17, "YTD PODs": 7, "Apr Cases": 1.17, "Apr PODs": 2, "May Cases": 1.25, "May PODs": 2, "Jun Cases": 1.00, "Jun PODs": 1, "Jul Cases": 1.50, "Jul PODs": 2, "Aug Cases": 2.25, "Aug PODs": 3, "Sep Cases": 0, "Sep PODs": 0, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 2, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "DC", "YTD Cases": 7.00, "YTD PODs": 1, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 3.00, "May PODs": 1, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 0, "Jul PODs": 0, "Aug Cases": 1.00, "Aug PODs": 1, "Sep Cases": 2.00, "Sep PODs": 1, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "IN", "YTD Cases": 6.17, "YTD PODs": 3, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 1.00, "May PODs": 1, "Jun Cases": 1.00, "Jun PODs": 1, "Jul Cases": 2.00, "Jul PODs": 2, "Aug Cases": 0, "Aug PODs": 0, "Sep Cases": 2.17, "Sep PODs": 2, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "MO", "YTD Cases": 6.17, "YTD PODs": 4, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 0, "May PODs": 0, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 3.17, "Jul PODs": 1, "Aug Cases": 1.00, "Aug PODs": 1, "Sep Cases": 2.00, "Sep PODs": 2, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 1, "New Sep PODs": 2, "New Oct PODs": 0},
    {"State": "SC", "YTD Cases": 5.00, "YTD PODs": 4, "Apr Cases": 0.50, "Apr PODs": 1, "May Cases": 0, "May PODs": 0, "Jun Cases": 1.00, "Jun PODs": 1, "Jul Cases": 1.50, "Jul PODs": 2, "Aug Cases": 1.00, "Aug PODs": 1, "Sep Cases": 1.00, "Sep PODs": 1, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "MN", "YTD Cases": 1.00, "YTD PODs": 1, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 0, "May PODs": 0, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 0, "Jul PODs": 0, "Aug Cases": 0, "Aug PODs": 0, "Sep Cases": 0, "Sep PODs": 0, "Oct Cases": 1.00, "Oct PODs": 1, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 1},
    {"State": "ME", "YTD Cases": 0.75, "YTD PODs": 1, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 0, "May PODs": 0, "Jun Cases": 0.25, "Jun PODs": 1, "Jul Cases": 0.17, "Jul PODs": 1, "Aug Cases": 0.17, "Aug PODs": 1, "Sep Cases": 0.17, "Sep PODs": 1, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
])

# OFF-PREMISE state data (from latest depletion tab, tight scrub applied)
off_states = pd.DataFrame([
    {"State": "CA", "YTD Cases": 964.99, "YTD PODs": 263, "Apr Cases": 89.75, "Apr PODs": 47, "May Cases": 82.33, "May PODs": 48, "Jun Cases": 108.34, "Jun PODs": 55, "Jul Cases": 116.24, "Jul PODs": 67, "Aug Cases": 83.92, "Aug PODs": 60, "Sep Cases": 110.58, "Sep PODs": 57, "Oct Cases": 11.33, "Oct PODs": 2, "New Aug PODs": 4, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "NY", "YTD Cases": 435.00, "YTD PODs": 118, "Apr Cases": 28.00, "Apr PODs": 16, "May Cases": 26.00, "May PODs": 16, "Jun Cases": 50.08, "Jun PODs": 34, "Jul Cases": 62.58, "Jul PODs": 36, "Aug Cases": 47.00, "Aug PODs": 27, "Sep Cases": 89.17, "Sep PODs": 29, "Oct Cases": 4.00, "Oct PODs": 4, "New Aug PODs": 7, "New Sep PODs": 8, "New Oct PODs": 1},
    {"State": "NJ", "YTD Cases": 382.83, "YTD PODs": 91, "Apr Cases": 17.50, "Apr PODs": 10, "May Cases": 23.08, "May PODs": 20, "Jun Cases": 42.58, "Jun PODs": 30, "Jul Cases": 47.34, "Jul PODs": 26, "Aug Cases": 26.75, "Aug PODs": 20, "Sep Cases": 30.25, "Sep PODs": 25, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 1, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "FL", "YTD Cases": 333.02, "YTD PODs": 79, "Apr Cases": 26.35, "Apr PODs": 18, "May Cases": 80.91, "May PODs": 31, "Jun Cases": 23.09, "Jun PODs": 22, "Jul Cases": 33.10, "Jul PODs": 28, "Aug Cases": 25.08, "Aug PODs": 20, "Sep Cases": 25.75, "Sep PODs": 14, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 3, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "IL", "YTD Cases": 304.98, "YTD PODs": 86, "Apr Cases": 24.08, "Apr PODs": 21, "May Cases": 30.00, "May PODs": 27, "Jun Cases": 24.00, "Jun PODs": 19, "Jul Cases": 71.08, "Jul PODs": 34, "Aug Cases": 20.00, "Aug PODs": 18, "Sep Cases": 29.00, "Sep PODs": 26, "Oct Cases": 1.00, "Oct PODs": 1, "New Aug PODs": 2, "New Sep PODs": 2, "New Oct PODs": 0},
    {"State": "NC", "YTD Cases": 247.09, "YTD PODs": 191, "Apr Cases": 7.83, "Apr PODs": 21, "May Cases": 41.50, "May PODs": 69, "Jun Cases": 41.67, "Jun PODs": 73, "Jul Cases": 43.16, "Jul PODs": 62, "Aug Cases": 37.84, "Aug PODs": 54, "Sep Cases": 42.32, "Sep PODs": 50, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 10, "New Sep PODs": 9, "New Oct PODs": 0},
    {"State": "TX", "YTD Cases": 156.85, "YTD PODs": 50, "Apr Cases": 11.33, "Apr PODs": 11, "May Cases": 17.67, "May PODs": 20, "Jun Cases": 24.51, "Jun PODs": 20, "Jul Cases": 36.25, "Jul PODs": 21, "Aug Cases": 10.00, "Aug PODs": 8, "Sep Cases": 28.00, "Sep PODs": 10, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 8, "New Sep PODs": 5, "New Oct PODs": 0},
    {"State": "VA", "YTD Cases": 117.42, "YTD PODs": 115, "Apr Cases": 5.50, "Apr PODs": 9, "May Cases": 15.34, "May PODs": 25, "Jun Cases": 12.50, "Jun PODs": 20, "Jul Cases": 1.50, "Jul PODs": 3, "Aug Cases": 22.00, "Aug PODs": 31, "Sep Cases": 11.00, "Sep PODs": 11, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 9, "New Sep PODs": 11, "New Oct PODs": 0},
    {"State": "SC", "YTD Cases": 108.59, "YTD PODs": 78, "Apr Cases": 5.25, "Apr PODs": 6, "May Cases": 25.99, "May PODs": 40, "Jun Cases": 30.20, "Jun PODs": 27, "Jul Cases": 9.43, "Jul PODs": 18, "Aug Cases": 8.51, "Aug PODs": 11, "Sep Cases": 20.67, "Sep PODs": 13, "Oct Cases": 0.25, "Oct PODs": 1, "New Aug PODs": 1, "New Sep PODs": 3, "New Oct PODs": 0},
    {"State": "MA", "YTD Cases": 101.75, "YTD PODs": 25, "Apr Cases": 7.00, "Apr PODs": 6, "May Cases": 18.75, "May PODs": 15, "Jun Cases": 27.00, "Jun PODs": 11, "Jul Cases": 22.00, "Jul PODs": 9, "Aug Cases": 15.08, "Aug PODs": 7, "Sep Cases": 11.92, "Sep PODs": 5, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "CT", "YTD Cases": 72.50, "YTD PODs": 33, "Apr Cases": 8.17, "Apr PODs": 8, "May Cases": 6.00, "May PODs": 5, "Jun Cases": 6.75, "Jun PODs": 8, "Jul Cases": 8.42, "Jul PODs": 8, "Aug Cases": 1.00, "Aug PODs": 1, "Sep Cases": 9.00, "Sep PODs": 6, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 1, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "MI", "YTD Cases": 58.84, "YTD PODs": 29, "Apr Cases": 21.34, "Apr PODs": 22, "May Cases": 3.25, "May PODs": 4, "Jun Cases": 6.75, "Jun PODs": 7, "Jul Cases": 8.92, "Jul PODs": 10, "Aug Cases": 12.50, "Aug PODs": 10, "Sep Cases": 0, "Sep PODs": 0, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "WA", "YTD Cases": 46.58, "YTD PODs": 23, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 6.00, "May PODs": 3, "Jun Cases": 6.00, "Jun PODs": 3, "Jul Cases": 1.00, "Jul PODs": 1, "Aug Cases": 4.25, "Aug PODs": 5, "Sep Cases": 28.33, "Sep PODs": 22, "Oct Cases": 1.00, "Oct PODs": 1, "New Aug PODs": 3, "New Sep PODs": 15, "New Oct PODs": 1},
    {"State": "OH", "YTD Cases": 38.75, "YTD PODs": 14, "Apr Cases": 4.25, "Apr PODs": 6, "May Cases": 2.75, "May PODs": 4, "Jun Cases": 6.42, "Jun PODs": 5, "Jul Cases": 4.25, "Jul PODs": 7, "Aug Cases": 1.58, "Aug PODs": 2, "Sep Cases": 5.08, "Sep PODs": 8, "Oct Cases": 0.33, "Oct PODs": 1, "New Aug PODs": 0, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "KY", "YTD Cases": 36.00, "YTD PODs": 8, "Apr Cases": 1.00, "Apr PODs": 1, "May Cases": 6.00, "May PODs": 4, "Jun Cases": 17.00, "Jun PODs": 3, "Jul Cases": 6.00, "Jul PODs": 4, "Aug Cases": 1.00, "Aug PODs": 1, "Sep Cases": 2.00, "Sep PODs": 2, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 1, "New Sep PODs": 2, "New Oct PODs": 0},
    {"State": "CO", "YTD Cases": 30.50, "YTD PODs": 19, "Apr Cases": 2.08, "Apr PODs": 3, "May Cases": 4.00, "May PODs": 3, "Jun Cases": 5.00, "Jun PODs": 3, "Jul Cases": 9.42, "Jul PODs": 10, "Aug Cases": 6.00, "Aug PODs": 4, "Sep Cases": 1.00, "Sep PODs": 1, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 1, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "MD", "YTD Cases": 30.50, "YTD PODs": 15, "Apr Cases": 4.00, "Apr PODs": 4, "May Cases": 3.00, "May PODs": 3, "Jun Cases": 1.00, "Jun PODs": 1, "Jul Cases": 4.00, "Jul PODs": 4, "Aug Cases": 3.00, "Aug PODs": 3, "Sep Cases": 2.00, "Sep PODs": 2, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "DE", "YTD Cases": 28.00, "YTD PODs": 16, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 1.00, "May PODs": 1, "Jun Cases": 5.00, "Jun PODs": 2, "Jul Cases": 0, "Jul PODs": 0, "Aug Cases": 1.00, "Aug PODs": 1, "Sep Cases": 0, "Sep PODs": 0, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "AZ", "YTD Cases": 19.50, "YTD PODs": 6, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 2.00, "May PODs": 2, "Jun Cases": 5.00, "Jun PODs": 2, "Jul Cases": 2.50, "Jul PODs": 3, "Aug Cases": 6.00, "Aug PODs": 4, "Sep Cases": 3.00, "Sep PODs": 3, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 1, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "GA", "YTD Cases": 18.84, "YTD PODs": 9, "Apr Cases": 7.00, "Apr PODs": 2, "May Cases": 1.00, "May PODs": 1, "Jun Cases": 3.00, "Jun PODs": 2, "Jul Cases": 1.00, "Jul PODs": 1, "Aug Cases": 2.00, "Aug PODs": 2, "Sep Cases": 1.84, "Sep PODs": 3, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 2, "New Oct PODs": 0},
    {"State": "DC", "YTD Cases": 12.00, "YTD PODs": 6, "Apr Cases": 4.00, "Apr PODs": 3, "May Cases": 2.00, "May PODs": 2, "Jun Cases": 2.00, "Jun PODs": 2, "Jul Cases": 0, "Jul PODs": 0, "Aug Cases": 1.00, "Aug PODs": 1, "Sep Cases": 2.00, "Sep PODs": 2, "Oct Cases": 1.00, "Oct PODs": 1, "New Aug PODs": 0, "New Sep PODs": 1, "New Oct PODs": 1},
    {"State": "NM", "YTD Cases": 11.75, "YTD PODs": 7, "Apr Cases": 0.08, "Apr PODs": 1, "May Cases": 0.17, "May PODs": 1, "Jun Cases": 3.58, "Jun PODs": 3, "Jul Cases": 4.58, "Jul PODs": 4, "Aug Cases": 1.00, "Aug PODs": 1, "Sep Cases": 2.33, "Sep PODs": 3, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 1, "New Sep PODs": 2, "New Oct PODs": 0},
    {"State": "NV", "YTD Cases": 11.00, "YTD PODs": 4, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 2.00, "May PODs": 2, "Jun Cases": 2.00, "Jun PODs": 2, "Jul Cases": 2.00, "Jul PODs": 2, "Aug Cases": 4.00, "Aug PODs": 3, "Sep Cases": 1.00, "Sep PODs": 1, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 1, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "MN", "YTD Cases": 10.85, "YTD PODs": 8, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 0, "May PODs": 0, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 4.17, "Jul PODs": 4, "Aug Cases": 3.51, "Aug PODs": 3, "Sep Cases": 3.17, "Sep PODs": 3, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 3, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "IN", "YTD Cases": 10.41, "YTD PODs": 5, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 2.08, "May PODs": 2, "Jun Cases": 0.08, "Jun PODs": 1, "Jul Cases": 5.00, "Jul PODs": 2, "Aug Cases": 1.25, "Aug PODs": 2, "Sep Cases": 2.00, "Sep PODs": 2, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 1, "New Sep PODs": 2, "New Oct PODs": 0},
    {"State": "LA", "YTD Cases": 8.00, "YTD PODs": 8, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 0, "May PODs": 0, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 0, "Jul PODs": 0, "Aug Cases": 0, "Aug PODs": 0, "Sep Cases": 8.00, "Sep PODs": 8, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 8, "New Oct PODs": 0},
    {"State": "MO", "YTD Cases": 7.25, "YTD PODs": 4, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 1.00, "May PODs": 1, "Jun Cases": 1.00, "Jun PODs": 1, "Jul Cases": 1.00, "Jul PODs": 1, "Aug Cases": 2.25, "Aug PODs": 3, "Sep Cases": 2.00, "Sep PODs": 2, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 3, "New Sep PODs": 0, "New Oct PODs": 0},
    {"State": "ME", "YTD Cases": 3.17, "YTD PODs": 2, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 1.00, "May PODs": 1, "Jun Cases": 0.58, "Jun PODs": 1, "Jul Cases": 0.25, "Jul PODs": 1, "Aug Cases": 0.33, "Aug PODs": 1, "Sep Cases": 1.00, "Sep PODs": 1, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 1, "New Oct PODs": 0},
    {"State": "NE", "YTD Cases": 0.50, "YTD PODs": 1, "Apr Cases": 0, "Apr PODs": 0, "May Cases": 0, "May PODs": 0, "Jun Cases": 0, "Jun PODs": 0, "Jul Cases": 0.50, "Jul PODs": 1, "Aug Cases": 0, "Aug PODs": 0, "Sep Cases": 0, "Sep PODs": 0, "Oct Cases": 0, "Oct PODs": 0, "New Aug PODs": 0, "New Sep PODs": 0, "New Oct PODs": 0},
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
    {"Month": "Jun '26", "Cases": 520},
    {"Month": "Jul '26", "Cases": 691},
])

# Top accounts — chain data from Ethica 05.11.26 (samples removed)
top_accounts = pd.DataFrame([
    {"Account": "Total Wine & More", "Premise": "Off", "States": "Multi", "YTD Cases": 562.61, "YTD PODs": 140, "Apr Cases": 35.93, "May Cases": 85.99, "Jun Cases": 127.93, "Jul Cases": 93.60, "Aug Cases": 67.50, "Sep Cases": 78.42, "Oct Cases": 2.00},
    {"Account": "Eataly", "Premise": "On", "States": "CA, FL, IL, MA, NJ, NY, TX", "YTD Cases": 368.08, "YTD PODs": 15, "Apr Cases": 46.00, "May Cases": 60.00, "Jun Cases": 48.00, "Jul Cases": 65.00, "Aug Cases": 23.00, "Sep Cases": 47.08, "Oct Cases": 3.00},
    {"Account": "BevMo!", "Premise": "Off", "States": "CA", "YTD Cases": 330.00, "YTD PODs": 145, "Apr Cases": 9.00, "May Cases": 18.00, "Jun Cases": 36.00, "Jul Cases": 54.00, "Aug Cases": 33.00, "Sep Cases": 29.00, "Oct Cases": 0},
    {"Account": "Food Lion", "Premise": "Off", "States": "NC, SC, VA", "YTD Cases": 223.67, "YTD PODs": 305, "Apr Cases": 6.83, "May Cases": 43.75, "Jun Cases": 42.87, "Jul Cases": 21.42, "Aug Cases": 22.93, "Sep Cases": 12.08, "Oct Cases": 0.25},
    {"Account": "Binny's", "Premise": "Off", "States": "IL", "YTD Cases": 193.74, "YTD PODs": 43, "Apr Cases": 14.08, "May Cases": 29.00, "Jun Cases": 17.00, "Jul Cases": 56.08, "Aug Cases": 16.00, "Sep Cases": 18.00, "Oct Cases": 1.00},
    {"Account": "Wine.com", "Premise": "Off", "States": "CA, MA, NJ, NY, OH, TX", "YTD Cases": 169.92, "YTD PODs": 8, "Apr Cases": 15.00, "May Cases": 8.00, "Jun Cases": 19.00, "Jul Cases": 20.00, "Aug Cases": 19.00, "Sep Cases": 54.92, "Oct Cases": 0},
    {"Account": "Albertsons Warehouse", "Premise": "Off", "States": "CA", "YTD Cases": 133.00, "YTD PODs": 1, "Apr Cases": 22.00, "May Cases": 11.00, "Jun Cases": 11.00, "Jul Cases": 11.00, "Aug Cases": 11.00, "Sep Cases": 22.00, "Oct Cases": 0},
    {"Account": "Trader Joe's", "Premise": "Off", "States": "KY, NC, SC", "YTD Cases": 132.00, "YTD PODs": 17, "Apr Cases": 2.00, "May Cases": 23.00, "Jun Cases": 29.00, "Jul Cases": 25.00, "Aug Cases": 25.00, "Sep Cases": 28.00, "Oct Cases": 0},
    {"Account": "Gary's Wine", "Premise": "Off", "States": "NJ", "YTD Cases": 77.00, "YTD PODs": 3, "Apr Cases": 1.00, "May Cases": 1.00, "Jun Cases": 1.00, "Jul Cases": 0, "Aug Cases": 1.00, "Sep Cases": 0, "Oct Cases": 0},
    {"Account": "Milam's Markets", "Premise": "Off", "States": "FL", "YTD Cases": 72.00, "YTD PODs": 6, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"Account": "Stew Leonard's Wines", "Premise": "Off", "States": "CT, NY", "YTD Cases": 57.00, "YTD PODs": 5, "Apr Cases": 2.00, "May Cases": 1.00, "Jun Cases": 1.00, "Jul Cases": 3.00, "Aug Cases": 1.00, "Sep Cases": 2.00, "Oct Cases": 0},
    {"Account": "Trader Joe's Warehouse", "Premise": "Off", "States": "FL", "YTD Cases": 56.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 56.00, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"Account": "Stew Leonard's", "Premise": "Off", "States": "NJ", "YTD Cases": 42.00, "YTD PODs": 2, "Apr Cases": 4.00, "May Cases": 1.00, "Jun Cases": 3.00, "Jul Cases": 2.00, "Aug Cases": 3.00, "Sep Cases": 0, "Oct Cases": 0},
    {"Account": "Capital One Lounge", "Premise": "On", "States": "CO, NV, NY, VA", "YTD Cases": 28.17, "YTD PODs": 4, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 28.17, "Oct Cases": 0},
    {"Account": "H-E-B Central Market", "Premise": "Off", "States": "TX", "YTD Cases": 27.42, "YTD PODs": 10, "Apr Cases": 2.25, "May Cases": 4.00, "Jun Cases": 2.00, "Jul Cases": 8.00, "Aug Cases": 6.00, "Sep Cases": 4.00, "Oct Cases": 0},
    {"Account": "Harris Teeter", "Premise": "Off", "States": "FL, NC, SC", "YTD Cases": 26.19, "YTD PODs": 20, "Apr Cases": 0.25, "May Cases": 0.50, "Jun Cases": 3.33, "Jul Cases": 4.01, "Aug Cases": 4.59, "Sep Cases": 13.49, "Oct Cases": 0},
    {"Account": "Bottle King", "Premise": "Off", "States": "NJ", "YTD Cases": 26.00, "YTD PODs": 12, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 12.00, "Jul Cases": 7.00, "Aug Cases": 1.00, "Sep Cases": 6.00, "Oct Cases": 0},
    {"Account": "Trader Joe's Liquor", "Premise": "Off", "States": "KY", "YTD Cases": 23.00, "YTD PODs": 3, "Apr Cases": 0, "May Cases": 4.00, "Jun Cases": 16.00, "Jul Cases": 2.00, "Aug Cases": 1.00, "Sep Cases": 0, "Oct Cases": 0},
    {"Account": "Haggen Food & Pharmacy", "Premise": "Off", "States": "WA", "YTD Cases": 22.00, "YTD PODs": 14, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 1.00, "Sep Cases": 21.00, "Oct Cases": 0},
    {"Account": "VIN Chicago", "Premise": "Off", "States": "IL", "YTD Cases": 20.16, "YTD PODs": 2, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"Account": "BevMax", "Premise": "Off", "States": "CT", "YTD Cases": 18.00, "YTD PODs": 12, "Apr Cases": 3.00, "May Cases": 1.00, "Jun Cases": 2.00, "Jul Cases": 2.00, "Aug Cases": 1.00, "Sep Cases": 0, "Oct Cases": 0},
    {"Account": "ShopRite Liquors", "Premise": "Off", "States": "NJ", "YTD Cases": 16.00, "YTD PODs": 6, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 1.00, "Sep Cases": 2.00, "Oct Cases": 0},
    {"Account": "Oliver's Market", "Premise": "Off", "States": "CA", "YTD Cases": 15.00, "YTD PODs": 4, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 0, "Sep Cases": 2.00, "Oct Cases": 0},
    {"Account": "Spec's Wine & Spirits", "Premise": "Off", "States": "TX", "YTD Cases": 14.00, "YTD PODs": 8, "Apr Cases": 2.00, "May Cases": 0, "Jun Cases": 3.00, "Jul Cases": 1.00, "Aug Cases": 1.00, "Sep Cases": 0, "Oct Cases": 0},
    {"Account": "Eataly", "Premise": "Off", "States": "MA", "YTD Cases": 14.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 2.00, "Jun Cases": 5.00, "Jul Cases": 2.00, "Aug Cases": 3.00, "Sep Cases": 2.00, "Oct Cases": 0},
])

# State-level top accounts for key 6 states (CA, TX, FL, NY, NJ, IL) — as of 7/31/26 (samples removed)
state_top_accounts = pd.DataFrame([
    # CA
    {"State": "CA", "Account": "BevMo!", "Premise": "Off", "YTD Cases": 330.00, "YTD PODs": 145, "Apr Cases": 9.00, "May Cases": 18.00, "Jun Cases": 36.00, "Jul Cases": 54.00, "Aug Cases": 33.00, "Sep Cases": 29.00, "Oct Cases": 0},
    {"State": "CA", "Account": "Albertsons Warehouse", "Premise": "Off", "YTD Cases": 133.00, "YTD PODs": 1, "Apr Cases": 22.00, "May Cases": 11.00, "Jun Cases": 11.00, "Jul Cases": 11.00, "Aug Cases": 11.00, "Sep Cases": 22.00, "Oct Cases": 0},
    {"State": "CA", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 91.08, "YTD PODs": 15, "Apr Cases": 5.00, "May Cases": 11.00, "Jun Cases": 35.08, "Jul Cases": 6.00, "Aug Cases": 7.00, "Sep Cases": 16.00, "Oct Cases": 0},
    {"State": "CA", "Account": "Eataly", "Premise": "On", "YTD Cases": 74.00, "YTD PODs": 2, "Apr Cases": 4.00, "May Cases": 14.00, "Jun Cases": 9.00, "Jul Cases": 8.00, "Aug Cases": 6.00, "Sep Cases": 13.00, "Oct Cases": 2.00},
    {"State": "CA", "Account": "Wine.com", "Premise": "Off", "YTD Cases": 27.00, "YTD PODs": 2, "Apr Cases": 5.00, "May Cases": 2.00, "Jun Cases": 4.00, "Jul Cases": 4.00, "Aug Cases": 3.00, "Sep Cases": 2.00, "Oct Cases": 0},
    {"State": "CA", "Account": "Oliver's Market", "Premise": "Off", "YTD Cases": 15.00, "YTD PODs": 4, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 0, "Sep Cases": 2.00, "Oct Cases": 0},
    {"State": "CA", "Account": "Sodexo Live!", "Premise": "On", "YTD Cases": 13.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 3.00, "Jun Cases": 0, "Jul Cases": 3.00, "Aug Cases": 5.00, "Sep Cases": 2.00, "Oct Cases": 0},
    {"State": "CA", "Account": "Buona Forchetta", "Premise": "On", "YTD Cases": 11.00, "YTD PODs": 4, "Apr Cases": 0, "May Cases": 9.00, "Jun Cases": 0, "Jul Cases": 2.00, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "CA", "Account": "Troon Golf", "Premise": "On", "YTD Cases": 3.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 2.00, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "CA", "Account": "ClubProcure", "Premise": "On", "YTD Cases": 3.00, "YTD PODs": 2, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 2.00, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "CA", "Account": "Invited", "Premise": "On", "YTD Cases": 3.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "CA", "Account": "Waldorf Collection", "Premise": "On", "YTD Cases": 2.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 2.00, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "CA", "Account": "Mission Wine & Spirits", "Premise": "Off", "YTD Cases": 2.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 1.00, "Oct Cases": 0},
    # TX
    {"State": "TX", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 60.43, "YTD PODs": 19, "Apr Cases": 1.08, "May Cases": 10.67, "Jun Cases": 14.51, "Jul Cases": 25.17, "Aug Cases": 0, "Sep Cases": 3.00, "Oct Cases": 0},
    {"State": "TX", "Account": "Eataly", "Premise": "On", "YTD Cases": 35.00, "YTD PODs": 4, "Apr Cases": 7.00, "May Cases": 5.00, "Jun Cases": 4.00, "Jul Cases": 6.00, "Aug Cases": 2.00, "Sep Cases": 7.00, "Oct Cases": 0},
    {"State": "TX", "Account": "H-E-B Central Market", "Premise": "Off", "YTD Cases": 27.42, "YTD PODs": 10, "Apr Cases": 2.25, "May Cases": 4.00, "Jun Cases": 2.00, "Jul Cases": 8.00, "Aug Cases": 6.00, "Sep Cases": 4.00, "Oct Cases": 0},
    {"State": "TX", "Account": "Wine.com", "Premise": "Off", "YTD Cases": 20.00, "YTD PODs": 2, "Apr Cases": 3.00, "May Cases": 2.00, "Jun Cases": 2.00, "Jul Cases": 0, "Aug Cases": 1.00, "Sep Cases": 7.00, "Oct Cases": 0},
    {"State": "TX", "Account": "Spec's Wine & Spirits", "Premise": "Off", "YTD Cases": 14.00, "YTD PODs": 8, "Apr Cases": 2.00, "May Cases": 0, "Jun Cases": 3.00, "Jul Cases": 1.00, "Aug Cases": 1.00, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "TX", "Account": "Spec's Wholesale", "Premise": "Off", "YTD Cases": 12.17, "YTD PODs": 4, "Apr Cases": 2.00, "May Cases": 1.00, "Jun Cases": 2.00, "Jul Cases": 1.00, "Aug Cases": 2.00, "Sep Cases": 1.00, "Oct Cases": 0},
    {"State": "TX", "Account": "Specs Warehouse", "Premise": "Off", "YTD Cases": 12.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 12.00, "Oct Cases": 0},
    {"State": "TX", "Account": "Miraval", "Premise": "On", "YTD Cases": 4.00, "YTD PODs": 1, "Apr Cases": 2.00, "May Cases": 0, "Jun Cases": 2.00, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "TX", "Account": "Liquorland", "Premise": "Off", "YTD Cases": 3.00, "YTD PODs": 2, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "TX", "Account": "Royal Blue Grocery", "Premise": "On", "YTD Cases": 1.00, "YTD PODs": 1, "Apr Cases": 1.00, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    # FL
    {"State": "FL", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 102.02, "YTD PODs": 30, "Apr Cases": 4.68, "May Cases": 16.41, "Jun Cases": 18.59, "Jul Cases": 16.51, "Aug Cases": 12.50, "Sep Cases": 16.42, "Oct Cases": 0},
    {"State": "FL", "Account": "Milam's Markets", "Premise": "Off", "YTD Cases": 72.00, "YTD PODs": 6, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "FL", "Account": "Trader Joe's Warehouse", "Premise": "Off", "YTD Cases": 56.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 56.00, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "FL", "Account": "Eataly", "Premise": "On", "YTD Cases": 15.00, "YTD PODs": 2, "Apr Cases": 0, "May Cases": 2.00, "Jun Cases": 2.00, "Jul Cases": 3.00, "Aug Cases": 3.00, "Sep Cases": 2.00, "Oct Cases": 0},
    {"State": "FL", "Account": "Gopuff", "Premise": "Off", "YTD Cases": 12.00, "YTD PODs": 6, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 1.00, "Jul Cases": 2.00, "Aug Cases": 2.00, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "FL", "Account": "Amex Centurion Lounge", "Premise": "On", "YTD Cases": 8.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 6.00, "Aug Cases": 2.00, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "FL", "Account": "Shores", "Premise": "Off", "YTD Cases": 4.00, "YTD PODs": 4, "Apr Cases": 4.00, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "FL", "Account": "Doris Italian Market", "Premise": "Off", "YTD Cases": 3.17, "YTD PODs": 1, "Apr Cases": 1.00, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0.17, "Aug Cases": 1.00, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "FL", "Account": "Soho House", "Premise": "On", "YTD Cases": 1.83, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "FL", "Account": "Bice Ristorante", "Premise": "On", "YTD Cases": 1.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "FL", "Account": "Harris Teeter", "Premise": "Off", "YTD Cases": 0.42, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0.42, "Sep Cases": 0, "Oct Cases": 0},
    # NY
    {"State": "NY", "Account": "Wine.com", "Premise": "Off", "YTD Cases": 86.00, "YTD PODs": 1, "Apr Cases": 5.00, "May Cases": 3.00, "Jun Cases": 5.00, "Jul Cases": 13.00, "Aug Cases": 10.00, "Sep Cases": 36.00, "Oct Cases": 0},
    {"State": "NY", "Account": "Eataly", "Premise": "On", "YTD Cases": 82.00, "YTD PODs": 4, "Apr Cases": 9.00, "May Cases": 19.00, "Jun Cases": 10.00, "Jul Cases": 19.00, "Aug Cases": 2.00, "Sep Cases": 12.00, "Oct Cases": 0},
    {"State": "NY", "Account": "Stew Leonard's Wines", "Premise": "Off", "YTD Cases": 33.00, "YTD PODs": 2, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 1.00, "Sep Cases": 1.00, "Oct Cases": 0},
    {"State": "NY", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 22.00, "YTD PODs": 1, "Apr Cases": 3.00, "May Cases": 2.00, "Jun Cases": 4.00, "Jul Cases": 5.00, "Aug Cases": 2.00, "Sep Cases": 2.00, "Oct Cases": 1.00},
    {"State": "NY", "Account": "Capital One Lounge", "Premise": "On", "YTD Cases": 14.17, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 14.17, "Oct Cases": 0},
    {"State": "NY", "Account": "Moxy Hotels", "Premise": "On", "YTD Cases": 13.00, "YTD PODs": 2, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 11.00, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 2.00, "Oct Cases": 0},
    {"State": "NY", "Account": "Freehand", "Premise": "On", "YTD Cases": 11.00, "YTD PODs": 1, "Apr Cases": 2.00, "May Cases": 2.00, "Jun Cases": 2.00, "Jul Cases": 1.00, "Aug Cases": 2.00, "Sep Cases": 1.00, "Oct Cases": 0},
    {"State": "NY", "Account": "Hilton", "Premise": "On", "YTD Cases": 2.00, "YTD PODs": 2, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 1.00, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "NY", "Account": "1 Hotel", "Premise": "On", "YTD Cases": 1.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 1.00},
    {"State": "NY", "Account": "ClubProcure", "Premise": "On", "YTD Cases": 1.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    # NJ
    {"State": "NJ", "Account": "Gary's Wine & Marketplace", "Premise": "Off", "YTD Cases": 77.00, "YTD PODs": 3, "Apr Cases": 1.00, "May Cases": 1.00, "Jun Cases": 1.00, "Jul Cases": 0, "Aug Cases": 1.00, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "NJ", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 44.00, "YTD PODs": 7, "Apr Cases": 2.00, "May Cases": 8.00, "Jun Cases": 7.00, "Jul Cases": 8.00, "Aug Cases": 2.00, "Sep Cases": 7.00, "Oct Cases": 0},
    {"State": "NJ", "Account": "Stew Leonard's", "Premise": "Off", "YTD Cases": 42.00, "YTD PODs": 2, "Apr Cases": 4.00, "May Cases": 1.00, "Jun Cases": 3.00, "Jul Cases": 2.00, "Aug Cases": 3.00, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "NJ", "Account": "Eataly", "Premise": "On", "YTD Cases": 33.08, "YTD PODs": 1, "Apr Cases": 2.00, "May Cases": 4.00, "Jun Cases": 4.00, "Jul Cases": 6.00, "Aug Cases": 4.00, "Sep Cases": 4.08, "Oct Cases": 1.00},
    {"State": "NJ", "Account": "Bottle King", "Premise": "Off", "YTD Cases": 26.00, "YTD PODs": 12, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 12.00, "Jul Cases": 7.00, "Aug Cases": 1.00, "Sep Cases": 6.00, "Oct Cases": 0},
    {"State": "NJ", "Account": "Wine.com", "Premise": "Off", "YTD Cases": 19.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 5.00, "Jul Cases": 2.00, "Aug Cases": 5.00, "Sep Cases": 3.00, "Oct Cases": 0},
    {"State": "NJ", "Account": "ShopRite Liquors", "Premise": "Off", "YTD Cases": 16.00, "YTD PODs": 6, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 1.00, "Sep Cases": 2.00, "Oct Cases": 0},
    {"State": "NJ", "Account": "ShopRite Wines & Spirits", "Premise": "Off", "YTD Cases": 10.00, "YTD PODs": 4, "Apr Cases": 0, "May Cases": 3.00, "Jun Cases": 1.00, "Jul Cases": 0, "Aug Cases": 1.00, "Sep Cases": 2.00, "Oct Cases": 0},
    {"State": "NJ", "Account": "Canal's Liquor", "Premise": "Off", "YTD Cases": 4.00, "YTD PODs": 2, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "NJ", "Account": "Bourbon Street Wine & Spirits", "Premise": "Off", "YTD Cases": 3.00, "YTD PODs": 1, "Apr Cases": 1.00, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 1.00, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "NJ", "Account": "ShopRite", "Premise": "Off", "YTD Cases": 2.00, "YTD PODs": 2, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "NJ", "Account": "Home Liquors", "Premise": "Off", "YTD Cases": 2.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 1.00, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "NJ", "Account": "Joe Canals Discount Liquor", "Premise": "Off", "YTD Cases": 2.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 1.00, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    # IL
    {"State": "IL", "Account": "Binny's Beverage Depot", "Premise": "Off", "YTD Cases": 193.74, "YTD PODs": 43, "Apr Cases": 14.08, "May Cases": 29.00, "Jun Cases": 17.00, "Jul Cases": 56.08, "Aug Cases": 16.00, "Sep Cases": 18.00, "Oct Cases": 1.00},
    {"State": "IL", "Account": "Eataly (Brew Pub, Chicago)", "Premise": "On", "YTD Cases": 115.00, "YTD PODs": 1, "Apr Cases": 20.00, "May Cases": 15.00, "Jun Cases": 14.00, "Jul Cases": 23.00, "Aug Cases": 4.00, "Sep Cases": 7.00, "Oct Cases": 0},
    {"State": "IL", "Account": "VIN Chicago", "Premise": "Off", "YTD Cases": 20.16, "YTD PODs": 2, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "IL", "Account": "Midtown Athletic Club", "Premise": "On", "YTD Cases": 4.33, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 4.33, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "IL", "Account": "Heinen's", "Premise": "Off", "YTD Cases": 3.00, "YTD PODs": 1, "Apr Cases": 1.00, "May Cases": 0, "Jun Cases": 1.00, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "IL", "Account": "Go Grocer", "Premise": "On", "YTD Cases": 2.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 1.00, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "IL", "Account": "ClubProcure", "Premise": "On", "YTD Cases": 1.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "IL", "Account": "Garfield's Beverage Warehouse", "Premise": "Off", "YTD Cases": 1.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 0, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
    {"State": "IL", "Account": "South Loop Market", "Premise": "Off", "YTD Cases": 1.00, "YTD PODs": 1, "Apr Cases": 0, "May Cases": 0, "Jun Cases": 1.00, "Jul Cases": 0, "Aug Cases": 0, "Sep Cases": 0, "Oct Cases": 0},
])

# Top 15 Restaurants/Bars (clean — samples removed) from latest tab
top_restaurants_bars = pd.DataFrame([
    {"Rank": 1, "Restaurant": "Eataly (brew Pub)", "City": "Chicago", "State": "IL", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 115.00, "Apr": 20.00, "May": 15.00, "Jun": 14.00, "Jul": 23.00, "Aug": 4.00, "Sep": 7.00, "Oct": 0},
    {"Rank": 2, "Restaurant": "Eataly", "City": "Los Angeles", "State": "CA", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 40.00, "Apr": 4.00, "May": 5.00, "Jun": 6.00, "Jul": 4.00, "Aug": 5.00, "Sep": 11.00, "Oct": 2.00},
    {"Rank": 3, "Restaurant": "Eataly Vino NYC Eataly Vino", "City": "New York", "State": "NY", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 38.00, "Apr": 3.00, "May": 9.00, "Jun": 10.00, "Jul": 10.00, "Aug": 1.00, "Sep": 3.00, "Oct": 0},
    {"Rank": 4, "Restaurant": "Eataly", "City": "Santa Clara", "State": "CA", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 34.00, "Apr": 0, "May": 9.00, "Jun": 3.00, "Jul": 4.00, "Aug": 1.00, "Sep": 2.00, "Oct": 0},
    {"Rank": 5, "Restaurant": "Eataly (shop)", "City": "Dallas", "State": "TX", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 23.00, "Apr": 6.00, "May": 3.00, "Jun": 3.00, "Jul": 5.00, "Aug": 1.00, "Sep": 5.00, "Oct": 0},
    {"Rank": 6, "Restaurant": "Eataly", "City": "New York", "State": "NY", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 21.00, "Apr": 0, "May": 5.00, "Jun": 0, "Jul": 6.00, "Aug": 0, "Sep": 5.00, "Oct": 0},
    {"Rank": 7, "Restaurant": "Enoteca LA Storia", "City": "Los Gatos", "State": "CA", "Chain": "(independent)", "Channel": "Bar/Tavern", "YTD Cases": 17.00, "Apr": 4.00, "May": 0, "Jun": 4.00, "Jul": 2.00, "Aug": 3.00, "Sep": 4.00, "Oct": 0},
    {"Rank": 8, "Restaurant": "Pizzeria Portofino", "City": "Chicago", "State": "IL", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 16.00, "Apr": 0, "May": 1.00, "Jun": 4.00, "Jul": 4.00, "Aug": 3.00, "Sep": 3.00, "Oct": 1.00},
    {"Rank": 9, "Restaurant": "Eataly NYC Flatiron", "City": "New York", "State": "NY", "Chain": "EATALY", "Channel": "Restaurant", "YTD Cases": 16.00, "Apr": 4.00, "May": 3.00, "Jun": 0, "Jul": 3.00, "Aug": 0, "Sep": 3.00, "Oct": 0},
    {"Rank": 10, "Restaurant": "Vesta", "City": "Redwood City", "State": "CA", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 15.00, "Apr": 0, "May": 4.00, "Jun": 3.00, "Jul": 8.00, "Aug": 0, "Sep": 0, "Oct": 0},
    {"Rank": 11, "Restaurant": "Marvito", "City": "West Hollywood", "State": "CA", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 15.00, "Apr": 5.00, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 2.00, "Oct": 0},
    {"Rank": 12, "Restaurant": "Fino All Is Well Good As Gold", "City": "Denver", "State": "CO", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 14.50, "Apr": 3.00, "May": 2.00, "Jun": 2.00, "Jul": 1.00, "Aug": 2.00, "Sep": 1.00, "Oct": 0},
    {"Rank": 13, "Restaurant": "Tav New York Operation Service", "City": "Jamaica", "State": "NY", "Chain": "CAPITAL ONE LOUNGE", "Channel": "Bar/Tavern", "YTD Cases": 14.17, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 14.17, "Oct": 0},
    {"Rank": 14, "Restaurant": "Eataly - 1st Flr", "City": "Boston", "State": "MA", "Chain": "EATALY", "Channel": "Bar/Tavern", "YTD Cases": 14.00, "Apr": 4.00, "May": 1.00, "Jun": 5.00, "Jul": 0, "Aug": 2.00, "Sep": 2.00, "Oct": 0},
    {"Rank": 15, "Restaurant": "Alta Calidad", "City": "Brooklyn", "State": "NY", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 14.00, "Apr": 0, "May": 0, "Jun": 3.00, "Jul": 2.00, "Aug": 3.00, "Sep": 0, "Oct": 0},
])

# NEW PODs added this past week (prior week -> 10/2/2026 snapshots)
new_pods_week = pd.DataFrame([
    # ON-PREMISE (16 new)
    {"Account": "Mandolin Aegean Bistro", "City": "Miami", "State": "FL", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 3},
    {"Account": "La Voglia", "City": "New York", "State": "NY", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 1},
    {"Account": "1 Hotel Brooklyn Bridge", "City": "Brooklyn", "State": "NY", "Premise": "On", "Chain": "1 Hotel", "Channel": "Hotel/ Motel", "Cases": 1},
    {"Account": "Piazza Di Roma Inc.", "City": "Aberdeen", "State": "NJ", "Premise": "On", "Chain": "(indep)", "Channel": "Other On Premise", "Cases": 1},
    {"Account": "Salt & Flour", "City": "Minneapolis", "State": "MN", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 1},
    {"Account": "Settebello Pizzeria Napoletana", "City": "Pasadena", "State": "CA", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 0},
    {"Account": "Sogno Toscano Cafe", "City": "Los Angeles", "State": "CA", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 0},
    {"Account": "Sogno Toscano Cafe", "City": "Santa Monica", "State": "CA", "Premise": "On", "Chain": "(indep)", "Channel": "Bar/Tavern", "Cases": 0},
    {"Account": "Briciola", "City": "New York", "State": "NY", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 0},
    {"Account": "Piadi", "City": "New York", "State": "NY", "Premise": "On", "Chain": "(indep)", "Channel": "Other On Premise", "Cases": 0},
    {"Account": "Bin + Board", "City": "Brandon", "State": "FL", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 0},
    {"Account": "Seagate Hotel& Spa/Bourbon", "City": "Delray Beach", "State": "FL", "Premise": "On", "Chain": "(indep)", "Channel": "Hotel/ Motel", "Cases": 0},
    {"Account": "Vintage Wine Bar", "City": "Dallas", "State": "TX", "Premise": "On", "Chain": "(indep)", "Channel": "Bar/Tavern", "Cases": 0},
    {"Account": "Crave Pizza", "City": "Mesa", "State": "AZ", "Premise": "On", "Chain": "(indep)", "Channel": "Restaurant", "Cases": 0},
    {"Account": "Spectators", "City": "Jefferson City", "State": "MO", "Premise": "On", "Chain": "(indep)", "Channel": "Bar/Tavern", "Cases": 0},
    {"Account": "Hickory Hills Country Club", "City": "Springfield", "State": "MO", "Premise": "On", "Chain": "(indep)", "Channel": "Golf/ Country Club", "Cases": 0},
    # OFF-PREMISE (18 new)
    {"Account": "Avenue A Liquor Corp.", "City": "New York", "State": "NY", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package Store", "Cases": 1},
    {"Account": "Total Wine & More #1408", "City": "Spokane", "State": "WA", "Premise": "Off", "Chain": "Total Wine & More", "Channel": "Liquor/Package Store", "Cases": 1},
    {"Account": "Safeway #3217", "City": "Washington", "State": "DC", "Premise": "Off", "Chain": "Safeway", "Channel": "Liquor/Package Store", "Cases": 1},
    {"Account": "Cork & Keg", "City": "Emerson", "State": "NJ", "Premise": "Off", "Chain": "(indep)", "Channel": "Other Off Premise", "Cases": 0},
    {"Account": "Garys Closter", "City": "Closter", "State": "NJ", "Premise": "Off", "Chain": "Garys Wine & Marketplace", "Channel": "Other Off Premise", "Cases": 0},
    {"Account": "Total Wine & More #947", "City": "Tampa", "State": "FL", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package Store", "Cases": 0},
    {"Account": "Food Lion #0465", "City": "Burlington", "State": "NC", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0},
    {"Account": "Food Lion 2538", "City": "Littleton", "State": "NC", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0},
    {"Account": "Food Lion 2114", "City": "Oak Island", "State": "NC", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0},
    {"Account": "Food Lion 1573", "City": "Raleigh", "State": "NC", "Premise": "Off", "Chain": "Food Lion", "Channel": "Supermarket", "Cases": 0},
    {"Account": "Sparkys Bardega", "City": "Asheville", "State": "NC", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package Store", "Cases": 0},
    {"Account": "Total Wine & More # 530", "City": "Houston", "State": "TX", "Premise": "Off", "Chain": "Total Wine & More", "Channel": "Liquor/Package Store", "Cases": 0},
    {"Account": "Trader Joe S # 626", "City": "Lexington", "State": "KY", "Premise": "Off", "Chain": "Trader Joes Liquor", "Channel": "Liquor/Package Store", "Cases": 0},
    {"Account": "Trader Joe S # 625", "City": "Louisville", "State": "KY", "Premise": "Off", "Chain": "Trader Joes", "Channel": "Liquor/Package Store", "Cases": 0},
    {"Account": "Ingles #086", "City": "Chatsworth", "State": "GA", "Premise": "Off", "Chain": "Ingles", "Channel": "Supermarket", "Cases": 0},
    {"Account": "De Arcos Center", "City": "Santa Fe", "State": "NM", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package Store", "Cases": 0},
    {"Account": "Northbound Liquor - Cambr", "City": "Cambridge", "State": "MN", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package Store", "Cases": 0},
    {"Account": "Macadoodles - Dardenne Prairie", "City": "Dardenne Prairie", "State": "MO", "Premise": "Off", "Chain": "(indep)", "Channel": "Liquor/Package Store", "Cases": 0},
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

# Sample tracking (Lucci vs Ethica-funded sample activity)
with open(os.path.join(os.path.dirname(__file__), "samples.json"), "r", encoding="utf-8") as _f:
    _samples = json.load(_f)
samples_by_bucket_df = pd.DataFrame(_samples["by_bucket"])
samples_by_funded_df = pd.DataFrame(_samples["by_funded_by"])
samples_top_accts_df = pd.DataFrame(_samples["top_accounts"])
SAMPLES_NOTE = _samples["notes"]

# New PODs velocity (weekly count + this-week breakdown by state/channel)
with open(os.path.join(os.path.dirname(__file__), "new_pods_velocity.json"), "r", encoding="utf-8") as _f:
    _velocity = json.load(_f)
velocity_df = pd.DataFrame(_velocity["weekly"])
velocity_df["week_ending"] = pd.to_datetime(velocity_df["week_ending"])
new_pods_by_state_df = pd.DataFrame(_velocity["this_week_by_state"])
new_pods_by_channel_on_df = pd.DataFrame(_velocity["this_week_by_channel_on"])
new_pods_by_channel_off_df = pd.DataFrame(_velocity["this_week_by_channel_off"])

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
    {"Trade Channel": "Liquor / Package Store", "YTD Cases": 1847.18, "Dec": 3.24, "Jan": 132.81, "Feb": 189.80, "Mar": 225.39, "Apr": 116.59, "May": 182.24, "Jun": 268.68, "Jul": 310.76, "Aug": 178.42, "Sep": 232.26, "Oct": 7.00},
    {"Trade Channel": "Supermarket", "YTD Cases": 872.62, "Dec": 0, "Jan": 51.17, "Feb": 86.25, "Mar": 121.57, "Apr": 70.58, "May": 152.42, "Jun": 99.20, "Jul": 84.35, "Aug": 89.77, "Sep": 116.74, "Oct": 0.58},
    {"Trade Channel": "Other Off Premise", "YTD Cases": 642.58, "Dec": 5.75, "Jan": 26.08, "Feb": 185.17, "Mar": 42.24, "Apr": 60.92, "May": 46.91, "Jun": 60.17, "Jul": 84.50, "Aug": 53.33, "Sep": 65.16, "Oct": 11.33},
    {"Trade Channel": "General Merchandise", "YTD Cases": 154.00, "Dec": 0, "Jan": 13.00, "Feb": 19.00, "Mar": 4.00, "Apr": 13.00, "May": 8.00, "Jun": 15.00, "Jul": 20.00, "Aug": 15.00, "Sep": 47.00, "Oct": 0},
    {"Trade Channel": "Wholesale Club", "YTD Cases": 43.25, "Dec": 0, "Jan": 0, "Feb": 4.00, "Mar": 8.00, "Apr": 3.17, "May": 8.08, "Jun": 6.00, "Jul": 3.00, "Aug": 8.00, "Sep": 3.00, "Oct": 0},
    {"Trade Channel": "Fine Wine Store", "YTD Cases": 18.33, "Dec": 0, "Jan": 0, "Feb": 1.08, "Mar": 2.25, "Apr": 1.83, "May": 4.67, "Jun": 2.08, "Jul": 0.91, "Aug": 2.33, "Sep": 3.17, "Oct": 0},
    {"Trade Channel": "Convenience / Gas", "YTD Cases": 17.75, "Dec": 1.00, "Jan": 0, "Feb": 1.00, "Mar": 3.83, "Apr": 2.42, "May": 1.25, "Jun": 2.00, "Jul": 2.17, "Aug": 0, "Sep": 4.08, "Oct": 0},
    {"Trade Channel": "Small Grocery Store", "YTD Cases": 10.00, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0, "Apr": 6.00, "May": 1.00, "Jun": 2.00, "Jul": 0, "Aug": 0, "Sep": 1.00, "Oct": 0},
    {"Trade Channel": "Retail Specialty Services", "YTD Cases": 1.75, "Dec": 0, "Jan": 0, "Feb": 0.50, "Mar": 0, "Apr": 0, "May": 0.25, "Jun": 0, "Jul": 0, "Aug": 1.00, "Sep": 0, "Oct": 0},
])

on_trade_channels = pd.DataFrame([
    {"Trade Channel": "Restaurant", "YTD Cases": 1058.14, "Dec": 14.00, "Jan": 17.33, "Feb": 81.42, "Mar": 121.25, "Apr": 150.74, "May": 158.32, "Jun": 124.91, "Jul": 160.91, "Aug": 96.16, "Sep": 125.76, "Oct": 7.33},
    {"Trade Channel": "Bar / Tavern", "YTD Cases": 213.25, "Dec": 0, "Jan": 5.00, "Feb": 8.41, "Mar": 16.42, "Apr": 25.09, "May": 23.58, "Jun": 41.08, "Jul": 21.75, "Aug": 20.50, "Sep": 51.42, "Oct": 0},
    {"Trade Channel": "Other On Premise", "YTD Cases": 153.16, "Dec": 1.00, "Jan": 2.00, "Feb": 19.00, "Mar": 10.00, "Apr": 11.33, "May": 25.25, "Jun": 20.50, "Jul": 28.34, "Aug": 16.67, "Sep": 17.08, "Oct": 2.00},
    {"Trade Channel": "Hotel / Motel", "YTD Cases": 133.50, "Dec": 0, "Jan": 0, "Feb": 4.17, "Mar": 3.17, "Apr": 10.08, "May": 14.00, "Jun": 49.50, "Jul": 8.00, "Aug": 18.58, "Sep": 24.00, "Oct": 2.00},
    {"Trade Channel": "Golf / Country Club", "YTD Cases": 72.49, "Dec": 1.00, "Jan": 3.00, "Feb": 1.50, "Mar": 10.08, "Apr": 5.00, "May": 30.00, "Jun": 6.41, "Jul": 3.50, "Aug": 8.00, "Sep": 4.00, "Oct": 0},
    {"Trade Channel": "Concessionaire", "YTD Cases": 13.00, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 3.00, "Jun": 0, "Jul": 3.00, "Aug": 5.00, "Sep": 2.00, "Oct": 0},
    {"Trade Channel": "Special Event / Temp License", "YTD Cases": 5.50, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0, "Apr": 2.00, "May": 1.00, "Jun": 0.50, "Jul": 1.00, "Aug": 0, "Sep": 1.00, "Oct": 0},
    {"Trade Channel": "Recreation / Entertainment", "YTD Cases": 0.50, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0.50, "Aug": 0, "Sep": 0, "Oct": 0},
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
    ["Overview", "Shipments", "Depletions", "POD Recency", "Sample Tracking", "Account Explorer", "Gopuff", "ReserveBar"],
    horizontal=True,
    label_visibility="collapsed",
)

st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# SHARED MONTH OPTIONS
# ══════════════════════════════════════════════════════════════════════════════
DEPL_MONTHS = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
SHIP_MONTHS = ["Dec '25", "Jan '26", "Feb '26", "Mar '26", "Apr '26", "May '26", "Jun '26", "Jul '26"]
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
        st.markdown(kpi("Total YTD PODs", "1,809", "29 active states", dark=True), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Cases Shipped", "6,822", "Dec '25 – Jul '26 · Aug pending"), unsafe_allow_html=True)
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

    # Monthly detail — click column headers to sort
    section_title("Monthly Detail")
    st.caption("Partial months (Sep) compare to same-period prior month (Oct 1-2 vs Oct 1-2). Click any column to sort.")
    cd_filt = channel_detail[channel_detail["Short"].isin(ov_months)].copy()
    cd_display = cd_filt[["Month", "Total Depletions", "Compare Ref", "Depl Change vs LM", "% Change vs LM", "On-Premise", "Off-Premise"]].copy()
    st.dataframe(
        cd_display, use_container_width=True, hide_index=True, height=340,
        column_config={
            "Month":               st.column_config.TextColumn("Month"),
            "Total Depletions":    st.column_config.NumberColumn("Total Depletions", format="%.2f"),
            "Compare Ref":         st.column_config.TextColumn("Compared To"),
            "Depl Change vs LM":   st.column_config.NumberColumn("Δ vs prior", format="%+.2f"),
            "% Change vs LM":      st.column_config.NumberColumn("% Change", format="%+.1f%%"),
            "On-Premise":          st.column_config.NumberColumn("On-Premise", format="%.2f"),
            "Off-Premise":         st.column_config.NumberColumn("Off-Premise", format="%.2f"),
        },
    )

    # Top 3 States — sortable
    section_title("Top States by Depletions")
    st.caption("Top-performing states in the filtered period · click any column to sort.")
    top3_display = top3_states[["State", "Total Cases", "Total PODs", "On Cases", "Off Cases"]].copy()
    st.dataframe(
        top3_display, use_container_width=True, hide_index=True, height=180,
        column_config={
            "Total Cases": st.column_config.NumberColumn("Total Cases", format="%.2f"),
            "Total PODs":  st.column_config.NumberColumn("Total PODs", format="%d"),
            "On Cases":    st.column_config.NumberColumn("On-Premise Cases", format="%.2f"),
            "Off Cases":   st.column_config.NumberColumn("Off-Premise Cases", format="%.2f"),
        },
    )

    # ── NEW PODs THIS PAST WEEK ──────────────────────────────────────────────
    section_title("New PODs This Past Week")
    n_total = len(new_pods_week)
    n_on = int((new_pods_week["Premise"] == "On").sum())
    n_off = int((new_pods_week["Premise"] == "Off").sum())
    cs_total = new_pods_week["Cases"].sum()
    cs_on = new_pods_week.loc[new_pods_week["Premise"] == "On", "Cases"].sum()
    cs_off = new_pods_week.loc[new_pods_week["Premise"] == "Off", "Cases"].sum()
    state_count = new_pods_week["State"].nunique()
    # 4-week rolling avg from velocity for context
    velo = velocity_df.dropna(subset=["new_pods"])
    last4 = velo.tail(4)["new_pods"].mean() if len(velo) >= 4 else velo["new_pods"].mean() if len(velo) else 0
    vs_avg = int(round(n_total - last4)) if last4 else 0
    st.caption(
        f"📍 Week of {DEPLETION_AS_OF} · samples excluded · accounts that first depleted Lucci during this week"
    )

    npk1, npk2, npk3, npk4 = st.columns(4)
    with npk1:
        st.markdown(kpi("🆕 New PODs This Week", f"{n_total}",
                         f"{'+' if vs_avg >= 0 else ''}{vs_avg} vs 4-wk avg ({last4:.0f})", dark=True), unsafe_allow_html=True)
    with npk2:
        st.markdown(kpi("New · On-Premise", f"{n_on}", f"{cs_on:.2f} cases"), unsafe_allow_html=True)
    with npk3:
        st.markdown(kpi("New · Off-Premise", f"{n_off}", f"{cs_off:.2f} cases"), unsafe_allow_html=True)
    with npk4:
        st.markdown(kpi("States with new PODs", f"{state_count}", f"{cs_total:.2f} cases added"), unsafe_allow_html=True)

    # (b) Weekly velocity — last 8 weeks with WoW % change
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("New PODs · Week-over-Week")
    st.caption("Weekly new-account count with the % change vs. the prior week. Watching for deceleration.")
    velo_recent = velo.tail(8).copy()
    velo_recent["Week Ending"] = velo_recent["week_ending"].dt.strftime("%b %d")
    velo_recent["New PODs"] = velo_recent["new_pods"].astype(int)
    velo_recent["WoW %"] = velo_recent["new_pods"].pct_change() * 100
    st.dataframe(
        velo_recent[["Week Ending", "New PODs", "WoW %"]],
        use_container_width=True, hide_index=True, height=310,
        column_config={
            "New PODs": st.column_config.NumberColumn("New PODs", format="%d"),
            "WoW %":    st.column_config.NumberColumn("WoW %",    format="%+.1f%%"),
        },
    )

    # (c) This-week breakdown by state and channel
    st.markdown("<br>", unsafe_allow_html=True)
    npbc1, npbc2 = st.columns(2)
    with npbc1:
        section_title("New PODs · By State (this week)")
        if len(new_pods_by_state_df):
            st.dataframe(
                new_pods_by_state_df.rename(columns={"state": "State", "count": "New PODs"}),
                use_container_width=True, hide_index=True, height=340,
            )
        else:
            st.caption("_No new PODs this week._")
    with npbc2:
        section_title("New PODs · By Channel (this week)")
        st.markdown("**On-Premise**")
        if len(new_pods_by_channel_on_df):
            st.dataframe(
                new_pods_by_channel_on_df.rename(columns={"channel": "Channel", "count": "New PODs"}),
                use_container_width=True, hide_index=True, height=150,
            )
        else:
            st.caption("_No new on-premise this week._")
        st.markdown("**Off-Premise**")
        if len(new_pods_by_channel_off_df):
            st.dataframe(
                new_pods_by_channel_off_df.rename(columns={"channel": "Channel", "count": "New PODs"}),
                use_container_width=True, hide_index=True, height=150,
            )
        else:
            st.caption("_No new off-premise this week._")

    # Full list of new PODs this week
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("New PODs This Week — Full List")
    npk_display = new_pods_week[["Account", "City", "State", "Premise", "Chain", "Channel", "Cases"]].copy()
    st.dataframe(
        npk_display, use_container_width=True, hide_index=True, height=380,
        column_config={"Cases": st.column_config.NumberColumn("Cases", format="%.2f")},
    )

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
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">1,809</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">TOTAL PODS</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">28</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">STATES</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SHIPMENTS & REVENUE
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Shipments":
    st.caption("📅 Shipment data through Jul 2026 · Aug shipments pending from EW · Source: Lucci Payment Process file")
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
    st.caption("Click any column to sort.")
    sc_filt["Chg vs LM"] = sc_filt["Cases"].diff()
    st.dataframe(
        sc_filt[["Month", "Cases", "Chg vs LM"]],
        use_container_width=True, hide_index=True, height=280,
        column_config={
            "Cases":     st.column_config.NumberColumn("Cases", format="%d"),
            "Chg vs LM": st.column_config.NumberColumn("Δ vs prior", format="%+d"),
        },
    )


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
    gm_filt = grand_monthly[grand_monthly["Month"].isin(dp_months)]
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
    st.caption(f"Samples excluded · as of {DEPLETION_AS_OF} · Partial months (Sep) compare to same-period prior (Oct 1-2 vs Oct 1-2). Click any column to sort.")
    cd_filt = channel_detail[channel_detail["Short"].isin(dp_months)].copy()
    cd_display = cd_filt[["Month", "Total Depletions", "Total PODs", "Compare Ref", "Depl Change vs LM", "% Change vs LM", "On-Premise", "Off-Premise"]].copy()
    st.dataframe(
        cd_display, use_container_width=True, hide_index=True, height=380,
        column_config={
            "Month":               st.column_config.TextColumn("Month"),
            "Total Depletions":    st.column_config.NumberColumn("Total Depletions", format="%.2f"),
            "Total PODs":          st.column_config.NumberColumn("Active PODs", format="%d"),
            "Compare Ref":         st.column_config.TextColumn("Compared To"),
            "Depl Change vs LM":   st.column_config.NumberColumn("Δ vs prior", format="%+.2f"),
            "% Change vs LM":      st.column_config.NumberColumn("% Change", format="%+.1f%%"),
            "On-Premise":          st.column_config.NumberColumn("On-Premise", format="%.2f"),
            "Off-Premise":         st.column_config.NumberColumn("Off-Premise", format="%.2f"),
        },
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── State Performance — Jun / Jul / Aug with new PODs ──
    section_title("State Performance — Jul / Aug / Sep")
    st.caption(f"As of {DEPLETION_AS_OF}. Aug & Sep are full months; Oct is partial (1–2). 'YTD PODs' = unique accounts active YTD. 'New Aug/Sep/Oct PODs' = accounts that first depleted Lucci that month. Samples excluded.")

    state_view = st.radio(
        "View",
        ["Total", "On-Premise", "Off-Premise"],
        horizontal=True,
        key="state_view_toggle",
        label_visibility="collapsed",
    )

    on_f = on_states[on_states["State"].isin(dp_states)].copy()
    off_f = off_states[off_states["State"].isin(dp_states)].copy()

    sp_cols = ["Aug Cases", "Sep Cases", "Oct Cases", "YTD PODs", "New Aug PODs", "New Sep PODs", "New Oct PODs"]
    if state_view == "On-Premise":
        sp = on_f[["State"] + sp_cols].copy()
    elif state_view == "Off-Premise":
        sp = off_f[["State"] + sp_cols].copy()
    else:
        on_agg = on_f.groupby("State", as_index=False)[sp_cols].sum()
        off_agg = off_f.groupby("State", as_index=False)[sp_cols].sum()
        sp = pd.concat([on_agg, off_agg]).groupby("State", as_index=False).sum()

    sp = sp.sort_values("Sep Cases", ascending=False).reset_index(drop=True)

    sp_display = sp[["State", "Aug Cases", "Sep Cases", "Oct Cases", "YTD PODs", "New Aug PODs", "New Sep PODs", "New Oct PODs"]].copy()

    st.caption("Click any column header to sort · e.g. sort by YTD PODs to find top-POD states, or Sep Cases to spot top current-period movers")
    st.dataframe(
        sp_display, use_container_width=True, hide_index=True, height=520,
        column_config={
            "Aug Cases":     st.column_config.NumberColumn("Aug Cases", format="%.2f"),
            "Sep Cases":     st.column_config.NumberColumn("Sep Cases", format="%.2f"),
            "Oct Cases":     st.column_config.NumberColumn("Oct MTD",   format="%.2f"),
            "YTD PODs":      st.column_config.NumberColumn("YTD PODs", format="%d"),
            "New Aug PODs":  st.column_config.NumberColumn("New Aug PODs", format="%d"),
            "New Sep PODs":  st.column_config.NumberColumn("New Sep PODs", format="%d"),
            "New Oct PODs":  st.column_config.NumberColumn("New Oct PODs", format="%d"),
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
    sda["Chg vs LM"] = sda["Sep Cases"] - sda["Aug Cases"]
    sda["% Growth"] = sda.apply(
        lambda r: ((r["Sep Cases"] - r["Aug Cases"]) / r["Aug Cases"] * 100) if r["Aug Cases"] > 0 else (float("inf") if r["Sep Cases"] > 0 else 0),
        axis=1,
    )
    st.dataframe(
        sda[["Account", "Premise", "YTD Cases", "YTD PODs", "Aug Cases", "Sep Cases", "Oct Cases"]],
        use_container_width=True, hide_index=True, height=480,
        column_config={
            "YTD Cases": st.column_config.NumberColumn("YTD Cases", format="%.2f"),
            "YTD PODs":  st.column_config.NumberColumn("YTD PODs", format="%d"),
            "Aug Cases": st.column_config.NumberColumn("Aug Cases", format="%.2f"),
            "Sep Cases": st.column_config.NumberColumn("Sep Cases", format="%.2f"),
            "Oct Cases": st.column_config.NumberColumn("Oct MTD",   format="%.2f"),
        },
    )

    # ── Top 10 Restaurants / Bars ──
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Top 10 Restaurants & Bars by YTD Depletions")
    st.caption(f"On-premise restaurants, bars, and fine-dining accounts · sorted by YTD cases · as of {DEPLETION_AS_OF} · Samples excluded")
    st.dataframe(
        top_restaurants_bars[["Rank", "Restaurant", "City", "State", "Chain", "Channel", "YTD Cases", "Aug", "Sep", "Oct"]],
        use_container_width=True, hide_index=True, height=560,
        column_config={
            "Rank":      st.column_config.NumberColumn("Rank", format="%d"),
            "YTD Cases": st.column_config.NumberColumn("YTD Cases", format="%.2f"),
            "Aug":       st.column_config.NumberColumn("Aug", format="%.2f"),
            "Sep":       st.column_config.NumberColumn("Sep", format="%.2f"),
            "Oct":       st.column_config.NumberColumn("Oct MTD", format="%.2f"),
        },
    )

    # Trade channel breakdown — Jan through current, with MTD + %vs Jul same-period
    st.markdown("<br>", unsafe_allow_html=True)

    def _tc_with_mtd(df):
        """Add 'Oct 1-2' (Sep scaled to same-period MTD as Oct) and '% vs Sep' columns."""
        out = df.copy()
        out["Oct 1-2"] = out["Sep"] * (2/30)
        out["% vs Sep"] = out.apply(
            lambda r: ((r["Oct"] - r["Oct 1-2"]) / r["Oct 1-2"] * 100) if r["Oct 1-2"] > 0 else 0,
            axis=1,
        )
        return out

    section_title("Off-Premise by Trade Channel")
    st.caption(f"As of {DEPLETION_AS_OF} · Jan 2026 → Oct MTD · '% vs Sep' compares Oct 1-2 to Sep scaled to 2 days (same-period). Click any column to sort. Samples / internal excluded.")
    tc_off = _tc_with_mtd(off_trade_channels)
    st.dataframe(
        tc_off[["Trade Channel", "YTD Cases", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "% vs Sep"]],
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
            "Aug": st.column_config.NumberColumn("Aug", format="%.2f"),
            "Sep": st.column_config.NumberColumn("Sep", format="%.2f"),
            "Oct": st.column_config.NumberColumn("Oct MTD", format="%.2f"),
            "% vs Sep": st.column_config.NumberColumn("% vs Oct 1-2", format="%+.1f%%"),
        },
    )

    section_title("On-Premise by Trade Channel")
    st.caption(f"As of {DEPLETION_AS_OF} · Jan 2026 → Oct MTD · '% vs Sep' compares Oct 1-2 to Sep scaled to 2 days (same-period). Click any column to sort. Samples / internal excluded.")
    tc_on = _tc_with_mtd(on_trade_channels)
    st.dataframe(
        tc_on[["Trade Channel", "YTD Cases", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "% vs Sep"]],
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
            "Aug": st.column_config.NumberColumn("Aug", format="%.2f"),
            "Sep": st.column_config.NumberColumn("Sep", format="%.2f"),
            "Oct": st.column_config.NumberColumn("Oct MTD", format="%.2f"),
            "% vs Sep": st.column_config.NumberColumn("% vs Oct 1-2", format="%+.1f%%"),
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

    acct_display = ta_filt[["Account", "Premise", "States", "YTD Cases", "YTD PODs", "Aug Cases", "Sep Cases", "Oct Cases"]].copy()
    st.dataframe(
        acct_display, use_container_width=True, hide_index=True, height=560,
        column_config={
            "YTD Cases": st.column_config.NumberColumn("YTD Cases", format="%.2f"),
            "YTD PODs":  st.column_config.NumberColumn("YTD PODs", format="%d"),
            "Aug Cases": st.column_config.NumberColumn("Aug", format="%.2f"),
            "Sep Cases": st.column_config.NumberColumn("Sep", format="%.2f"),
            "Oct Cases": st.column_config.NumberColumn("Oct MTD", format="%.2f"),
        },
    )

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
# POD ORDER RECENCY — all PODs flagged by last order date
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "POD Recency":
    st.caption(f"📅 Depletion data as of **{DEPLETION_AS_OF}** · Samples / internal accounts excluded · Source: Ethica weekly snapshots")

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
    rec_states = sorted(v for v in pod_recency_df["state"].unique() if v and str(v) != "nan")
    rec_premises = sorted(v for v in pod_recency_df["premise"].unique() if v and str(v) != "nan")
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
    st.dataframe(styled, use_container_width=True, height=650)


# ══════════════════════════════════════════════════════════════════════════════
# SAMPLE TRACKING — Lucci-funded vs Ethica-funded
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Sample Tracking":
    st.caption(f"📅 Depletion data as of **{DEPLETION_AS_OF}** · Source: Ethica weekly snapshots")

    section_title("Sample Tracking — Lucci vs. Ethica-funded")
    st.caption(
        f"Cases we exclude from depletions as samples, categorized by who funded them. "
        f"Note: {SAMPLES_NOTE}"
    )

    # 3-KPI summary — Lucci / Ethica / Low-volume (new bucket for ≤1/3 case YTD)
    lucci_row  = samples_by_funded_df[samples_by_funded_df["funded_by"] == "Lucci"]
    ethica_row = samples_by_funded_df[samples_by_funded_df["funded_by"] == "Ethica"]
    unknown_row = samples_by_funded_df[samples_by_funded_df["funded_by"] == "Unknown"]
    lucci_ytd   = float(lucci_row["ytd_cases"].iloc[0])  if len(lucci_row)  else 0
    ethica_ytd  = float(ethica_row["ytd_cases"].iloc[0]) if len(ethica_row) else 0
    unknown_ytd = float(unknown_row["ytd_cases"].iloc[0]) if len(unknown_row) else 0
    lucci_ct    = int(lucci_row["accounts"].iloc[0])  if len(lucci_row)  else 0
    ethica_ct   = int(ethica_row["accounts"].iloc[0]) if len(ethica_row) else 0
    unknown_ct  = int(unknown_row["accounts"].iloc[0]) if len(unknown_row) else 0
    smp1, smp2, smp3, smp4 = st.columns(4)
    with smp1:
        st.markdown(kpi("Lucci-funded samples", f"{lucci_ytd:,.2f}",
                         f"{lucci_ct} accounts · marketing / activations", dark=True), unsafe_allow_html=True)
    with smp2:
        st.markdown(kpi("Ethica-funded samples", f"{ethica_ytd:,.2f}",
                         f"{ethica_ct} accounts · supplier arm / distributor / reps"), unsafe_allow_html=True)
    with smp3:
        st.markdown(kpi("Likely tastings (≤1/3 case)", f"{unknown_ytd:,.2f}",
                         f"{unknown_ct} accounts · scrubbed per new methodology"), unsafe_allow_html=True)
    with smp4:
        total = lucci_ytd + ethica_ytd + unknown_ytd
        st.markdown(kpi("Total sample volume YTD", f"{total:,.2f}",
                         f"~{(total / (total + 4574) * 100):.1f}% of gross depletions" if (total + 4574) > 0 else ""), unsafe_allow_html=True)

    # Breakdown by bucket
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Sample Breakdown by Bucket")
    st.caption("Click any column to sort. Each bucket represents a distinct sample-funding source.")
    smpl_display = samples_by_bucket_df[["label", "funded_by", "accounts", "ytd_cases",
                                          "aug", "sep", "oct"]].copy()
    smpl_display.columns = ["Bucket", "Funded By", "Accounts", "YTD Cases", "Aug", "Sep", "Oct MTD"]
    st.dataframe(
        smpl_display, use_container_width=True, hide_index=True, height=280,
        column_config={
            "Accounts": st.column_config.NumberColumn("Accounts", format="%d"),
            "YTD Cases": st.column_config.NumberColumn("YTD Cases", format="%.2f"),
            "Aug": st.column_config.NumberColumn("Aug", format="%.2f"),
            "Sep": st.column_config.NumberColumn("Sep", format="%.2f"),
            "Oct MTD": st.column_config.NumberColumn("Oct MTD", format="%.2f"),
        },
    )

    # Top sample accounts
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Top Sample-Tagged Accounts (YTD)")
    top_smp = samples_top_accts_df[["account", "state", "trade_channel", "label", "funded_by", "ytd_cases"]].copy()
    top_smp.columns = ["Account", "State", "Channel", "Bucket", "Funded By", "YTD Cases"]
    st.dataframe(
        top_smp, use_container_width=True, hide_index=True, height=480,
        column_config={"YTD Cases": st.column_config.NumberColumn("YTD Cases", format="%.2f")},
    )


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

    # Clean 'nan' premise values (a small number of UNCLASSIFIED accounts have
    # no premise assigned in Ethica's raw data — treat as OFF-premise for
    # filter purposes rather than showing 'nan' as a chip)
    _pod_df = pod_recency_df.copy()
    _pod_df["premise"] = _pod_df["premise"].replace(["nan", "NaN"], "OFF")
    ae_states = sorted(v for v in _pod_df["state"].unique() if v and str(v) != "nan")
    ae_channels = sorted(v for v in _pod_df["channel"].unique() if v and str(v) != "nan")
    ae_premises = sorted(v for v in _pod_df["premise"].unique() if v and str(v) != "nan")

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

    ae_filt = _pod_df.copy()
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
    ae_oct_cases = ae_filt["oct"].sum() if "oct" in ae_filt.columns else 0
    ae_count = len(ae_filt)
    ae_states_filt = ae_filt["state"].nunique()
    aek1, aek2, aek3, aek4, aek5 = st.columns(5)
    with aek1:
        st.markdown(kpi("Accounts (filtered)", f"{ae_count:,}", f"of {len(pod_recency_df):,} total", dark=True), unsafe_allow_html=True)
    with aek2:
        st.markdown(kpi("Filtered YTD Cases", f"{ae_cases:,.2f}", f"Across {ae_states_filt} state(s)"), unsafe_allow_html=True)
    with aek3:
        st.markdown(kpi("Oct MTD Cases", f"{ae_oct_cases:,.2f}", f"Through {DEPLETION_AS_OF}"), unsafe_allow_html=True)
    with aek4:
        active = int((ae_filt["status"] == "Green").sum())
        st.markdown(kpi("🟢 Active (≤60d)", f"{active:,}", f"{round(active/max(ae_count,1)*100,1)}% of filtered"), unsafe_allow_html=True)
    with aek5:
        stale = int((ae_filt["status"] == "Red").sum())
        st.markdown(kpi("🔴 Stale (90+d)", f"{stale:,}", f"{round(stale/max(ae_count,1)*100,1)}% of filtered"), unsafe_allow_html=True)

    # Prep display DataFrame — sortable via st.dataframe native click-to-sort
    ae_display = ae_filt[[
        "account", "city", "state", "premise", "chain", "channel",
        "ytd_cases", "aug", "sep", "oct",
        "last_order_date", "days_since", "status",
    ]].copy()
    ae_display.columns = [
        "Account", "City", "State", "Premise", "Chain", "Channel",
        "YTD Cases", "Aug", "Sep", "Oct MTD",
        "Last Order", "Days Since", "Status",
    ]
    ae_display = ae_display.sort_values("YTD Cases", ascending=False)

    st.markdown(f"<p style='margin:4px 0; font-size:13px; color:#6b7280;'>Showing <strong>{len(ae_display):,}</strong> of {len(pod_recency_df):,} accounts · click column headers to sort</p>", unsafe_allow_html=True)
    st.dataframe(
        ae_display,
        use_container_width=True, height=650, hide_index=True,
        column_config={
            "YTD Cases": st.column_config.NumberColumn("YTD Cases", format="%.2f"),
            "Aug":       st.column_config.NumberColumn("Aug", format="%.2f"),
            "Sep":       st.column_config.NumberColumn("Sep", format="%.2f"),
            "Oct MTD":   st.column_config.NumberColumn("Oct MTD", format="%.2f"),
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
    st.caption("Click any column to sort.")
    detail_display = gl_filt[["Rank", "Location", "ST", "Jan", "Feb", "Mar", "Apr", "YTD"]].copy()
    st.dataframe(
        detail_display, use_container_width=True, hide_index=True, height=440,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", format="%d"),
            "Jan":  st.column_config.NumberColumn("Jan",  format="%d"),
            "Feb":  st.column_config.NumberColumn("Feb",  format="%d"),
            "Mar":  st.column_config.NumberColumn("Mar",  format="%d"),
            "Apr":  st.column_config.NumberColumn("Apr",  format="%d"),
            "YTD":  st.column_config.NumberColumn("YTD",  format="%d"),
        },
    )


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
st.markdown(f'<p class="footer-text">Data Period: Dec 2025 – Sep 2026 &middot; Depletions thru {DEPLETION_AS_OF} &middot; Gopuff thru {GOPUFF_AS_OF} &middot; Samples / internal accounts excluded &middot; Lucci Sales Intelligence</p>', unsafe_allow_html=True)

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
            <p style="margin:0; font-size:13px; color:rgba(255,255,255,0.95); font-weight:700;">Depletions: 5/1/26 &middot; Gopuff: 4/25/26 &middot; ReserveBar: 4/25/26</p>
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

# Source: Ethica Depletions 05.01.26 tab (data through May 1, 2026)
# Apr is now a complete month (full 30 days). May data is just 5/1 (1 day, minimal).
# IMPORTANT: All numbers below have SAMPLE / INTERNAL accounts removed
# (excludes accounts containing SAMPLE, F&F FINE WINE, SGWS-, TEAM #).
# 115.80 YTD cases / 111 PODs excluded as samples/internal.
DEPLETION_AS_OF = "5/1/2026"

grand_monthly = pd.DataFrame([
    {"Month": "Nov", "Cases": 0, "PODs": 0},
    {"Month": "Dec", "Cases": 24.72, "PODs": 23},
    {"Month": "Jan", "Cases": 242.78, "PODs": 199},
    {"Month": "Feb", "Cases": 599.28, "PODs": 391},
    {"Month": "Mar", "Cases": 551.41, "PODs": 552},
    {"Month": "Apr", "Cases": 430.94, "PODs": 328},
])

combined_monthly = pd.DataFrame([
    {"Month": "Nov", "On-Premise": 0, "Off-Premise": 0},
    {"Month": "Dec", "On-Premise": 16.32, "Off-Premise": 8.40},
    {"Month": "Jan", "On-Premise": 29.32, "Off-Premise": 202.55},
    {"Month": "Feb", "On-Premise": 123.27, "Off-Premise": 475.76},
    {"Month": "Mar", "On-Premise": 163.24, "Off-Premise": 388.17},
    {"Month": "Apr", "On-Premise": 197.87, "Off-Premise": 232.82},
])

# Channel breakdown — chronological (oldest → newest)
channel_detail = pd.DataFrame([
    {"Month": "Nov 2025", "Short": "Nov", "Total Depletions": 0, "Total PODs": 0, "On-Premise": 0, "Off-Premise": 0},
    {"Month": "Dec 2025", "Short": "Dec", "Total Depletions": 24.72, "Total PODs": 23, "On-Premise": 16.32, "Off-Premise": 8.40},
    {"Month": "Jan 2026", "Short": "Jan", "Total Depletions": 242.78, "Total PODs": 199, "On-Premise": 29.32, "Off-Premise": 202.55},
    {"Month": "Feb 2026", "Short": "Feb", "Total Depletions": 599.28, "Total PODs": 391, "On-Premise": 123.27, "Off-Premise": 475.76},
    {"Month": "Mar 2026", "Short": "Mar", "Total Depletions": 551.41, "Total PODs": 552, "On-Premise": 163.24, "Off-Premise": 388.17},
    {"Month": "Apr 2026", "Short": "Apr", "Total Depletions": 430.94, "Total PODs": 328, "On-Premise": 197.87, "Off-Premise": 232.82},
])

# Compute change vs last month (chronological order: prior month is row i-1)
depl_vals = channel_detail["Total Depletions"].tolist()
pod_vals = channel_detail["Total PODs"].tolist()
changes, pct_changes, pod_changes, pod_pct_changes = [], [], [], []
for i in range(len(depl_vals)):
    if i > 0:
        prev = depl_vals[i - 1]
        chg = depl_vals[i] - prev
        pct = (chg / prev * 100) if prev > 0 else float("inf")
        changes.append(chg)
        pct_changes.append(pct)
        pprev = pod_vals[i - 1]
        pchg = pod_vals[i] - pprev
        ppct = (pchg / pprev * 100) if pprev > 0 else float("inf")
        pod_changes.append(pchg)
        pod_pct_changes.append(ppct)
    else:
        changes.append(None)
        pct_changes.append(None)
        pod_changes.append(None)
        pod_pct_changes.append(None)
channel_detail["Depl Change vs LM"] = changes
channel_detail["% Change vs LM"] = pct_changes
channel_detail["PODs Change vs LM"] = pod_changes
channel_detail["PODs % Change"] = pod_pct_changes

# ON-PREMISE state data (from Depletions 05.01.26, samples/internal removed)
# Apr is now full month. "New Apr PODs" = retail accounts with 0 PODs in Nov-Mar but >0 PODs in Apr.
on_states = pd.DataFrame([
    {"State": "CA", "YTD Cases": 165.33, "YTD PODs": 89, "Mar Cases": 62.58, "Mar PODs": 37, "Apr Cases": 54.58, "Apr PODs": 35, "New Apr PODs": 24},
    {"State": "IL", "YTD Cases": 75.30, "YTD PODs": 76, "Mar Cases": 21.76, "Mar PODs": 26, "Apr Cases": 24.48, "Apr PODs": 10, "New Apr PODs": 8},
    {"State": "FL", "YTD Cases": 58.32, "YTD PODs": 37, "Mar Cases": 8.67, "Mar PODs": 12, "Apr Cases": 35.08, "Apr PODs": 11, "New Apr PODs": 10},
    {"State": "NY", "YTD Cases": 57.41, "YTD PODs": 27, "Mar Cases": 19.17, "Mar PODs": 12, "Apr Cases": 19.17, "Apr PODs": 11, "New Apr PODs": 4},
    {"State": "TX", "YTD Cases": 41.08, "YTD PODs": 25, "Mar Cases": 12.25, "Mar PODs": 6, "Apr Cases": 18.75, "Apr PODs": 13, "New Apr PODs": 11},
    {"State": "AZ", "YTD Cases": 40.06, "YTD PODs": 38, "Mar Cases": 6.75, "Mar PODs": 9, "Apr Cases": 10.25, "Apr PODs": 7, "New Apr PODs": 1},
    {"State": "NJ", "YTD Cases": 36.25, "YTD PODs": 15, "Mar Cases": 9.00, "Mar PODs": 6, "Apr Cases": 6.25, "Apr PODs": 6, "New Apr PODs": 3},
    {"State": "CO", "YTD Cases": 10.50, "YTD PODs": 4, "Mar Cases": 4.50, "Mar PODs": 2, "Apr Cases": 5.00, "Apr PODs": 3, "New Apr PODs": 1},
    {"State": "MD", "YTD Cases": 9.08, "YTD PODs": 8, "Mar Cases": 3.16, "Mar PODs": 4, "Apr Cases": 5.25, "Apr PODs": 4, "New Apr PODs": 2},
    {"State": "VA", "YTD Cases": 8.16, "YTD PODs": 9, "Mar Cases": 4.08, "Mar PODs": 5, "Apr Cases": 3.00, "Apr PODs": 2, "New Apr PODs": 2},
    {"State": "OH", "YTD Cases": 7.81, "YTD PODs": 13, "Mar Cases": 2.50, "Mar PODs": 4, "Apr Cases": 1.66, "Apr PODs": 6, "New Apr PODs": 5},
    {"State": "NC", "YTD Cases": 6.24, "YTD PODs": 7, "Mar Cases": 0.33, "Mar PODs": 2, "Apr Cases": 5.91, "Apr PODs": 5, "New Apr PODs": 5},
    {"State": "NV", "YTD Cases": 6.00, "YTD PODs": 1, "Mar Cases": 6.00, "Mar PODs": 1, "Apr Cases": 0, "Apr PODs": 0, "New Apr PODs": 0},
    {"State": "KY", "YTD Cases": 4.00, "YTD PODs": 2, "Mar Cases": 1.00, "Mar PODs": 1, "Apr Cases": 3.00, "Apr PODs": 1, "New Apr PODs": 1},
    {"State": "CT", "YTD Cases": 3.00, "YTD PODs": 3, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 2.00, "Apr PODs": 2, "New Apr PODs": 2},
    {"State": "DE", "YTD Cases": 2.08, "YTD PODs": 2, "Mar Cases": 1.00, "Mar PODs": 1, "Apr Cases": 1.00, "Apr PODs": 1, "New Apr PODs": 0},
    {"State": "NM", "YTD Cases": 1.50, "YTD PODs": 5, "Mar Cases": 0.16, "Mar PODs": 2, "Apr Cases": 1.17, "Apr PODs": 2, "New Apr PODs": 2},
    {"State": "DC", "YTD Cases": 1.42, "YTD PODs": 4, "Mar Cases": 0.08, "Mar PODs": 1, "Apr Cases": 0, "Apr PODs": 0, "New Apr PODs": 0},
    {"State": "GA", "YTD Cases": 0.75, "YTD PODs": 2, "Mar Cases": 0.25, "Mar PODs": 1, "Apr Cases": 0.50, "Apr PODs": 1, "New Apr PODs": 1},
    {"State": "SC", "YTD Cases": 0.50, "YTD PODs": 1, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0.50, "Apr PODs": 1, "New Apr PODs": 1},
    {"State": "WA", "YTD Cases": 0.32, "YTD PODs": 4, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0.32, "Apr PODs": 4, "New Apr PODs": 4},
])

# OFF-PREMISE state data (from Depletions 05.01.26, samples/internal removed; Apr is full month)
off_states = pd.DataFrame([
    {"State": "CA", "YTD Cases": 407.17, "YTD PODs": 244, "Mar Cases": 120.00, "Mar PODs": 97, "Apr Cases": 80.17, "Apr PODs": 45, "New Apr PODs": 21},
    {"State": "NJ", "YTD Cases": 194.00, "YTD PODs": 66, "Mar Cases": 17.00, "Mar PODs": 11, "Apr Cases": 12.00, "Apr PODs": 7, "New Apr PODs": 1},
    {"State": "NY", "YTD Cases": 158.51, "YTD PODs": 59, "Mar Cases": 22.17, "Mar PODs": 16, "Apr Cases": 28.17, "Apr PODs": 17, "New Apr PODs": 7},
    {"State": "FL", "YTD Cases": 142.02, "YTD PODs": 53, "Mar Cases": 14.92, "Mar PODs": 21, "Apr Cases": 26.26, "Apr PODs": 19, "New Apr PODs": 10},
    {"State": "IL", "YTD Cases": 133.29, "YTD PODs": 85, "Mar Cases": 46.72, "Mar PODs": 29, "Apr Cases": 24.24, "Apr PODs": 23, "New Apr PODs": 8},
    {"State": "VA", "YTD Cases": 55.58, "YTD PODs": 81, "Mar Cases": 43.50, "Mar PODs": 79, "Apr Cases": 5.50, "Apr PODs": 9, "New Apr PODs": 0},
    {"State": "CT", "YTD Cases": 41.99, "YTD PODs": 28, "Mar Cases": 30.16, "Mar PODs": 17, "Apr Cases": 8.17, "Apr PODs": 8, "New Apr PODs": 4},
    {"State": "TX", "YTD Cases": 40.85, "YTD PODs": 25, "Mar Cases": 19.66, "Mar PODs": 17, "Apr Cases": 11.58, "Apr PODs": 13, "New Apr PODs": 5},
    {"State": "NC", "YTD Cases": 39.71, "YTD PODs": 94, "Mar Cases": 31.31, "Mar PODs": 74, "Apr Cases": 8.40, "Apr PODs": 29, "New Apr PODs": 20},
    {"State": "DE", "YTD Cases": 21.00, "YTD PODs": 16, "Mar Cases": 13.00, "Mar PODs": 13, "Apr Cases": 0, "Apr PODs": 0, "New Apr PODs": 0},
    {"State": "OH", "YTD Cases": 19.99, "YTD PODs": 19, "Mar Cases": 4.58, "Mar PODs": 8, "Apr Cases": 4.09, "Apr PODs": 6, "New Apr PODs": 1},
    {"State": "MD", "YTD Cases": 17.99, "YTD PODs": 16, "Mar Cases": 8.00, "Mar PODs": 8, "Apr Cases": 4.00, "Apr PODs": 4, "New Apr PODs": 1},
    {"State": "SC", "YTD Cases": 13.58, "YTD PODs": 24, "Mar Cases": 8.33, "Mar PODs": 18, "Apr Cases": 5.25, "Apr PODs": 6, "New Apr PODs": 6},
    {"State": "GA", "YTD Cases": 10.50, "YTD PODs": 7, "Mar Cases": 3.00, "Mar PODs": 3, "Apr Cases": 7.00, "Apr PODs": 2, "New Apr PODs": 2},
    {"State": "CO", "YTD Cases": 8.57, "YTD PODs": 15, "Mar Cases": 1.74, "Mar PODs": 6, "Apr Cases": 2.42, "Apr PODs": 5, "New Apr PODs": 4},
    {"State": "KY", "YTD Cases": 7.00, "YTD PODs": 4, "Mar Cases": 3.00, "Mar PODs": 1, "Apr Cases": 1.00, "Apr PODs": 1, "New Apr PODs": 1},
    {"State": "DC", "YTD Cases": 4.00, "YTD PODs": 3, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 4.00, "Apr PODs": 3, "New Apr PODs": 3},
    {"State": "AZ", "YTD Cases": 1.50, "YTD PODs": 3, "Mar Cases": 1.00, "Mar PODs": 1, "Apr Cases": 0.25, "Apr PODs": 1, "New Apr PODs": 1},
    {"State": "NM", "YTD Cases": 0.65, "YTD PODs": 5, "Mar Cases": 0.08, "Mar PODs": 1, "Apr Cases": 0.24, "Apr PODs": 3, "New Apr PODs": 3},
    {"State": "WA", "YTD Cases": 0.08, "YTD PODs": 1, "Mar Cases": 0, "Mar PODs": 0, "Apr Cases": 0.08, "Apr PODs": 1, "New Apr PODs": 1},
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

# ── SHIPMENTS & REVENUE DATA ────────────────────────────────────────────────
ship_monthly_cases = pd.DataFrame([
    {"Month": "Dec '25", "Cases": 2302},
    {"Month": "Jan '26", "Cases": 1447},
    {"Month": "Feb '26", "Cases": 683},
    {"Month": "Mar '26", "Cases": 379},
])

ship_monthly_revenue = pd.DataFrame([
    {"Month": "Dec '25", "Revenue": 71539},
    {"Month": "Jan '26", "Revenue": 47005},
    {"Month": "Feb '26", "Revenue": 18488},
    {"Month": "Mar '26", "Revenue": 11073},
])

ship_monthly_rev_per_case = pd.DataFrame([
    {"Month": "Dec '25", "Rev/Case": 31.1},
    {"Month": "Jan '26", "Rev/Case": 32.5},
    {"Month": "Feb '26", "Rev/Case": 27.1},
    {"Month": "Mar '26", "Rev/Case": 29.2},
])

# Credit memo breakdown by month (from Payment Process Excel)
ship_monthly_credits = pd.DataFrame([
    {"Month": "Dec '25", "Credit Memo": 0},
    {"Month": "Jan '26", "Credit Memo": -325.44},
    {"Month": "Feb '26", "Credit Memo": -2123.16},
    {"Month": "Mar '26", "Credit Memo": -11074.88},
])

ship_monthly_net = pd.DataFrame([
    {"Month": "Dec '25", "Net Revenue": 71538.92},
    {"Month": "Jan '26", "Net Revenue": 46680.02},
    {"Month": "Feb '26", "Net Revenue": 16365.00},
    {"Month": "Mar '26", "Net Revenue": -1.60},
])

# Top accounts — chain data from Ethica 05.01.26 (Apr full month, samples/internal removed)
top_accounts = pd.DataFrame([
    {"Account": "BevMo!", "Premise": "Off", "States": "CA", "YTD Cases": 160.00, "YTD PODs": 145, "Mar Cases": 50.00, "Apr Cases": 9.00},
    {"Account": "Eataly", "Premise": "On", "States": "CA, IL, NJ, NY, TX, FL", "YTD Cases": 119.08, "YTD PODs": 12, "Mar Cases": 50.00, "Apr Cases": 42.08},
    {"Account": "Total Wine & More", "Premise": "Off", "States": "Multi", "YTD Cases": 98.60, "YTD PODs": 57, "Mar Cases": 34.16, "Apr Cases": 26.01},
    {"Account": "Food Lion", "Premise": "Off", "States": "Multi", "YTD Cases": 78.48, "YTD PODs": 162, "Mar Cases": 72.23, "Apr Cases": 6.25},
    {"Account": "Gary's Wine", "Premise": "Off", "States": "NJ", "YTD Cases": 74.00, "YTD PODs": 3, "Mar Cases": 1.00, "Apr Cases": 1.00},
    {"Account": "Milam's Markets", "Premise": "Off", "States": "FL", "YTD Cases": 72.00, "YTD PODs": 6, "Mar Cases": 0, "Apr Cases": 0},
    {"Account": "Albertsons Warehouse", "Premise": "Off", "States": "CA", "YTD Cases": 67.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 22.00},
    {"Account": "Binny's", "Premise": "Off", "States": "IL", "YTD Cases": 58.91, "YTD PODs": 40, "Mar Cases": 8.40, "Apr Cases": 14.24},
    {"Account": "Stew Leonard's Wines", "Premise": "Off", "States": "NJ, NY, CT", "YTD Cases": 49.00, "YTD PODs": 4, "Mar Cases": 17.00, "Apr Cases": 2.00},
    {"Account": "Wine.com", "Premise": "Off", "States": "Multi", "YTD Cases": 47.00, "YTD PODs": 5, "Mar Cases": 4.00, "Apr Cases": 13.00},
    {"Account": "Stew Leonard's", "Premise": "Off", "States": "NJ", "YTD Cases": 30.00, "YTD PODs": 2, "Mar Cases": 2.00, "Apr Cases": 1.00},
    {"Account": "VIN Chicago", "Premise": "Off", "States": "IL", "YTD Cases": 20.16, "YTD PODs": 2, "Mar Cases": 20.00, "Apr Cases": 0},
    {"Account": "Oliver's Market", "Premise": "Off", "States": "CA", "YTD Cases": 11.00, "YTD PODs": 4, "Mar Cases": 11.00, "Apr Cases": 0},
    {"Account": "BevMax", "Premise": "Off", "States": "CT", "YTD Cases": 11.00, "YTD PODs": 9, "Mar Cases": 8.00, "Apr Cases": 2.00},
    {"Account": "ShopRite Liquors", "Premise": "Off", "States": "NJ", "YTD Cases": 11.00, "YTD PODs": 5, "Mar Cases": 5.00, "Apr Cases": 0},
    {"Account": "Spec's Wine & Spirits", "Premise": "Off", "States": "TX", "YTD Cases": 9.08, "YTD PODs": 8, "Mar Cases": 7.00, "Apr Cases": 2.08},
    {"Account": "Gopuff", "Premise": "Off", "States": "FL", "YTD Cases": 6.00, "YTD PODs": 6, "Mar Cases": 0, "Apr Cases": 0},
    {"Account": "Spec's Wholesale", "Premise": "Off", "States": "TX", "YTD Cases": 5.17, "YTD PODs": 2, "Mar Cases": 3.00, "Apr Cases": 2.00},
    {"Account": "Curio Collection by Hilton", "Premise": "On", "States": "Multi", "YTD Cases": 4.17, "YTD PODs": 1, "Mar Cases": 0.17, "Apr Cases": 2.00},
    {"Account": "H-E-B Central Market", "Premise": "Off", "States": "TX", "YTD Cases": 3.42, "YTD PODs": 4, "Mar Cases": 1.00, "Apr Cases": 2.25},
    {"Account": "ClubProcure", "Premise": "On", "States": "Multi", "YTD Cases": 3.41, "YTD PODs": 6, "Mar Cases": 1.08, "Apr Cases": 0},
    {"Account": "ShopRite Wines & Spirits", "Premise": "Off", "States": "NJ", "YTD Cases": 3.00, "YTD PODs": 3, "Mar Cases": 0, "Apr Cases": 0},
    {"Account": "Trader Joe's Liquor", "Premise": "Off", "States": "Multi", "YTD Cases": 3.00, "YTD PODs": 2, "Mar Cases": 0, "Apr Cases": 0},
    {"Account": "Invited", "Premise": "On", "States": "CA", "YTD Cases": 2.00, "YTD PODs": 1, "Mar Cases": 2.00, "Apr Cases": 0},
    {"Account": "Miraval", "Premise": "On", "States": "TX", "YTD Cases": 2.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 2.00},
])

# State-level top accounts for key 5 states (CA, TX, FL, NY, NJ) — from 04.24.26 tab (samples removed)
state_top_accounts = pd.DataFrame([
    # CA
    {"State": "CA", "Account": "BevMo!", "Premise": "Off", "YTD Cases": 160.00, "YTD PODs": 145, "Mar Cases": 50.00, "Apr Cases": 9.00},
    {"State": "CA", "Account": "Albertsons Warehouse", "Premise": "Off", "YTD Cases": 67.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 22.00},
    {"State": "CA", "Account": "Eataly", "Premise": "On", "YTD Cases": 23.00, "YTD PODs": 2, "Mar Cases": 13.00, "Apr Cases": 4.00},
    {"State": "CA", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 16.00, "YTD PODs": 10, "Mar Cases": 1.00, "Apr Cases": 5.00},
    {"State": "CA", "Account": "Wine.com", "Premise": "Off", "YTD Cases": 12.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 5.00},
    {"State": "CA", "Account": "Oliver's Market", "Premise": "Off", "YTD Cases": 11.00, "YTD PODs": 4, "Mar Cases": 11.00, "Apr Cases": 0},
    # TX
    {"State": "TX", "Account": "Eataly", "Premise": "On", "YTD Cases": 11.00, "YTD PODs": 2, "Mar Cases": 4.00, "Apr Cases": 7.00},
    {"State": "TX", "Account": "Spec's Wine & Spirits", "Premise": "Off", "YTD Cases": 9.08, "YTD PODs": 8, "Mar Cases": 7.00, "Apr Cases": 2.08},
    {"State": "TX", "Account": "Wine.com", "Premise": "Off", "YTD Cases": 8.00, "YTD PODs": 1, "Mar Cases": 1.00, "Apr Cases": 3.00},
    {"State": "TX", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 7.09, "YTD PODs": 3, "Mar Cases": 4.58, "Apr Cases": 1.08},
    {"State": "TX", "Account": "Spec's Wholesale", "Premise": "Off", "YTD Cases": 5.17, "YTD PODs": 2, "Mar Cases": 3.00, "Apr Cases": 2.00},
    {"State": "TX", "Account": "H-E-B Central Market", "Premise": "Off", "YTD Cases": 3.42, "YTD PODs": 4, "Mar Cases": 1.00, "Apr Cases": 2.25},
    {"State": "TX", "Account": "Miraval", "Premise": "On", "YTD Cases": 2.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 2.00},
    # FL
    {"State": "FL", "Account": "Milam's Markets", "Premise": "Off", "YTD Cases": 72.00, "YTD PODs": 6, "Mar Cases": 0, "Apr Cases": 0},
    {"State": "FL", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 24.93, "YTD PODs": 17, "Mar Cases": 9.33, "Apr Cases": 4.76},
    {"State": "FL", "Account": "Gopuff", "Premise": "Off", "YTD Cases": 6.00, "YTD PODs": 6, "Mar Cases": 0, "Apr Cases": 0},
    {"State": "FL", "Account": "Eataly", "Premise": "On", "YTD Cases": 3.08, "YTD PODs": 2, "Mar Cases": 3.00, "Apr Cases": 0.08},
    {"State": "FL", "Account": "Doris Italian Market", "Premise": "Off", "YTD Cases": 2.00, "YTD PODs": 1, "Mar Cases": 1.00, "Apr Cases": 1.00},
    {"State": "FL", "Account": "Soho House", "Premise": "On", "YTD Cases": 1.83, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0},
    # NY
    {"State": "NY", "Account": "Stew Leonard's Wines", "Premise": "Off", "YTD Cases": 30.00, "YTD PODs": 2, "Mar Cases": 0, "Apr Cases": 0},
    {"State": "NY", "Account": "Eataly", "Premise": "On", "YTD Cases": 20.00, "YTD PODs": 4, "Mar Cases": 11.00, "Apr Cases": 9.00},
    {"State": "NY", "Account": "Wine.com", "Premise": "Off", "YTD Cases": 19.00, "YTD PODs": 1, "Mar Cases": 1.00, "Apr Cases": 5.00},
    {"State": "NY", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 6.00, "YTD PODs": 1, "Mar Cases": 2.00, "Apr Cases": 3.00},
    {"State": "NY", "Account": "Hilton", "Premise": "On", "YTD Cases": 1.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0},
    # NJ
    {"State": "NJ", "Account": "Gary's Wine & Marketplace", "Premise": "Off", "YTD Cases": 74.00, "YTD PODs": 3, "Mar Cases": 1.00, "Apr Cases": 1.00},
    {"State": "NJ", "Account": "Stew Leonard's", "Premise": "Off", "YTD Cases": 30.00, "YTD PODs": 2, "Mar Cases": 2.00, "Apr Cases": 1.00},
    {"State": "NJ", "Account": "Total Wine & More", "Premise": "Off", "YTD Cases": 12.00, "YTD PODs": 4, "Mar Cases": 5.00, "Apr Cases": 2.00},
    {"State": "NJ", "Account": "ShopRite Liquors", "Premise": "Off", "YTD Cases": 11.00, "YTD PODs": 5, "Mar Cases": 5.00, "Apr Cases": 0},
    {"State": "NJ", "Account": "Eataly", "Premise": "On", "YTD Cases": 10.00, "YTD PODs": 1, "Mar Cases": 4.00, "Apr Cases": 2.00},
    {"State": "NJ", "Account": "Wine.com", "Premise": "Off", "YTD Cases": 4.00, "YTD PODs": 1, "Mar Cases": 0, "Apr Cases": 0},
])

# Top 10 Restaurants/Bars (clean — samples removed) from 05.01.26 tab
top_restaurants_bars = pd.DataFrame([
    {"Rank": 1, "Restaurant": "Eataly (Brew Pub)", "City": "Chicago", "State": "IL", "Chain": "Eataly", "Channel": "Restaurant", "YTD Cases": 52.00, "Mar": 15.00, "Apr": 20.00},
    {"Rank": 2, "Restaurant": "Eataly", "City": "Santa Clara", "State": "CA", "Chain": "Eataly", "Channel": "Restaurant", "YTD Cases": 16.00, "Mar": 10.00, "Apr": 0},
    {"Rank": 3, "Restaurant": "Marvito", "City": "West Hollywood", "State": "CA", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 13.00, "Mar": 5.00, "Apr": 5.00},
    {"Rank": 4, "Restaurant": "Lucia Pizzeria", "City": "Miami", "State": "FL", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 10.00, "Mar": 0, "Apr": 10.00},
    {"Rank": 5, "Restaurant": "In Cucina / Sam's Italian Deli", "City": "Fresno", "State": "CA", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 9.00, "Mar": 7.00, "Apr": 0},
    {"Rank": 6, "Restaurant": "Eataly NYC Flatiron", "City": "New York", "State": "NY", "Chain": "Eataly", "Channel": "Restaurant", "YTD Cases": 7.00, "Mar": 3.00, "Apr": 4.00},
    {"Rank": 7, "Restaurant": "Eataly", "City": "Los Angeles", "State": "CA", "Chain": "Eataly", "Channel": "Restaurant", "YTD Cases": 7.00, "Mar": 3.00, "Apr": 4.00},
    {"Rank": 8, "Restaurant": "Fino All Is Well Good As Gold", "City": "Denver", "State": "CO", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 6.50, "Mar": 3.50, "Apr": 3.00},
    {"Rank": 9, "Restaurant": "Wayward Fare", "City": "Brooklyn", "State": "NY", "Chain": "(independent)", "Channel": "Restaurant", "YTD Cases": 6.00, "Mar": 0, "Apr": 3.00},
    {"Rank": 10, "Restaurant": "Eataly (Shop)", "City": "Dallas", "State": "TX", "Chain": "Eataly", "Channel": "Restaurant", "YTD Cases": 6.00, "Mar": 0, "Apr": 6.00},
])

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

# Trade channel breakdown (Ethica 05.01.26, samples / internal accounts removed; Apr full month)
off_trade_channels = pd.DataFrame([
    {"Trade Channel": "Liquor / Package Store", "YTD Cases": 674.40, "Dec": 3.40, "Jan": 132.81, "Feb": 192.62, "Mar": 224.97, "Apr": 110.33},
    {"Trade Channel": "Supermarket", "YTD Cases": 330.72, "Dec": 0, "Jan": 51.50, "Feb": 86.66, "Mar": 122.72, "Apr": 69.84},
    {"Trade Channel": "Other Off Premise", "YTD Cases": 226.47, "Dec": 4.00, "Jan": 5.24, "Feb": 170.65, "Mar": 20.99, "Apr": 25.58},
    {"Trade Channel": "General Merchandise", "YTD Cases": 49.00, "Dec": 0, "Jan": 13.00, "Feb": 19.00, "Mar": 4.00, "Apr": 13.00},
    {"Trade Channel": "Wholesale Club", "YTD Cases": 15.17, "Dec": 0, "Jan": 0, "Feb": 4.00, "Mar": 8.00, "Apr": 3.17},
    {"Trade Channel": "Convenience / Gas", "YTD Cases": 8.67, "Dec": 1.00, "Jan": 0, "Feb": 1.25, "Mar": 4.83, "Apr": 1.59},
    {"Trade Channel": "Small Grocery Store", "YTD Cases": 6.00, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0, "Apr": 6.00},
    {"Trade Channel": "Fine Wine Store", "YTD Cases": 5.33, "Dec": 0, "Jan": 0, "Feb": 1.08, "Mar": 2.25, "Apr": 2.00},
    {"Trade Channel": "Non-Retail", "YTD Cases": 1.72, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0.41, "Apr": 1.31},
    {"Trade Channel": "Retail-Specialty Services", "YTD Cases": 0.50, "Dec": 0, "Jan": 0, "Feb": 0.50, "Mar": 0, "Apr": 0},
])

on_trade_channels = pd.DataFrame([
    {"Trade Channel": "Restaurant", "YTD Cases": 396.31, "Dec": 14.24, "Jan": 18.82, "Feb": 87.07, "Mar": 122.13, "Apr": 151.97},
    {"Trade Channel": "Bar / Tavern", "YTD Cases": 53.19, "Dec": 0.08, "Jan": 5.08, "Feb": 10.31, "Mar": 16.23, "Apr": 21.49},
    {"Trade Channel": "Other On Premise", "YTD Cases": 38.41, "Dec": 1.00, "Jan": 2.00, "Feb": 19.16, "Mar": 9.41, "Apr": 6.83},
    {"Trade Channel": "Golf / Country Club", "YTD Cases": 22.56, "Dec": 1.00, "Jan": 3.00, "Feb": 1.99, "Mar": 11.57, "Apr": 5.00},
    {"Trade Channel": "Hotel / Motel", "YTD Cases": 21.81, "Dec": 0, "Jan": 0.42, "Feb": 4.49, "Mar": 3.57, "Apr": 10.33},
    {"Trade Channel": "Special Event / Temp License", "YTD Cases": 2.00, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0, "Apr": 2.00},
    {"Trade Channel": "Concessionaire", "YTD Cases": 0.50, "Dec": 0, "Jan": 0, "Feb": 0.25, "Mar": 0, "Apr": 0.25},
    {"Trade Channel": "Fine Dining / White Tablecloth", "YTD Cases": 0.25, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0.25, "Apr": 0},
    {"Trade Channel": "Recreation / Entertainment", "YTD Cases": 0.08, "Dec": 0, "Jan": 0, "Feb": 0, "Mar": 0.08, "Apr": 0},
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
    ["Overview", "Shipments & Revenue", "Depletions", "Gopuff", "ReserveBar"],
    horizontal=True,
    label_visibility="collapsed",
)

st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# SHARED MONTH OPTIONS
# ══════════════════════════════════════════════════════════════════════════════
DEPL_MONTHS = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]
SHIP_MONTHS = ["Dec '25", "Jan '26", "Feb '26", "Mar '26"]
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
        st.markdown(kpi("Gross Revenue YTD", "$148,106", "Net: $134,582 · as of 3/31/26", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Cases Shipped YTD", "4,811", "Dec '25 - Mar '26", dark=True), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Total Depletions", f"{total_cases:,.2f}", f"Cases · samples excl · as of {DEPLETION_AS_OF}"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Gopuff YTD Units", "169", f"29 locations · as of {GOPUFF_AS_OF}"), unsafe_allow_html=True)

    with c5:
        st.markdown(kpi("ReserveBar Units", "86", "27 orders, $1.74K · as of 4/25/26"), unsafe_allow_html=True)

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

    # Channel breakdown table — redesigned with change vs LM
    section_title("Channel Breakdown")
    cd_filt = channel_detail[channel_detail["Short"].isin(ov_months)].copy()
    cd_display = cd_filt[["Month", "Total Depletions", "Depl Change vs LM", "% Change vs LM", "On-Premise", "Off-Premise"]].copy()

    fmt_map = {
        "Total Depletions": lambda v: f"{v:,.2f}",
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
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">1,223</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">TOTAL PODS</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">21</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">STATES</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SHIPMENTS & REVENUE
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Shipments & Revenue":
    sh_months = st.multiselect("Filter by Month", SHIP_MONTHS, default=SHIP_MONTHS, key="sh_months")
    sc_filt = ship_monthly_cases[ship_monthly_cases["Month"].isin(sh_months)]
    sr_filt = ship_monthly_revenue[ship_monthly_revenue["Month"].isin(sh_months)]
    srpc_filt = ship_monthly_rev_per_case[ship_monthly_rev_per_case["Month"].isin(sh_months)]
    scr_filt = ship_monthly_credits[ship_monthly_credits["Month"].isin(sh_months)]
    snet_filt = ship_monthly_net[ship_monthly_net["Month"].isin(sh_months)]

    filt_cases = int(sc_filt["Cases"].sum())
    filt_rev = int(sr_filt["Revenue"].sum())
    filt_credits = round(scr_filt["Credit Memo"].sum(), 2)
    filt_net = round(snet_filt["Net Revenue"].sum(), 2)
    filt_rpc = round(filt_rev / filt_cases, 0) if filt_cases > 0 else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(kpi("Cases Shipped", f"{filt_cases:,}", "Filtered period", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Gross Revenue", f"${filt_rev:,}", "Before credit memos"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Credit Memos", f"-${abs(filt_credits):,.0f}", "DAs, samples, other"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Net Revenue", f"${filt_net:,.0f}", "After credit memos"), unsafe_allow_html=True)
    with c5:
        st.markdown(kpi("Gross Rev / Case", f"${filt_rpc:.0f}", "Gross rev / cases shipped"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        section_title("Monthly Cases Shipped")
        fig = bar_chart(sc_filt, "Month", "Cases")
        fig.update_traces(text=sc_filt["Cases"].apply(lambda x: f"{x:,.0f}"), textposition="outside")
        fig.update_layout(height=320)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("Monthly Gross Revenue")
        fig = bar_chart(sr_filt, "Month", "Revenue")
        fig.update_traces(text=sr_filt["Revenue"].apply(lambda x: f"${x:,.0f}"), textposition="outside")
        fig.update_layout(height=320)
        st.plotly_chart(fig, use_container_width=True)

    # Monthly financial summary table
    section_title("Monthly Financial Summary")
    fin_table = pd.merge(sc_filt[["Month", "Cases"]], sr_filt, on="Month")
    fin_table = pd.merge(fin_table, scr_filt, on="Month")
    fin_table = pd.merge(fin_table, snet_filt, on="Month")
    fin_table = pd.merge(fin_table, srpc_filt, on="Month")
    fin_table = fin_table[["Month", "Cases", "Revenue", "Credit Memo", "Net Revenue", "Rev/Case"]]
    st.markdown(styled_table(fin_table, fmt={
        "Cases": lambda v: f"{int(v):,}",
        "Revenue": lambda v: f"${v:,.0f}",
        "Credit Memo": lambda v: f"${v:,.2f}" if v == 0 else f"-${abs(v):,.2f}",
        "Net Revenue": lambda v: f"${v:,.2f}",
        "Rev/Case": lambda v: f"${v:.1f}",
    }), unsafe_allow_html=True)

    if filt_credits < -5000:
        st.markdown(f"""
        <div class="highlight-banner">
            <div>
                <p style="margin:0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.15em; text-transform:uppercase;">Credit Memo Alert</p>
                <p style="margin:8px 0 0; font-size:16px; color:white; font-weight:700;">March credit memos (-$11,075) nearly offset gross revenue ($11,073)</p>
                <p style="margin:4px 0 0; font-size:13px; color:rgba(255,255,255,0.7);">Includes DAs, samples, POSM materials, demo tastings, and labeling costs</p>
            </div>
        </div>
        """, unsafe_allow_html=True)


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

    section_title("On-Premise vs Off-Premise by Month")
    st.plotly_chart(
        grouped_bar(cm_filt, "Month", "On-Premise", "Off-Premise", "On-Premise", "Off-Premise"),
        use_container_width=True,
    )

    # Monthly detail table — redesigned with change vs LM
    section_title("Monthly Depletion Detail")
    st.caption(f"All months full-month actuals · samples excluded · as of {DEPLETION_AS_OF}")
    cd_filt = channel_detail[channel_detail["Short"].isin(dp_months)].copy()
    cd_display = cd_filt[["Month", "Total Depletions", "Total PODs", "Depl Change vs LM", "% Change vs LM", "On-Premise", "Off-Premise"]].copy()
    st.markdown(styled_table(cd_display, fmt={
        "Total Depletions": lambda v: f"{v:,.2f}",
        "Total PODs": lambda v: f"{int(v):,}",
        "Depl Change vs LM": lambda v: change_fmt(v),
        "% Change vs LM": lambda v: pct_change_fmt(v),
        "On-Premise": lambda v: f"{v:,.2f}",
        "Off-Premise": lambda v: f"{v:,.2f}",
    }), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── State Performance — Apr (full) vs Mar (full) ──
    section_title("State Performance — Apr vs Mar (Full Month MoM)")
    st.caption(f"As of {DEPLETION_AS_OF}. Apr is now a complete month — apples-to-apples MoM comparison. PODs are cumulative: 'YTD PODs' = total unique distribution points active YTD; 'New Apr PODs' = retail accounts activated for the first time in April. Samples / internal accounts excluded.")

    state_view = st.radio(
        "View",
        ["Total", "On-Premise", "Off-Premise"],
        horizontal=True,
        key="state_view_toggle",
        label_visibility="collapsed",
    )

    on_f = on_states[on_states["State"].isin(dp_states)].copy()
    off_f = off_states[off_states["State"].isin(dp_states)].copy()

    sp_cols = ["Mar Cases", "Apr Cases", "YTD PODs", "New Apr PODs"]
    if state_view == "On-Premise":
        sp = on_f[["State"] + sp_cols].copy()
    elif state_view == "Off-Premise":
        sp = off_f[["State"] + sp_cols].copy()
    else:
        on_agg = on_f.groupby("State", as_index=False)[sp_cols].sum()
        off_agg = off_f.groupby("State", as_index=False)[sp_cols].sum()
        sp = pd.concat([on_agg, off_agg]).groupby("State", as_index=False).sum()

    sp = sp.sort_values("Apr Cases", ascending=False).reset_index(drop=True)

    sp_display = sp[["State", "Mar Cases", "Apr Cases", "YTD PODs", "New Apr PODs"]].copy()

    st.markdown(styled_table(sp_display, fmt={
        "Mar Cases": lambda v: f"{v:,.2f}",
        "Apr Cases": lambda v: f"{v:,.2f}",
        "YTD PODs": lambda v: f"{int(v)}",
        "New Apr PODs": lambda v: f"+{int(v)}" if v > 0 else "0",
    }), unsafe_allow_html=True)

    # ── State Drill-Down: Top accounts within key 5 states ──
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Top Accounts by Key State")
    st.caption(f"Top accounts within CA, TX, FL, NY, NJ — sorted by YTD cases · as of {DEPLETION_AS_OF} · Apr is full month · Samples excluded")

    drill_state = st.radio(
        "Drill-down state",
        ["CA", "TX", "FL", "NY", "NJ"],
        horizontal=True,
        key="state_drill",
        label_visibility="collapsed",
    )
    sda = state_top_accounts[state_top_accounts["State"] == drill_state].copy()
    sda["Chg vs LM"] = sda["Apr Cases"] - sda["Mar Cases"]
    sda["% Growth"] = sda.apply(
        lambda r: ((r["Apr Cases"] - r["Mar Cases"]) / r["Mar Cases"] * 100) if r["Mar Cases"] > 0 else (float("inf") if r["Apr Cases"] > 0 else 0),
        axis=1,
    )
    st.markdown(styled_table(
        sda[["Account", "Premise", "YTD Cases", "YTD PODs", "Mar Cases", "Apr Cases"]],
        fmt={
            "YTD Cases": lambda v: f"{v:,.2f}",
            "YTD PODs": lambda v: f"{int(v):,}",
            "Mar Cases": lambda v: f"{v:,.2f}",
            "Apr Cases": lambda v: f"{v:,.2f}",
        }
    ), unsafe_allow_html=True)

    # ── Top 10 Restaurants / Bars ──
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Top 10 Restaurants & Bars by YTD Depletions")
    st.caption(f"On-premise restaurants, bars, and fine-dining accounts · sorted by YTD cases · as of {DEPLETION_AS_OF} · Samples excluded")
    st.markdown(styled_table(
        top_restaurants_bars[["Rank", "Restaurant", "City", "State", "Chain", "Channel", "YTD Cases", "Mar", "Apr"]],
        fmt={
            "Rank": lambda v: str(v),
            "YTD Cases": lambda v: f"{v:,.2f}",
            "Mar": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Apr": lambda v: f"{v:,.2f}" if v > 0 else "—",
        }
    ), unsafe_allow_html=True)

    # Trade channel breakdown (Ethica 05.01.26, samples / internal accounts removed)
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Off-Premise by Trade Channel")
    st.caption(f"As of {DEPLETION_AS_OF} · Apr is full month · Samples / internal accounts excluded")
    st.markdown(styled_table(
        off_trade_channels[["Trade Channel", "YTD Cases", "Dec", "Jan", "Feb", "Mar", "Apr"]],
        fmt={
            "YTD Cases": lambda v: f"{v:,.2f}",
            "Dec": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Jan": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Feb": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Mar": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Apr": lambda v: f"{v:,.2f}" if v > 0 else "—",
        }
    ), unsafe_allow_html=True)

    section_title("On-Premise by Trade Channel")
    st.caption(f"As of {DEPLETION_AS_OF} · Apr is full month · Samples / internal accounts excluded")
    st.markdown(styled_table(
        on_trade_channels[["Trade Channel", "YTD Cases", "Dec", "Jan", "Feb", "Mar", "Apr"]],
        fmt={
            "YTD Cases": lambda v: f"{v:,.2f}",
            "Dec": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Jan": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Feb": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Mar": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Apr": lambda v: f"{v:,.2f}" if v > 0 else "—",
        }
    ), unsafe_allow_html=True)

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

    acct_display = ta_filt[["Account", "Premise", "States", "YTD Cases", "YTD PODs", "Mar Cases", "Apr Cases"]].copy()
    st.markdown(styled_table(acct_display, fmt={
        "YTD Cases": lambda v: f"{v:,.2f}",
        "YTD PODs": lambda v: f"{int(v):,}",
        "Mar Cases": lambda v: f"{v:,.2f}",
        "Apr Cases": lambda v: f"{v:,.2f}",
    }), unsafe_allow_html=True)


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

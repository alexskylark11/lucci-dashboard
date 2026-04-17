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
    <div style="display:flex; align-items:baseline;">
        <span class="lucci-title">LUCCI</span>
        <span class="lucci-subtitle">Lambrusco Reggiano DOC</span>
    </div>
    <p class="lucci-period">Sales Intelligence Dashboard</p>
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

grand_monthly = pd.DataFrame([
    {"Month": "Nov", "Cases": 1}, {"Month": "Dec", "Cases": 28.17},
    {"Month": "Jan", "Cases": 248.25}, {"Month": "Feb", "Cases": 634.83},
    {"Month": "Mar", "Cases": 490.67},
])

combined_monthly = pd.DataFrame([
    {"Month": "Nov", "On-Premise": 0, "Off-Premise": 1},
    {"Month": "Dec", "On-Premise": 16.33, "Off-Premise": 11.83},
    {"Month": "Jan", "On-Premise": 30.25, "Off-Premise": 207.08},
    {"Month": "Feb", "On-Premise": 128.33, "Off-Premise": 506.25},
    {"Month": "Mar", "On-Premise": 137.17, "Off-Premise": 353.5},
])

# Channel breakdown with change vs last month
channel_detail = pd.DataFrame([
    {"Month": "Mar 2026", "Short": "Mar", "Total Depletions": 490.67, "On-Premise": 137.17, "Off-Premise": 353.50},
    {"Month": "Feb 2026", "Short": "Feb", "Total Depletions": 634.83, "On-Premise": 128.33, "Off-Premise": 506.25},
    {"Month": "Jan 2026", "Short": "Jan", "Total Depletions": 248.25, "On-Premise": 30.25, "Off-Premise": 207.08},
    {"Month": "Dec 2025", "Short": "Dec", "Total Depletions": 28.17, "On-Premise": 16.33, "Off-Premise": 11.83},
    {"Month": "Nov 2025", "Short": "Nov", "Total Depletions": 1.00, "On-Premise": 0, "Off-Premise": 1.00},
])

# Compute change vs last month (previous row is prior month since sorted newest first)
depl_vals = channel_detail["Total Depletions"].tolist()
changes = []
pct_changes = []
for i in range(len(depl_vals)):
    if i < len(depl_vals) - 1:
        prev = depl_vals[i + 1]
        chg = depl_vals[i] - prev
        pct = (chg / prev * 100) if prev > 0 else float("inf")
        changes.append(chg)
        pct_changes.append(pct)
    else:
        changes.append(None)
        pct_changes.append(None)
channel_detail["Depl Change vs LM"] = changes
channel_detail["% Change vs LM"] = pct_changes

on_states = pd.DataFrame([
    {"State": "CA", "YTD Cases": 96, "YTD PODs": 58, "Mar Cases": 51.5, "Mar PODs": 28, "Feb Cases": 20.83, "Jan Cases": 20.67, "Dec Cases": 3},
    {"State": "IL", "YTD Cases": 49.92, "YTD PODs": 66, "Mar Cases": 20.83, "Mar PODs": 25, "Feb Cases": 25.5, "Jan Cases": 2.25, "Dec Cases": 1.33},
    {"State": "NY", "YTD Cases": 35.25, "YTD PODs": 21, "Mar Cases": 16.17, "Mar PODs": 10, "Feb Cases": 5.67, "Jan Cases": 2.42, "Dec Cases": 11},
    {"State": "FL", "YTD Cases": 29.83, "YTD PODs": 30, "Mar Cases": 11.25, "Mar PODs": 14, "Feb Cases": 16.5, "Jan Cases": 2.08, "Dec Cases": 0},
    {"State": "NJ", "YTD Cases": 29, "YTD PODs": 12, "Mar Cases": 8, "Mar PODs": 5, "Feb Cases": 19, "Jan Cases": 1, "Dec Cases": 1},
    {"State": "AZ", "YTD Cases": 28.83, "YTD PODs": 37, "Mar Cases": 5.75, "Mar PODs": 9, "Feb Cases": 23, "Jan Cases": 0.08, "Dec Cases": 0},
    {"State": "TX", "YTD Cases": 19.33, "YTD PODs": 14, "Mar Cases": 9.25, "Mar PODs": 5, "Feb Cases": 9.08, "Jan Cases": 1, "Dec Cases": 0},
    {"State": "OH", "YTD Cases": 5.17, "YTD PODs": 8, "Mar Cases": 1.5, "Mar PODs": 4, "Feb Cases": 3.42, "Jan Cases": 0.25, "Dec Cases": 0},
    {"State": "CO", "YTD Cases": 4.5, "YTD PODs": 3, "Mar Cases": 3.5, "Mar PODs": 2, "Feb Cases": 1, "Jan Cases": 0, "Dec Cases": 0},
    {"State": "MD", "YTD Cases": 4.42, "YTD PODs": 11, "Mar Cases": 3.42, "Mar PODs": 7, "Feb Cases": 1, "Jan Cases": 0, "Dec Cases": 0},
    {"State": "NV", "YTD Cases": 4, "YTD PODs": 1, "Mar Cases": 4, "Mar PODs": 1, "Feb Cases": 0, "Jan Cases": 0, "Dec Cases": 0},
    {"State": "VA", "YTD Cases": 2.17, "YTD PODs": 4, "Mar Cases": 1.08, "Mar PODs": 2, "Feb Cases": 1.08, "Jan Cases": 0, "Dec Cases": 0},
    {"State": "DC", "YTD Cases": 1.42, "YTD PODs": 4, "Mar Cases": 0.08, "Mar PODs": 1, "Feb Cases": 1.17, "Jan Cases": 0.17, "Dec Cases": 0},
    {"State": "CT", "YTD Cases": 1, "YTD PODs": 1, "Mar Cases": 0, "Mar PODs": 0, "Feb Cases": 1, "Jan Cases": 0, "Dec Cases": 0},
    {"State": "DE", "YTD Cases": 0.58, "YTD PODs": 3, "Mar Cases": 0.33, "Mar PODs": 1, "Feb Cases": 0.08, "Jan Cases": 0.17, "Dec Cases": 0},
    {"State": "NC", "YTD Cases": 0.33, "YTD PODs": 2, "Mar Cases": 0.33, "Mar PODs": 2, "Feb Cases": 0, "Jan Cases": 0, "Dec Cases": 0},
    {"State": "NM", "YTD Cases": 0.33, "YTD PODs": 3, "Mar Cases": 0.17, "Mar PODs": 2, "Feb Cases": 0, "Jan Cases": 0.17, "Dec Cases": 0},
])

off_states = pd.DataFrame([
    {"State": "CA", "YTD Cases": 310.33, "YTD PODs": 225, "Mar Cases": 100.33, "Mar PODs": 97, "Feb Cases": 41.75, "Jan Cases": 165.17},
    {"State": "NJ", "YTD Cases": 199.58, "YTD PODs": 68, "Mar Cases": 20.33, "Mar PODs": 13, "Feb Cases": 170.08, "Jan Cases": 3.83},
    {"State": "NY", "YTD Cases": 138.17, "YTD PODs": 69, "Mar Cases": 24.58, "Mar PODs": 16, "Feb Cases": 99.08, "Jan Cases": 14.5},
    {"State": "FL", "YTD Cases": 117.08, "YTD PODs": 47, "Mar Cases": 16.5, "Mar PODs": 23, "Feb Cases": 90.25, "Jan Cases": 10.33},
    {"State": "IL", "YTD Cases": 101.92, "YTD PODs": 74, "Mar Cases": 41.58, "Mar PODs": 24, "Feb Cases": 49.75, "Jan Cases": 6.17},
    {"State": "VA", "YTD Cases": 51.5, "YTD PODs": 96, "Mar Cases": 43.33, "Mar PODs": 87, "Feb Cases": 8.17, "Jan Cases": 0},
    {"State": "CT", "YTD Cases": 33.83, "YTD PODs": 24, "Mar Cases": 30.17, "Mar PODs": 17, "Feb Cases": 3.67, "Jan Cases": 0},
    {"State": "TX", "YTD Cases": 25.25, "YTD PODs": 19, "Mar Cases": 15.67, "Mar PODs": 16, "Feb Cases": 8.5, "Jan Cases": 1.08},
    {"State": "NC", "YTD Cases": 22.58, "YTD PODs": 52, "Mar Cases": 22.58, "Mar PODs": 52, "Feb Cases": 0, "Jan Cases": 0},
    {"State": "DE", "YTD Cases": 21.58, "YTD PODs": 17, "Mar Cases": 13.5, "Mar PODs": 13, "Feb Cases": 7, "Jan Cases": 1.08},
    {"State": "MD", "YTD Cases": 20.08, "YTD PODs": 16, "Mar Cases": 7, "Mar PODs": 7, "Feb Cases": 12.75, "Jan Cases": 0.33},
    {"State": "OH", "YTD Cases": 15.92, "YTD PODs": 18, "Mar Cases": 4.58, "Mar PODs": 8, "Feb Cases": 9.83, "Jan Cases": 1.5},
    {"State": "SC", "YTD Cases": 10.67, "YTD PODs": 23, "Mar Cases": 10.67, "Mar PODs": 23, "Feb Cases": 0, "Jan Cases": 0},
    {"State": "CO", "YTD Cases": 6, "YTD PODs": 10, "Mar Cases": 1.58, "Mar PODs": 4, "Feb Cases": 1.33, "Jan Cases": 3.08},
    {"State": "DC", "YTD Cases": 3, "YTD PODs": 1, "Mar Cases": 0, "Mar PODs": 0, "Feb Cases": 3, "Jan Cases": 0},
    {"State": "GA", "YTD Cases": 1.5, "YTD PODs": 3, "Mar Cases": 1, "Mar PODs": 1, "Feb Cases": 0.5, "Jan Cases": 0},
    {"State": "NM", "YTD Cases": 0.42, "YTD PODs": 2, "Mar Cases": 0.08, "Mar PODs": 1, "Feb Cases": 0.33, "Jan Cases": 0},
    {"State": "AZ", "YTD Cases": 0.25, "YTD PODs": 1, "Mar Cases": 0, "Mar PODs": 0, "Feb Cases": 0.25, "Jan Cases": 0},
])

# Add change vs last month to state data
for df in [on_states, off_states]:
    df["Depl Chg vs LM"] = df["Mar Cases"] - df["Feb Cases"]
    df["% Growth vs LM"] = df.apply(
        lambda r: ((r["Mar Cases"] - r["Feb Cases"]) / r["Feb Cases"] * 100) if r["Feb Cases"] > 0 else (float("inf") if r["Mar Cases"] > 0 else 0),
        axis=1,
    )

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

# ── GOPUFF DATA (Updated from March 2026 Excel) ─────────────────────────────
gopuff_monthly = pd.DataFrame([
    {"Month": "Jan", "Units": 11},
    {"Month": "Feb", "Units": 70},
    {"Month": "Mar", "Units": 59},
])

gopuff_states = pd.DataFrame([
    {"State": "NY", "Units": 96, "Pct": 68.6, "Locations": 6},
    {"State": "CA", "Units": 30, "Pct": 21.4, "Locations": 18},
    {"State": "FL", "Units": 14, "Pct": 10.0, "Locations": 5},
])

gopuff_top_locations = pd.DataFrame([
    {"Location": "JFK New York 880", "State": "NY", "YTD": 28},
    {"Location": "JFK Brooklyn 554", "State": "NY", "YTD": 27},
    {"Location": "JFK New York 975", "State": "NY", "YTD": 24},
    {"Location": "JFK New York 807", "State": "NY", "YTD": 10},
    {"Location": "BUR Pasadena 416", "State": "CA", "YTD": 9},
    {"Location": "JFK Brooklyn 629", "State": "NY", "YTD": 6},
    {"Location": "MIA Miami 183", "State": "FL", "YTD": 5},
    {"Location": "MIA Miami Beach 911", "State": "FL", "YTD": 4},
    {"Location": "SAN Point Loma 446", "State": "CA", "YTD": 3},
    {"Location": "MIA Miami 330", "State": "FL", "YTD": 3},
])

gopuff_location_detail = pd.DataFrame([
    {"Rank": 1, "Location": "JFK_New-York_880", "ST": "NY", "Jan": 0, "Feb": 11, "Mar": 17, "YTD": 28},
    {"Rank": 2, "Location": "JFK_Brooklyn_554", "ST": "NY", "Jan": 4, "Feb": 10, "Mar": 13, "YTD": 27},
    {"Rank": 3, "Location": "JFK_New-York_975", "ST": "NY", "Jan": 4, "Feb": 9, "Mar": 11, "YTD": 24},
    {"Rank": 4, "Location": "JFK_New-York_807", "ST": "NY", "Jan": 0, "Feb": 3, "Mar": 7, "YTD": 10},
    {"Rank": 5, "Location": "BUR_Pasadena_416", "ST": "CA", "Jan": 0, "Feb": 9, "Mar": 0, "YTD": 9},
    {"Rank": 6, "Location": "JFK_Brooklyn_629", "ST": "NY", "Jan": 2, "Feb": 4, "Mar": 0, "YTD": 6},
    {"Rank": 7, "Location": "MIA_Miami_183", "ST": "FL", "Jan": 0, "Feb": 4, "Mar": 1, "YTD": 5},
    {"Rank": 8, "Location": "MIA_Miami-Beach_911", "ST": "FL", "Jan": 0, "Feb": 3, "Mar": 1, "YTD": 4},
    {"Rank": 9, "Location": "SAN_Point-Loma_446", "ST": "CA", "Jan": 0, "Feb": 3, "Mar": 0, "YTD": 3},
    {"Rank": 10, "Location": "MIA_Miami_330", "ST": "FL", "Jan": 0, "Feb": 2, "Mar": 1, "YTD": 3},
    {"Rank": 11, "Location": "OAK_Danville_487", "ST": "CA", "Jan": 0, "Feb": 2, "Mar": 0, "YTD": 2},
    {"Rank": 12, "Location": "SAN_La-Mesa_404", "ST": "CA", "Jan": 0, "Feb": 0, "Mar": 2, "YTD": 2},
    {"Rank": 13, "Location": "MIA_Miami_376", "ST": "FL", "Jan": 1, "Feb": 0, "Mar": 0, "YTD": 1},
    {"Rank": 14, "Location": "SFO_Colma_405", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "YTD": 1},
    {"Rank": 15, "Location": "LAX_Santa-Monica_427", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "YTD": 1},
    {"Rank": 16, "Location": "SFO_San-Francisco_434", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "YTD": 1},
    {"Rank": 17, "Location": "SMF_Sacramento_445", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "YTD": 1},
    {"Rank": 18, "Location": "SJC_San-Jose_459", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "YTD": 1},
    {"Rank": 19, "Location": "LAX_Torrance_462", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "YTD": 1},
    {"Rank": 20, "Location": "OAK_San-Leandro_497", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "YTD": 1},
    {"Rank": 21, "Location": "RDD_Redding_777", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "YTD": 1},
    {"Rank": 22, "Location": "SAN_La-Jolla_1016", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "YTD": 1},
    {"Rank": 23, "Location": "SJC_Los-Altos_1019", "ST": "CA", "Jan": 0, "Feb": 1, "Mar": 0, "YTD": 1},
    {"Rank": 24, "Location": "OAK_Oakland_403", "ST": "CA", "Jan": 0, "Feb": 0, "Mar": 1, "YTD": 1},
    {"Rank": 25, "Location": "LAX_Culver-City_423", "ST": "CA", "Jan": 0, "Feb": 0, "Mar": 1, "YTD": 1},
    {"Rank": 26, "Location": "BUR_Glendale_495", "ST": "CA", "Jan": 0, "Feb": 0, "Mar": 1, "YTD": 1},
    {"Rank": 27, "Location": "SFO_San-Mateo_496", "ST": "CA", "Jan": 0, "Feb": 0, "Mar": 1, "YTD": 1},
    {"Rank": 28, "Location": "MIA_Miami_602", "ST": "FL", "Jan": 0, "Feb": 0, "Mar": 1, "YTD": 1},
    {"Rank": 29, "Location": "JFK_New-York_839", "ST": "NY", "Jan": 0, "Feb": 0, "Mar": 1, "YTD": 1},
])

# ── RESERVEBAR DATA ──────────────────────────────────────────────────────────
rb_order_range = pd.DataFrame([
    {"Range": "<$100", "Pct": 65.2}, {"Range": "$100-200", "Pct": 26.1},
    {"Range": "$200-500", "Pct": 4.3}, {"Range": "$500-1K", "Pct": 4.3},
    {"Range": "$1K-2K", "Pct": 0}, {"Range": ">$2K", "Pct": 0},
])

rb_dow = pd.DataFrame([
    {"Day": "Mon", "Pct": 8.7}, {"Day": "Tue", "Pct": 8.7},
    {"Day": "Wed", "Pct": 17.4}, {"Day": "Thu", "Pct": 21.7},
    {"Day": "Fri", "Pct": 26.1}, {"Day": "Sat", "Pct": 13.0},
    {"Day": "Sun", "Pct": 4.3},
])

rb_discounts = pd.DataFrame([
    {"Code": "shiplucci", "Orders": 7, "Share": "58%"},
    {"Code": "lastminlove", "Orders": 2, "Share": "17%"},
    {"Code": "cheers10", "Orders": 1, "Share": "8%"},
    {"Code": "reservebar10", "Orders": 1, "Share": "8%"},
    {"Code": "feb26 codes", "Orders": 1, "Share": "8%"},
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

# Top accounts — REAL chain data from Ethica depletion report (thru 3/11/2026)
top_accounts = pd.DataFrame([
    {"Account": "BevMo!", "Premise": "Off", "States": "CA", "YTD Cases": 102.00, "Feb Cases": 0, "Mar Cases": 1.00},
    {"Account": "Stew Leonard's", "Premise": "Off", "States": "NJ, NY, CT", "YTD Cases": 74.00, "Feb Cases": 27.00, "Mar Cases": 17.00},
    {"Account": "Milam's Markets", "Premise": "Off", "States": "FL", "YTD Cases": 72.00, "Feb Cases": 72.00, "Mar Cases": 0},
    {"Account": "Gary's Wine", "Premise": "Off", "States": "NJ", "YTD Cases": 72.00, "Feb Cases": 72.00, "Mar Cases": 0},
    {"Account": "Total Wine & More", "Premise": "Off", "States": "Multi", "YTD Cases": 46.16, "Feb Cases": 14.59, "Mar Cases": 10.75},
    {"Account": "Albertsons", "Premise": "Off", "States": "CA", "YTD Cases": 45.00, "Feb Cases": 0, "Mar Cases": 0},
    {"Account": "Eataly", "Premise": "On", "States": "CA, IL, NJ, TX", "YTD Cases": 43.00, "Feb Cases": 20.00, "Mar Cases": 8.00},
    {"Account": "Binny's", "Premise": "Off", "States": "IL", "YTD Cases": 34.42, "Feb Cases": 34.17, "Mar Cases": 0.17},
    {"Account": "Wine.com", "Premise": "Off", "States": "Multi", "YTD Cases": 28.00, "Feb Cases": 17.00, "Mar Cases": 0},
    {"Account": "VIN Chicago", "Premise": "Off", "States": "IL", "YTD Cases": 20.17, "Feb Cases": 0, "Mar Cases": 20.00},
    {"Account": "ShopRite", "Premise": "Off", "States": "NJ", "YTD Cases": 16.00, "Feb Cases": 7.00, "Mar Cases": 5.00},
    {"Account": "Armanetti", "Premise": "Off", "States": "IL", "YTD Cases": 12.00, "Feb Cases": 4.00, "Mar Cases": 1.00},
    {"Account": "Spec's", "Premise": "Off", "States": "TX", "YTD Cases": 9.17, "Feb Cases": 0.17, "Mar Cases": 7.00},
    {"Account": "BevMax", "Premise": "Off", "States": "CT", "YTD Cases": 8.00, "Feb Cases": 1.00, "Mar Cases": 7.00},
    {"Account": "Gopuff", "Premise": "Off", "States": "FL", "YTD Cases": 6.00, "Feb Cases": 0, "Mar Cases": 0},
])

# Trade channel breakdown (from Ethica depletion report thru 3/11/2026)
off_trade_channels = pd.DataFrame([
    {"Trade Channel": "Liquor / Package Store", "YTD Cases": 518.58, "Nov": 0, "Dec": 5.42, "Jan": 130.41, "Feb": 260.09, "Mar": 122.65},
    {"Trade Channel": "Other Off Premise", "YTD Cases": 262.58, "Nov": 1, "Dec": 5.75, "Jan": 31.58, "Feb": 192.75, "Mar": 31.5},
    {"Trade Channel": "Supermarket", "YTD Cases": 149.50, "Nov": 0, "Dec": 0, "Jan": 51.5, "Feb": 87.33, "Mar": 10.67},
    {"Trade Channel": "General Merchandise", "YTD Cases": 34.00, "Nov": 0, "Dec": 0, "Jan": 13.0, "Feb": 19.0, "Mar": 2.0},
    {"Trade Channel": "Wholesale Club", "YTD Cases": 5.25, "Nov": 0, "Dec": 0, "Jan": 0, "Feb": 4.0, "Mar": 1.25},
    {"Trade Channel": "Fine Wine Store", "YTD Cases": 3.08, "Nov": 0, "Dec": 0, "Jan": 0, "Feb": 1.08, "Mar": 2.0},
    {"Trade Channel": "Convenience / Gas", "YTD Cases": 3.58, "Nov": 0, "Dec": 1.0, "Jan": 0, "Feb": 1.25, "Mar": 1.33},
    {"Trade Channel": "Non-Retail", "YTD Cases": 6.75, "Nov": 0, "Dec": 2.17, "Jan": 0.58, "Feb": 3.0, "Mar": 1.0},
])

on_trade_channels = pd.DataFrame([
    {"Trade Channel": "Restaurant", "YTD Cases": 147.67, "Nov": 0, "Dec": 14.25, "Jan": 18.83, "Feb": 86.58, "Mar": 28.0},
    {"Trade Channel": "Bar / Tavern", "YTD Cases": 18.75, "Nov": 0, "Dec": 0.08, "Jan": 5.08, "Feb": 10.33, "Mar": 4.25},
    {"Trade Channel": "Other On Premise", "YTD Cases": 30.91, "Nov": 0, "Dec": 1.0, "Jan": 1.92, "Feb": 24.08, "Mar": 3.92},
    {"Trade Channel": "Hotel / Motel", "YTD Cases": 6.24, "Nov": 0, "Dec": 0, "Jan": 0.42, "Feb": 4.49, "Mar": 1.33},
    {"Trade Channel": "Golf / Country Club", "YTD Cases": 9.33, "Nov": 0, "Dec": 1.0, "Jan": 4.0, "Feb": 2.0, "Mar": 1.41},
    {"Trade Channel": "Concessionaire", "YTD Cases": 0.25, "Nov": 0, "Dec": 0, "Jan": 0, "Feb": 0.25, "Mar": 0},
])
top_accounts["Chg vs LM"] = top_accounts["Mar Cases"] - top_accounts["Feb Cases"]
top_accounts["% Growth"] = top_accounts.apply(
    lambda r: ((r["Mar Cases"] - r["Feb Cases"]) / r["Feb Cases"] * 100) if r["Feb Cases"] > 0 else (float("inf") if r["Mar Cases"] > 0 else 0),
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
DEPL_MONTHS = ["Nov", "Dec", "Jan", "Feb", "Mar"]
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
        st.markdown(kpi("Gross Revenue YTD", "$148,106", "Net: $134,582 after credits", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Cases Shipped YTD", "4,811", "Dec '25 - Mar '26", dark=True), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Total Depletions", f"{total_cases:,.2f}", "Cases - filtered period"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Gopuff YTD Units", "140", "29 locations, 3 states"), unsafe_allow_html=True)
    with c5:
        st.markdown(kpi("ReserveBar Units", "73", "23 orders, $1.48K revenue"), unsafe_allow_html=True)

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
            <p style="margin:0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.15em; text-transform:uppercase;">Filtered Period Summary</p>
            <p style="margin:8px 0 0; font-size:18px; color:white; font-weight:900; letter-spacing:0.02em;">Lucci performance across all channels</p>
            <p style="margin:4px 0 0; font-size:13px; color:rgba(255,255,255,0.7);">{total_cases:,.2f} depletion cases &middot; {total_on:,.2f} on-premise &middot; {total_off:,.2f} off-premise</p>
        </div>
        <div style="display:flex; gap:32px; flex-shrink:0;">
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">{total_cases:,.1f}</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">TOTAL CASES</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">1,046</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">TOTAL PODS</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">17+</p>
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
        st.markdown(kpi("Total YTD (Cases)", f"{total_all:,.2f}", "Filtered period", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Total PODs", f"{total_pods:,}", "Points of distribution"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("On-Premise YTD", f"{total_on:,.2f}", f"{total_on_pods} PODs - {on_pct}% of total"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Off-Premise YTD", f"{total_off:,.2f}", f"{total_off_pods} PODs - {off_pct}% of total"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    section_title("On-Premise vs Off-Premise by Month")
    st.plotly_chart(
        grouped_bar(cm_filt, "Month", "On-Premise", "Off-Premise", "On-Premise", "Off-Premise"),
        use_container_width=True,
    )

    # Monthly detail table — redesigned with change vs LM
    section_title("Monthly Depletion Detail")
    cd_filt = channel_detail[channel_detail["Short"].isin(dp_months)].copy()
    cd_display = cd_filt[["Month", "Total Depletions", "Depl Change vs LM", "% Change vs LM", "On-Premise", "Off-Premise"]].copy()
    st.markdown(styled_table(cd_display, fmt={
        "Total Depletions": lambda v: f"{v:,.2f}",
        "Depl Change vs LM": lambda v: change_fmt(v),
        "% Change vs LM": lambda v: pct_change_fmt(v),
        "On-Premise": lambda v: f"{v:,.2f}",
        "Off-Premise": lambda v: f"{v:,.2f}",
    }), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Combined State View (On + Off Premise) ──
    section_title("Combined State Performance (On + Off Premise)")

    # Build combined state table from filtered on/off data
    on_agg = on_filt.groupby("State").agg(
        On_Cases=("YTD Cases", "sum"), On_PODs=("YTD PODs", "sum"),
        On_Mar=("Mar Cases", "sum"), On_Feb=("Feb Cases", "sum"),
        On_Mar_PODs=("Mar PODs", "sum"),
    ).reset_index()
    off_agg = off_filt.groupby("State").agg(
        Off_Cases=("YTD Cases", "sum"), Off_PODs=("YTD PODs", "sum"),
        Off_Mar=("Mar Cases", "sum"), Off_Feb=("Feb Cases", "sum"),
        Off_Mar_PODs=("Mar PODs", "sum"),
    ).reset_index()
    combined_st = pd.merge(on_agg, off_agg, on="State", how="outer").fillna(0)
    combined_st["Total Cases"] = combined_st["On_Cases"] + combined_st["Off_Cases"]
    combined_st["Total PODs"] = combined_st["On_PODs"] + combined_st["Off_PODs"]
    combined_st["On Cases"] = combined_st["On_Cases"]
    combined_st["Off Cases"] = combined_st["Off_Cases"]
    combined_st["Mar Cases"] = combined_st["On_Mar"] + combined_st["Off_Mar"]
    combined_st["Feb Cases"] = combined_st["On_Feb"] + combined_st["Off_Feb"]
    combined_st["Mar PODs"] = combined_st["On_Mar_PODs"] + combined_st["Off_Mar_PODs"]
    combined_st["Chg vs LM"] = combined_st["Mar Cases"] - combined_st["Feb Cases"]
    combined_st["% Growth"] = combined_st.apply(
        lambda r: ((r["Mar Cases"] - r["Feb Cases"]) / r["Feb Cases"] * 100) if r["Feb Cases"] > 0 else (float("inf") if r["Mar Cases"] > 0 else 0),
        axis=1,
    )
    combined_st = combined_st.sort_values("Total Cases", ascending=False).reset_index(drop=True)

    # Chart: combined top states
    chart_st = combined_st.head(10)
    st.plotly_chart(
        grouped_bar(chart_st, "State", "Total Cases", "Total PODs", "YTD Cases", "YTD PODs", horizontal=True),
        use_container_width=True,
    )

    # Combined state detail table
    cst_display = combined_st[["State", "Total Cases", "On Cases", "Off Cases", "Total PODs", "Mar Cases", "Feb Cases", "Chg vs LM", "% Growth"]].copy()
    st.markdown(styled_table(cst_display, fmt={
        "Total Cases": lambda v: f"{v:,.2f}",
        "On Cases": lambda v: f"{v:,.2f}",
        "Off Cases": lambda v: f"{v:,.2f}",
        "Total PODs": lambda v: f"{int(v):,}",
        "Mar Cases": lambda v: f"{v:,.2f}",
        "Feb Cases": lambda v: f"{v:,.2f}",
        "Chg vs LM": lambda v: change_fmt(v),
        "% Growth": lambda v: pct_change_fmt(v),
    }), unsafe_allow_html=True)

    # ── On/Off Premise split (expandable) ──
    st.markdown("<br>", unsafe_allow_html=True)
    col_on, col_off = st.columns(2)

    with col_on:
        section_title("On-Premise Top States — YTD Cases & PODs")
        st.plotly_chart(
            grouped_bar(on_filt.head(10), "State", "YTD Cases", "YTD PODs", "YTD Cases", "YTD PODs", horizontal=True),
            use_container_width=True,
        )

    with col_off:
        section_title("Off-Premise Top States — YTD Cases & PODs")
        st.plotly_chart(
            grouped_bar(off_filt.head(10), "State", "YTD Cases", "YTD PODs", "YTD Cases", "YTD PODs", horizontal=True),
            use_container_width=True,
        )

    with st.expander("On-Premise State Detail"):
        on_detail = on_filt[["State", "YTD Cases", "Depl Chg vs LM", "YTD PODs", "Mar PODs", "% Growth vs LM", "Feb Cases", "Mar Cases"]].copy()
        st.markdown(styled_table(on_detail, fmt={
            "YTD Cases": lambda v: f"{v:,.2f}",
            "Depl Chg vs LM": lambda v: change_fmt(v),
            "YTD PODs": lambda v: f"{int(v)}",
            "Mar PODs": lambda v: f"{int(v)}",
            "% Growth vs LM": lambda v: pct_change_fmt(v),
            "Feb Cases": lambda v: f"{v:,.2f}",
            "Mar Cases": lambda v: f"{v:,.2f}",
        }), unsafe_allow_html=True)

    with st.expander("Off-Premise State Detail"):
        off_detail = off_filt[["State", "YTD Cases", "Depl Chg vs LM", "YTD PODs", "Mar PODs", "% Growth vs LM", "Feb Cases", "Mar Cases"]].copy()
        st.markdown(styled_table(off_detail, fmt={
            "YTD Cases": lambda v: f"{v:,.2f}",
            "Depl Chg vs LM": lambda v: change_fmt(v),
            "YTD PODs": lambda v: f"{int(v)}",
            "Mar PODs": lambda v: f"{int(v)}",
            "% Growth vs LM": lambda v: pct_change_fmt(v),
            "Feb Cases": lambda v: f"{v:,.2f}",
            "Mar Cases": lambda v: f"{v:,.2f}",
        }), unsafe_allow_html=True)
        st.caption("Key chains: BevMo! - Binny's - Stew Leonard's - Total Wine - ShopRite - Milam's Markets")

    # Depletion performance by channel/premise type
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Depletion Performance by Premise Type")
    premise_perf = pd.DataFrame([
        {"Premise": "On-Premise", "YTD Cases": total_on, "Mar Cases": on_filt["Mar Cases"].sum(), "Feb Cases": on_filt["Feb Cases"].sum(), "YTD PODs": total_on_pods, "Mar PODs": int(on_filt["Mar PODs"].sum())},
        {"Premise": "Off-Premise", "YTD Cases": total_off, "Mar Cases": off_filt["Mar Cases"].sum(), "Feb Cases": off_filt["Feb Cases"].sum(), "YTD PODs": total_off_pods, "Mar PODs": int(off_filt["Mar PODs"].sum())},
    ])
    premise_perf["Depl Chg vs LM"] = premise_perf["Mar Cases"] - premise_perf["Feb Cases"]
    premise_perf["% Growth vs LM"] = premise_perf.apply(
        lambda r: ((r["Mar Cases"] - r["Feb Cases"]) / r["Feb Cases"] * 100) if r["Feb Cases"] > 0 else 0, axis=1
    )
    st.markdown(styled_table(
        premise_perf[["Premise", "YTD Cases", "Mar Cases", "Feb Cases", "Depl Chg vs LM", "% Growth vs LM", "YTD PODs", "Mar PODs"]],
        fmt={
            "YTD Cases": lambda v: f"{v:,.2f}",
            "Mar Cases": lambda v: f"{v:,.2f}",
            "Feb Cases": lambda v: f"{v:,.2f}",
            "Depl Chg vs LM": lambda v: change_fmt(v),
            "% Growth vs LM": lambda v: pct_change_fmt(v),
            "YTD PODs": lambda v: f"{int(v):,}",
            "Mar PODs": lambda v: f"{int(v):,}",
        }
    ), unsafe_allow_html=True)

    # Trade channel breakdown (from Ethica depletion report)
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Off-Premise by Trade Channel")
    st.markdown(styled_table(
        off_trade_channels[["Trade Channel", "YTD Cases", "Nov", "Dec", "Jan", "Feb", "Mar"]],
        fmt={
            "YTD Cases": lambda v: f"{v:,.2f}",
            "Nov": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Dec": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Jan": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Feb": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Mar": lambda v: f"{v:,.2f}" if v > 0 else "—",
        }
    ), unsafe_allow_html=True)
    st.caption("* Mar data through 3/11/2026 (from Ethica depletion report)")

    section_title("On-Premise by Trade Channel")
    st.markdown(styled_table(
        on_trade_channels[["Trade Channel", "YTD Cases", "Nov", "Dec", "Jan", "Feb", "Mar"]],
        fmt={
            "YTD Cases": lambda v: f"{v:,.2f}",
            "Nov": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Dec": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Jan": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Feb": lambda v: f"{v:,.2f}" if v > 0 else "—",
            "Mar": lambda v: f"{v:,.2f}" if v > 0 else "—",
        }
    ), unsafe_allow_html=True)

    # Top 15 accounts - REAL chain data from Ethica report
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Top 15 Accounts by YTD Depletions")
    st.caption("Source: Ethica depletion report through 3/11/2026")
    acct_display = top_accounts[["Account", "Premise", "States", "YTD Cases", "Feb Cases", "Mar Cases", "Chg vs LM", "% Growth"]].copy()
    st.markdown(styled_table(acct_display, fmt={
        "YTD Cases": lambda v: f"{v:,.2f}",
        "Feb Cases": lambda v: f"{v:,.2f}",
        "Mar Cases": lambda v: f"{v:,.2f}",
        "Chg vs LM": lambda v: change_fmt(v),
        "% Growth": lambda v: pct_change_fmt(v),
    }), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# GOPUFF (Updated with March 2026 Excel data)
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Gopuff":
    gp_all_states = gopuff_states["State"].tolist()
    gp_states = st.multiselect("Filter by State", gp_all_states, default=gp_all_states, key="gp_states")

    gs_filt = gopuff_states[gopuff_states["State"].isin(gp_states)]
    gl_filt = gopuff_location_detail[gopuff_location_detail["ST"].isin(gp_states)]
    filt_units = int(gs_filt["Units"].sum())
    filt_locs = int(gs_filt["Locations"].sum())

    gt_filt = gopuff_top_locations[gopuff_top_locations["State"].isin(gp_states)].head(5)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi("YTD Units Sold", str(filt_units), "Jan - Mar 2026", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Active Locations", str(filt_locs), f"Across {len(gp_states)} state(s)"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Mar Units", "59", "vs 70 in Feb (-15.7%)"), unsafe_allow_html=True)
    with c4:
        top_st = gs_filt.iloc[0] if len(gs_filt) > 0 else {"State": "-", "Units": 0, "Pct": 0}
        st.markdown(kpi("Top State", str(top_st["State"]), f"{int(top_st['Units'])} units - {top_st['Pct']}%"), unsafe_allow_html=True)

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

    section_title("Location Detail — Monthly Units")
    detail_display = gl_filt[["Rank", "Location", "ST", "Jan", "Feb", "Mar", "YTD"]].copy()
    detail_display = detail_display.replace(0, "-")
    st.markdown(styled_table(detail_display, fmt={
        "Rank": lambda v: str(v),
        "Jan": lambda v: str(v),
        "Feb": lambda v: str(v),
        "Mar": lambda v: str(v),
        "YTD": lambda v: f"<strong>{v}</strong>" if v != "-" else "-",
    }), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RESERVEBAR
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "ReserveBar":
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(kpi("Revenue", "$1.48K", "", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Orders", "23", ""), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Qty Sold", "73", ""), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("AOV", "$64.24", ""), unsafe_allow_html=True)
    with c5:
        st.markdown(kpi("AUO", "3.17", "Avg units/order"), unsafe_allow_html=True)
    with c6:
        st.markdown(kpi("Repeat Buyers", "4", "of 23 customers"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        section_title("Sales by Order Amount")
        st.plotly_chart(bar_chart(rb_order_range, "Range", "Pct"), use_container_width=True)

    with col2:
        section_title("Sales by Day of Week")
        st.plotly_chart(bar_chart(rb_dow, "Day", "Pct"), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        section_title("Customer Acquisition")
        acq1, acq2 = st.columns(2)
        with acq1:
            st.markdown(f"""
            <div style="background:{RED}; padding:22px 16px; text-align:center; border-radius:6px;">
                <span style="font-size:48px; font-weight:900; color:white; line-height:1;">19</span><br>
                <span style="font-size:11px; color:rgba(255,255,255,0.75); letter-spacing:0.1em; text-transform:uppercase;">New Customers</span><br>
                <span style="font-size:22px; color:white; font-weight:900;">83%</span>
            </div>""", unsafe_allow_html=True)
        with acq2:
            st.markdown(f"""
            <div style="background:{RED_MID}; padding:22px 16px; text-align:center; border-radius:6px;">
                <span style="font-size:48px; font-weight:900; color:white; line-height:1;">4</span><br>
                <span style="font-size:11px; color:rgba(255,255,255,0.75); letter-spacing:0.1em; text-transform:uppercase;">Repeat Customers</span><br>
                <span style="font-size:22px; color:white; font-weight:900;">17%</span>
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
                <p style="margin:0; font-size:32px; font-weight:900; color:white; line-height:1;">73</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">UNITS</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:32px; font-weight:900; color:white; line-height:1;">$1,478</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">REVENUE</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown('<p class="footer-text">Data Period: Nov 2025 - Mar 2026 &middot; Lucci Sales Intelligence</p>', unsafe_allow_html=True)

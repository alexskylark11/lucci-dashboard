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

on_states = pd.DataFrame([
    {"State": "CA", "YTD 9L": 96, "YTD PODs": 58, "Mar 9L": 51.5, "Mar PODs": 28, "Feb 9L": 20.83, "Jan 9L": 20.67, "Dec 9L": 3},
    {"State": "IL", "YTD 9L": 49.92, "YTD PODs": 66, "Mar 9L": 20.83, "Mar PODs": 25, "Feb 9L": 25.5, "Jan 9L": 2.25, "Dec 9L": 1.33},
    {"State": "NY", "YTD 9L": 35.25, "YTD PODs": 21, "Mar 9L": 16.17, "Mar PODs": 10, "Feb 9L": 5.67, "Jan 9L": 2.42, "Dec 9L": 11},
    {"State": "FL", "YTD 9L": 29.83, "YTD PODs": 30, "Mar 9L": 11.25, "Mar PODs": 14, "Feb 9L": 16.5, "Jan 9L": 2.08, "Dec 9L": 0},
    {"State": "NJ", "YTD 9L": 29, "YTD PODs": 12, "Mar 9L": 8, "Mar PODs": 5, "Feb 9L": 19, "Jan 9L": 1, "Dec 9L": 1},
    {"State": "AZ", "YTD 9L": 28.83, "YTD PODs": 37, "Mar 9L": 5.75, "Mar PODs": 9, "Feb 9L": 23, "Jan 9L": 0.08, "Dec 9L": 0},
    {"State": "TX", "YTD 9L": 19.33, "YTD PODs": 14, "Mar 9L": 9.25, "Mar PODs": 5, "Feb 9L": 9.08, "Jan 9L": 1, "Dec 9L": 0},
    {"State": "OH", "YTD 9L": 5.17, "YTD PODs": 8, "Mar 9L": 1.5, "Mar PODs": 4, "Feb 9L": 3.42, "Jan 9L": 0.25, "Dec 9L": 0},
    {"State": "CO", "YTD 9L": 4.5, "YTD PODs": 3, "Mar 9L": 3.5, "Mar PODs": 2, "Feb 9L": 1, "Jan 9L": 0, "Dec 9L": 0},
    {"State": "MD", "YTD 9L": 4.42, "YTD PODs": 11, "Mar 9L": 3.42, "Mar PODs": 7, "Feb 9L": 1, "Jan 9L": 0, "Dec 9L": 0},
    {"State": "NV", "YTD 9L": 4, "YTD PODs": 1, "Mar 9L": 4, "Mar PODs": 1, "Feb 9L": 0, "Jan 9L": 0, "Dec 9L": 0},
    {"State": "VA", "YTD 9L": 2.17, "YTD PODs": 4, "Mar 9L": 1.08, "Mar PODs": 2, "Feb 9L": 1.08, "Jan 9L": 0, "Dec 9L": 0},
    {"State": "DC", "YTD 9L": 1.42, "YTD PODs": 4, "Mar 9L": 0.08, "Mar PODs": 1, "Feb 9L": 1.17, "Jan 9L": 0.17, "Dec 9L": 0},
    {"State": "CT", "YTD 9L": 1, "YTD PODs": 1, "Mar 9L": 0, "Mar PODs": 0, "Feb 9L": 1, "Jan 9L": 0, "Dec 9L": 0},
    {"State": "DE", "YTD 9L": 0.58, "YTD PODs": 3, "Mar 9L": 0.33, "Mar PODs": 1, "Feb 9L": 0.08, "Jan 9L": 0.17, "Dec 9L": 0},
    {"State": "NC", "YTD 9L": 0.33, "YTD PODs": 2, "Mar 9L": 0.33, "Mar PODs": 2, "Feb 9L": 0, "Jan 9L": 0, "Dec 9L": 0},
    {"State": "NM", "YTD 9L": 0.33, "YTD PODs": 3, "Mar 9L": 0.17, "Mar PODs": 2, "Feb 9L": 0, "Jan 9L": 0.17, "Dec 9L": 0},
])

off_states = pd.DataFrame([
    {"State": "CA", "YTD 9L": 310.33, "YTD PODs": 225, "Mar 9L": 100.33, "Mar PODs": 97, "Feb 9L": 41.75, "Jan 9L": 165.17},
    {"State": "NJ", "YTD 9L": 199.58, "YTD PODs": 68, "Mar 9L": 20.33, "Mar PODs": 13, "Feb 9L": 170.08, "Jan 9L": 3.83},
    {"State": "NY", "YTD 9L": 138.17, "YTD PODs": 69, "Mar 9L": 24.58, "Mar PODs": 16, "Feb 9L": 99.08, "Jan 9L": 14.5},
    {"State": "FL", "YTD 9L": 117.08, "YTD PODs": 47, "Mar 9L": 16.5, "Mar PODs": 23, "Feb 9L": 90.25, "Jan 9L": 10.33},
    {"State": "IL", "YTD 9L": 101.92, "YTD PODs": 74, "Mar 9L": 41.58, "Mar PODs": 24, "Feb 9L": 49.75, "Jan 9L": 6.17},
    {"State": "VA", "YTD 9L": 51.5, "YTD PODs": 96, "Mar 9L": 43.33, "Mar PODs": 87, "Feb 9L": 8.17, "Jan 9L": 0},
    {"State": "CT", "YTD 9L": 33.83, "YTD PODs": 24, "Mar 9L": 30.17, "Mar PODs": 17, "Feb 9L": 3.67, "Jan 9L": 0},
    {"State": "TX", "YTD 9L": 25.25, "YTD PODs": 19, "Mar 9L": 15.67, "Mar PODs": 16, "Feb 9L": 8.5, "Jan 9L": 1.08},
    {"State": "NC", "YTD 9L": 22.58, "YTD PODs": 52, "Mar 9L": 22.58, "Mar PODs": 52, "Feb 9L": 0, "Jan 9L": 0},
    {"State": "DE", "YTD 9L": 21.58, "YTD PODs": 17, "Mar 9L": 13.5, "Mar PODs": 13, "Feb 9L": 7, "Jan 9L": 1.08},
    {"State": "MD", "YTD 9L": 20.08, "YTD PODs": 16, "Mar 9L": 7, "Mar PODs": 7, "Feb 9L": 12.75, "Jan 9L": 0.33},
    {"State": "OH", "YTD 9L": 15.92, "YTD PODs": 18, "Mar 9L": 4.58, "Mar PODs": 8, "Feb 9L": 9.83, "Jan 9L": 1.5},
    {"State": "SC", "YTD 9L": 10.67, "YTD PODs": 23, "Mar 9L": 10.67, "Mar PODs": 23, "Feb 9L": 0, "Jan 9L": 0},
    {"State": "CO", "YTD 9L": 6, "YTD PODs": 10, "Mar 9L": 1.58, "Mar PODs": 4, "Feb 9L": 1.33, "Jan 9L": 3.08},
    {"State": "DC", "YTD 9L": 3, "YTD PODs": 1, "Mar 9L": 0, "Mar PODs": 0, "Feb 9L": 3, "Jan 9L": 0},
    {"State": "GA", "YTD 9L": 1.5, "YTD PODs": 3, "Mar 9L": 1, "Mar PODs": 1, "Feb 9L": 0.5, "Jan 9L": 0},
    {"State": "NM", "YTD 9L": 0.42, "YTD PODs": 2, "Mar 9L": 0.08, "Mar PODs": 1, "Feb 9L": 0.33, "Jan 9L": 0},
    {"State": "AZ", "YTD 9L": 0.25, "YTD PODs": 1, "Mar 9L": 0, "Mar PODs": 0, "Feb 9L": 0.25, "Jan 9L": 0},
])

WEEKS = ["Jan 19", "Jan 26", "Feb 2", "Feb 9", "Feb 16", "Feb 23", "Mar 2", "Mar 9", "Mar 16"]
gopuff_weekly = pd.DataFrame({"Week": WEEKS, "Units": [5, 6, 8, 26, 21, 15, 8, 15, 12]})

gopuff_states = pd.DataFrame([
    {"State": "NY", "Units": 75, "Pct": 64.7, "Locations": 5},
    {"State": "CA", "Units": 27, "Pct": 23.3, "Locations": 13},
    {"State": "FL", "Units": 14, "Pct": 12.1, "Locations": 5},
])

gopuff_top_locations = pd.DataFrame([
    {"Location": "JFK Brooklyn 554", "YTD": 21},
    {"Location": "JFK New York 880", "YTD": 21},
    {"Location": "JFK New York 975", "YTD": 19},
    {"Location": "BUR Pasadena 416", "YTD": 9},
    {"Location": "JFK New York 807", "YTD": 8},
])

gopuff_location_detail = pd.DataFrame([
    {"Rank": 1, "Location": "JFK_Brooklyn_554", "ST": "NY", "Jan 19": 1, "Jan 26": 3, "Feb 2": 3, "Feb 9": 5, "Feb 16": 1, "Feb 23": 1, "Mar 2": 1, "Mar 9": 5, "Mar 16": 1, "YTD": 21},
    {"Rank": 2, "Location": "JFK_New-York_880", "ST": "NY", "Jan 19": None, "Jan 26": None, "Feb 2": None, "Feb 9": None, "Feb 16": 10, "Feb 23": 1, "Mar 2": 1, "Mar 9": 6, "Mar 16": 3, "YTD": 21},
    {"Rank": 3, "Location": "JFK_New-York_975", "ST": "NY", "Jan 19": 1, "Jan 26": 3, "Feb 2": 1, "Feb 9": 2, "Feb 16": 5, "Feb 23": 1, "Mar 2": 2, "Mar 9": 3, "Mar 16": 1, "YTD": 19},
    {"Rank": 4, "Location": "BUR_Pasadena_416", "ST": "CA", "Jan 19": None, "Jan 26": None, "Feb 2": None, "Feb 9": 2, "Feb 16": None, "Feb 23": 7, "Mar 2": None, "Mar 9": None, "Mar 16": None, "YTD": 9},
    {"Rank": 5, "Location": "JFK_New-York_807", "ST": "NY", "Jan 19": None, "Jan 26": None, "Feb 2": None, "Feb 9": 2, "Feb 16": None, "Feb 23": 1, "Mar 2": 1, "Mar 9": 1, "Mar 16": 3, "YTD": 8},
    {"Rank": 6, "Location": "JFK_Brooklyn_629", "ST": "NY", "Jan 19": 2, "Jan 26": None, "Feb 2": 1, "Feb 9": None, "Feb 16": 3, "Feb 23": None, "Mar 2": None, "Mar 9": None, "Mar 16": None, "YTD": 6},
    {"Rank": 7, "Location": "MIA_Miami_183", "ST": "FL", "Jan 19": None, "Jan 26": None, "Feb 2": None, "Feb 9": 2, "Feb 16": 1, "Feb 23": 1, "Mar 2": 1, "Mar 9": None, "Mar 16": None, "YTD": 5},
    {"Rank": 8, "Location": "MIA_Miami-Beach_911", "ST": "FL", "Jan 19": None, "Jan 26": None, "Feb 2": None, "Feb 9": 2, "Feb 16": None, "Feb 23": 1, "Mar 2": 1, "Mar 9": None, "Mar 16": None, "YTD": 4},
    {"Rank": 9, "Location": "SAN_Point-Loma_446", "ST": "CA", "Jan 19": None, "Jan 26": None, "Feb 2": None, "Feb 9": 1, "Feb 16": None, "Feb 23": 2, "Mar 2": None, "Mar 9": None, "Mar 16": None, "YTD": 3},
    {"Rank": 10, "Location": "MIA_Miami_330", "ST": "FL", "Jan 19": None, "Jan 26": None, "Feb 2": 1, "Feb 9": 1, "Feb 16": None, "Feb 23": None, "Mar 2": 1, "Mar 9": None, "Mar 16": None, "YTD": 3},
])

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


# ══════════════════════════════════════════════════════════════════════════════
# NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
active_tab = st.radio(
    "Dashboard",
    ["Overview", "Depletions", "Gopuff", "ReserveBar"],
    horizontal=True,
    label_visibility="collapsed",
)

st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW — master cross-channel summary
# ══════════════════════════════════════════════════════════════════════════════
if active_tab == "Overview":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi("Total Depletions (9L)", "1,402.92", "Nov 2025 - Mar 2026", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Total PODs", "1,046", "Points of distribution"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Gopuff YTD Units", "116", "23 locations, 3 states"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("ReserveBar Revenue", "$1.48K", "73 units, 23 orders"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        section_title("Monthly Depletions (9L Equiv)")
        st.plotly_chart(bar_chart(grand_monthly, "Month", "Cases"), use_container_width=True)

    with col2:
        section_title("On-Premise vs Off-Premise by Month")
        st.plotly_chart(
            grouped_bar(combined_monthly, "Month", "On-Premise", "Off-Premise", "On-Premise", "Off-Premise"),
            use_container_width=True,
        )

    # Channel breakdown
    section_title("Channel Breakdown")
    detail = pd.DataFrame([
        {"Month": "Nov 2025", "Total 9L": 1.00, "On-Premise": 0, "Off-Premise": 1.00},
        {"Month": "Dec 2025", "Total 9L": 28.17, "On-Premise": 16.33, "Off-Premise": 11.83},
        {"Month": "Jan 2026", "Total 9L": 248.25, "On-Premise": 30.25, "Off-Premise": 207.08},
        {"Month": "Feb 2026", "Total 9L": 634.83, "On-Premise": 128.33, "Off-Premise": 506.25},
        {"Month": "Mar 2026", "Total 9L": 490.67, "On-Premise": 137.17, "Off-Premise": 353.50},
    ])
    st.dataframe(detail, hide_index=True, use_container_width=True)

    # March highlight
    st.markdown("""
    <div class="highlight-banner">
        <div>
            <p style="margin:0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.15em; text-transform:uppercase;">March 2026 Highlights</p>
            <p style="margin:8px 0 0; font-size:18px; color:white; font-weight:900; letter-spacing:0.02em;">Strong March across all channels</p>
            <p style="margin:4px 0 0; font-size:13px; color:rgba(255,255,255,0.7);">490.67 depletion cases &middot; 520 PODs active &middot; 12 Gopuff units &middot; 17+ states</p>
        </div>
        <div style="display:flex; gap:32px; flex-shrink:0;">
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">490.67</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">MAR 9L</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">520</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">MAR PODS</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; line-height:1;">17+</p>
                <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6); letter-spacing:0.1em;">STATES</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DEPLETIONS — merged On + Off Premise
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Depletions":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi("Total YTD (9L)", "1,402.92", "Nov 2025 - Mar 2026", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Total PODs", "1,046", "Points of distribution"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("On-Premise YTD", "312.08", "278 PODs - 22% of total"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Off-Premise YTD", "1,079.67", "765 PODs - 77% of total"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # On vs Off by Month chart
    section_title("On-Premise vs Off-Premise by Month")
    st.plotly_chart(
        grouped_bar(combined_monthly, "Month", "On-Premise", "Off-Premise", "On-Premise", "Off-Premise"),
        use_container_width=True,
    )

    # Monthly detail table
    section_title("Monthly Depletion Detail")
    detail = pd.DataFrame([
        {"Month": "Nov 2025", "Total 9L": 1.00, "On-Premise": 0, "Off-Premise": 1.00},
        {"Month": "Dec 2025", "Total 9L": 28.17, "On-Premise": 16.33, "Off-Premise": 11.83},
        {"Month": "Jan 2026", "Total 9L": 248.25, "On-Premise": 30.25, "Off-Premise": 207.08},
        {"Month": "Feb 2026", "Total 9L": 634.83, "On-Premise": 128.33, "Off-Premise": 506.25},
        {"Month": "Mar 2026", "Total 9L": 490.67, "On-Premise": 137.17, "Off-Premise": 353.50},
    ])
    st.dataframe(detail, hide_index=True, use_container_width=True)

    # Side-by-side state charts
    st.markdown("<br>", unsafe_allow_html=True)
    col_on, col_off = st.columns(2)

    with col_on:
        section_title("On-Premise Top States — YTD vs March")
        st.plotly_chart(
            grouped_bar(on_states.head(10), "State", "YTD 9L", "Mar 9L", "YTD 9L", "Mar 9L", horizontal=True),
            use_container_width=True,
        )

    with col_off:
        section_title("Off-Premise Top States — YTD vs March")
        st.plotly_chart(
            grouped_bar(off_states.head(10), "State", "YTD 9L", "Mar 9L", "YTD 9L", "Mar 9L", horizontal=True),
            use_container_width=True,
        )

    # Expandable detail tables
    with st.expander("Full On-Premise State Detail"):
        st.dataframe(on_states, hide_index=True, use_container_width=True)

    with st.expander("Full Off-Premise State Detail"):
        st.dataframe(off_states, hide_index=True, use_container_width=True)
        st.caption("Key chains: BevMo! - Binny's - Stew Leonard's - Total Wine - ShopRite - Milam's Markets - Food Lion")


# ══════════════════════════════════════════════════════════════════════════════
# GOPUFF
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Gopuff":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi("YTD Units Sold", "116", "All locations", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Active Locations", "23", "Across 3 states"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Top State", "NY", "75 units - 64.7%"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Week of Mar 16", "12", "vs 15 prior week"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.65, 1])

    with col1:
        section_title("Weekly Units Ordered")
        st.plotly_chart(bar_chart(gopuff_weekly, "Week", "Units"), use_container_width=True)

    with col2:
        section_title("Units by State")
        for _, row in gopuff_states.iterrows():
            st.markdown(f"**{row['State']}** — {row['Units']} units ({row['Pct']}%)")
            st.progress(row["Pct"] / 100)
            st.caption(f"{row['Locations']} locations")

    section_title("Top 5 Locations by YTD Units")
    fig = bar_chart(gopuff_top_locations, "Location", "YTD", horizontal=True)
    fig.update_layout(height=200)
    st.plotly_chart(fig, use_container_width=True)

    section_title("Location Detail — Weekly Units")
    st.dataframe(gopuff_location_detail.fillna("-"), hide_index=True, use_container_width=True)


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

    # Top SKU banner
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

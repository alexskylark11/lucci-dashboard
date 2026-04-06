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
    # Month filter
    ov_months = st.multiselect("Filter by Month", DEPL_MONTHS, default=DEPL_MONTHS, key="ov_months")
    gm_filt = grand_monthly[grand_monthly["Month"].isin(ov_months)]
    cm_filt = combined_monthly[combined_monthly["Month"].isin(ov_months)]

    total_cases = gm_filt["Cases"].sum()
    total_on = cm_filt["On-Premise"].sum()
    total_off = cm_filt["Off-Premise"].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(kpi("Gross Revenue YTD", "$148,106", "4,811 cases shipped", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Net Revenue YTD", "$134,582", "After credit memos", dark=True), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Total Depletions", f"{total_cases:,.2f}", "Cases - filtered period"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Gopuff YTD Units", "116", "23 locations, 3 states"), unsafe_allow_html=True)
    with c5:
        st.markdown(kpi("ReserveBar Revenue", "$1.48K", "73 units, 23 orders"), unsafe_allow_html=True)

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

    # Channel breakdown
    section_title("Channel Breakdown")
    detail_all = pd.DataFrame([
        {"Month": "Nov 2025", "Short": "Nov", "Total Cases": 1.00, "On-Premise": 0, "Off-Premise": 1.00},
        {"Month": "Dec 2025", "Short": "Dec", "Total Cases": 28.17, "On-Premise": 16.33, "Off-Premise": 11.83},
        {"Month": "Jan 2026", "Short": "Jan", "Total Cases": 248.25, "On-Premise": 30.25, "Off-Premise": 207.08},
        {"Month": "Feb 2026", "Short": "Feb", "Total Cases": 634.83, "On-Premise": 128.33, "Off-Premise": 506.25},
        {"Month": "Mar 2026", "Short": "Mar", "Total Cases": 490.67, "On-Premise": 137.17, "Off-Premise": 353.50},
    ])
    detail_filt = detail_all[detail_all["Short"].isin(ov_months)].drop(columns=["Short"])
    st.dataframe(detail_filt, hide_index=True, use_container_width=True)

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
    # Month filter
    sh_months = st.multiselect("Filter by Month", SHIP_MONTHS, default=SHIP_MONTHS, key="sh_months")
    sc_filt = ship_monthly_cases[ship_monthly_cases["Month"].isin(sh_months)]
    sr_filt = ship_monthly_revenue[ship_monthly_revenue["Month"].isin(sh_months)]
    srpc_filt = ship_monthly_rev_per_case[ship_monthly_rev_per_case["Month"].isin(sh_months)]

    filt_cases = int(sc_filt["Cases"].sum())
    filt_rev = int(sr_filt["Revenue"].sum())
    filt_credits = round(filt_rev * (-13523 / 148106))  # proportional credit memos
    filt_net = filt_rev + filt_credits
    filt_rpc = round(filt_rev / filt_cases, 0) if filt_cases > 0 else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(kpi("Cases Shipped", f"{filt_cases:,}", "Filtered period", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Gross Revenue", f"${filt_rev:,}", "Before credit memos"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Credit Memos", f"-${abs(filt_credits):,}", "Adjustments applied"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Net Revenue", f"${filt_net:,}", "After credit memos"), unsafe_allow_html=True)
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

    section_title("Monthly Gross Revenue Per Case ($ / Case Shipped)")
    fig = bar_chart(srpc_filt, "Month", "Rev/Case")
    fig.update_traces(text=srpc_filt["Rev/Case"].apply(lambda x: f"${x:.1f}"), textposition="outside")
    fig.update_layout(height=320)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# DEPLETIONS — merged On + Off Premise
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Depletions":
    # Filters
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

    # On vs Off by Month chart
    section_title("On-Premise vs Off-Premise by Month")
    st.plotly_chart(
        grouped_bar(cm_filt, "Month", "On-Premise", "Off-Premise", "On-Premise", "Off-Premise"),
        use_container_width=True,
    )

    # Monthly detail table
    section_title("Monthly Depletion Detail")
    detail_all = pd.DataFrame([
        {"Month": "Nov 2025", "Short": "Nov", "Total Cases": 1.00, "On-Premise": 0, "Off-Premise": 1.00},
        {"Month": "Dec 2025", "Short": "Dec", "Total Cases": 28.17, "On-Premise": 16.33, "Off-Premise": 11.83},
        {"Month": "Jan 2026", "Short": "Jan", "Total Cases": 248.25, "On-Premise": 30.25, "Off-Premise": 207.08},
        {"Month": "Feb 2026", "Short": "Feb", "Total Cases": 634.83, "On-Premise": 128.33, "Off-Premise": 506.25},
        {"Month": "Mar 2026", "Short": "Mar", "Total Cases": 490.67, "On-Premise": 137.17, "Off-Premise": 353.50},
    ])
    detail_filt = detail_all[detail_all["Short"].isin(dp_months)].drop(columns=["Short"])
    st.dataframe(detail_filt, hide_index=True, use_container_width=True)

    # Side-by-side state charts
    st.markdown("<br>", unsafe_allow_html=True)
    col_on, col_off = st.columns(2)

    with col_on:
        section_title("On-Premise Top States — YTD vs March")
        st.plotly_chart(
            grouped_bar(on_filt.head(10), "State", "YTD Cases", "Mar Cases", "YTD Cases", "Mar Cases", horizontal=True),
            use_container_width=True,
        )

    with col_off:
        section_title("Off-Premise Top States — YTD vs March")
        st.plotly_chart(
            grouped_bar(off_filt.head(10), "State", "YTD Cases", "Mar Cases", "YTD Cases", "Mar Cases", horizontal=True),
            use_container_width=True,
        )

    # Expandable detail tables
    with st.expander("Full On-Premise State Detail"):
        st.dataframe(on_filt, hide_index=True, use_container_width=True)

    with st.expander("Full Off-Premise State Detail"):
        st.dataframe(off_filt, hide_index=True, use_container_width=True)
        st.caption("Key chains: BevMo! - Binny's - Stew Leonard's - Total Wine - ShopRite - Milam's Markets - Food Lion")


# ══════════════════════════════════════════════════════════════════════════════
# GOPUFF
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Gopuff":
    # State filter
    gp_all_states = gopuff_states["State"].tolist()
    gp_states = st.multiselect("Filter by State", gp_all_states, default=gp_all_states, key="gp_states")

    gs_filt = gopuff_states[gopuff_states["State"].isin(gp_states)]
    gl_filt = gopuff_location_detail[gopuff_location_detail["ST"].isin(gp_states)]
    filt_units = int(gs_filt["Units"].sum())
    filt_locs = int(gs_filt["Locations"].sum())

    # Recalc top locations from filtered detail
    gt_filt = gl_filt.nlargest(5, "YTD")[["Location", "YTD"]]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi("Units Sold", str(filt_units), "Filtered states", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Active Locations", str(filt_locs), f"Across {len(gp_states)} state(s)"), unsafe_allow_html=True)
    with c3:
        top_st = gs_filt.iloc[0] if len(gs_filt) > 0 else {"State": "-", "Units": 0, "Pct": 0}
        st.markdown(kpi("Top State", str(top_st["State"]), f"{int(top_st['Units'])} units - {top_st['Pct']}%"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Week of Mar 16", "12", "vs 15 prior week"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.65, 1])

    with col1:
        section_title("Weekly Units Ordered")
        st.plotly_chart(bar_chart(gopuff_weekly, "Week", "Units"), use_container_width=True)

    with col2:
        section_title("Units by State")
        for _, row in gs_filt.iterrows():
            st.markdown(f"**{row['State']}** — {row['Units']} units ({row['Pct']}%)")
            st.progress(row["Pct"] / 100)
            st.caption(f"{row['Locations']} locations")

    section_title("Top Locations by YTD Units")
    if len(gt_filt) > 0:
        fig = bar_chart(gt_filt, "Location", "YTD", horizontal=True)
        fig.update_layout(height=200)
        st.plotly_chart(fig, use_container_width=True)

    section_title("Location Detail — Weekly Units")
    st.dataframe(gl_filt.fillna("-"), hide_index=True, use_container_width=True)


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

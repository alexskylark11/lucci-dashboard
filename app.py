import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# ── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Anton&display=swap');

.main .block-container { padding-top: 0; }

.lucci-header {
    background: #8B1A1A;
    border-bottom: 4px solid #2C1A0E;
    padding: 18px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -1rem -1rem 1.5rem -1rem;
}
.lucci-title {
    font-family: 'Anton', 'Impact', 'Arial Black', sans-serif;
    font-size: 34px;
    font-weight: 900;
    color: white;
    letter-spacing: 0.06em;
    line-height: 1;
}
.lucci-subtitle {
    font-size: 10px;
    color: rgba(255,255,255,0.6);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-left: 12px;
}
.lucci-period {
    font-size: 9px;
    color: rgba(255,255,255,0.5);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 3px;
}

.kpi-card {
    border: 2px solid #EEDBD8;
    padding: 18px 20px;
    background: #FFFDF5;
    display: flex;
    flex-direction: column;
    gap: 3px;
    height: 100%;
}
.kpi-card-dark {
    border: 2px solid #8B1A1A;
    padding: 18px 20px;
    background: #8B1A1A;
    display: flex;
    flex-direction: column;
    gap: 3px;
    height: 100%;
}
.kpi-label {
    font-size: 9px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #8B6347;
    font-family: Georgia, serif;
}
.kpi-label-dark {
    font-size: 9px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #EEDBD8;
    font-family: Georgia, serif;
}
.kpi-value {
    font-size: 32px;
    font-weight: 900;
    color: #8B1A1A;
    font-family: 'Anton', 'Impact', 'Arial Black', sans-serif;
    line-height: 1.05;
    letter-spacing: 0.02em;
}
.kpi-value-dark {
    font-size: 32px;
    font-weight: 900;
    color: white;
    font-family: 'Anton', 'Impact', 'Arial Black', sans-serif;
    line-height: 1.05;
    letter-spacing: 0.02em;
}
.kpi-sub {
    font-size: 11px;
    color: #5C3A1E;
}
.kpi-sub-dark {
    font-size: 11px;
    color: rgba(255,255,255,0.65);
}

.section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
}
.section-bar {
    width: 4px;
    height: 20px;
    background: #8B1A1A;
    display: inline-block;
}
.section-text {
    font-size: 11px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #8B1A1A;
    font-family: 'Anton', 'Impact', 'Arial Black', sans-serif;
    font-weight: 900;
}

.highlight-banner {
    background: #8B1A1A;
    border: 3px solid #2C1A0E;
    padding: 20px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin-top: 1rem;
}
.highlight-text { color: white; }
.highlight-stat {
    text-align: center;
    color: white;
    font-family: 'Anton', 'Impact', sans-serif;
}

.footer-text {
    text-align: center;
    color: #8B6347;
    font-size: 9px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 2rem;
}

/* Style the radio buttons / tabs */
div[data-testid="stHorizontalBlock"] .stRadio > div {
    flex-direction: row;
    gap: 0;
}

/* Table styling */
table { font-size: 12px !important; }
thead tr th {
    background: #8B1A1A !important;
    color: white !important;
    font-weight: 900 !important;
    font-size: 9px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="lucci-header">
    <div>
        <div style="display:flex; align-items:baseline;">
            <span class="lucci-title">LUCCI</span>
            <span class="lucci-subtitle">Lambrusco Reggiano DOC</span>
        </div>
        <p class="lucci-period">Sales Intelligence Dashboard</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ── HELPERS ──────────────────────────────────────────────────────────────────
def kpi(label, value, sub="", dark=False):
    cls = "dark" if dark else ""
    return f"""
    <div class="kpi-card{'-dark' if dark else ''}">
        <span class="kpi-label{'-dark' if dark else ''}">{label}</span>
        <span class="kpi-value{'-dark' if dark else ''}">{value}</span>
        <span class="kpi-sub{'-dark' if dark else ''}">{sub}</span>
    </div>"""


def section_title(text):
    st.markdown(f"""
    <div class="section-title">
        <span class="section-bar"></span>
        <span class="section-text">{text}</span>
    </div>""", unsafe_allow_html=True)


def bar_chart(df, x, y, title="", color=RED, highlight_max=True, horizontal=False):
    if horizontal:
        fig = px.bar(df, y=x, x=y, orientation="h", color_discrete_sequence=[color])
        fig.update_layout(yaxis=dict(autorange="reversed"))
    else:
        fig = px.bar(df, x=x, y=y, color_discrete_sequence=[color])

    fig.update_layout(
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(family="Georgia, serif", color=TEXT_LIGHT, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor=CREAM_DARK, showline=False),
        showlegend=False,
        height=260,
    )
    if horizontal:
        fig.update_layout(
            xaxis=dict(showgrid=True, gridcolor=CREAM_DARK, showline=False),
            yaxis=dict(showgrid=False, showline=False, autorange="reversed"),
        )
    return fig


def grouped_bar(df, x, y1, y2, name1, name2, color1=RED, color2=RED_PALE):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df[x], y=df[y1], name=name1, marker_color=color1))
    fig.add_trace(go.Bar(x=df[x], y=df[y2], name=name2, marker_color=color2))
    fig.update_layout(
        barmode="group",
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(family="Georgia, serif", color=TEXT_LIGHT, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor=CREAM_DARK, showline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=10)),
        height=260,
    )
    return fig


def horizontal_grouped_bar(df, cat, y1, y2, name1, name2, color1=RED, color2=RED_PALE):
    fig = go.Figure()
    fig.add_trace(go.Bar(y=df[cat], x=df[y1], name=name1, marker_color=color1, orientation="h"))
    fig.add_trace(go.Bar(y=df[cat], x=df[y2], name=name2, marker_color=color2, orientation="h"))
    fig.update_layout(
        barmode="group",
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(family="Georgia, serif", color=TEXT_LIGHT, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor=CREAM_DARK, showline=False),
        yaxis=dict(showgrid=False, showline=False, autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=10)),
        height=340,
    )
    return fig


def style_dataframe(df):
    return df.style.set_properties(**{
        "font-size": "12px",
        "font-family": "Georgia, serif",
    }).set_table_styles([
        {"selector": "thead th", "props": [
            ("background-color", RED), ("color", "white"), ("font-weight", "900"),
            ("font-size", "9px"), ("letter-spacing", "0.1em"), ("text-transform", "uppercase"),
            ("padding", "8px 10px"),
        ]},
        {"selector": "tbody td", "props": [("padding", "8px 10px")]},
    ])


# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

# ── DEPLETION DATA ───────────────────────────────────────────────────────────
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

on_monthly = pd.DataFrame([
    {"Month": "Nov", "Cases": 0}, {"Month": "Dec", "Cases": 16.33},
    {"Month": "Jan", "Cases": 30.25}, {"Month": "Feb", "Cases": 128.33},
    {"Month": "Mar", "Cases": 137.17},
])

off_monthly = pd.DataFrame([
    {"Month": "Nov", "Cases": 1}, {"Month": "Dec", "Cases": 11.83},
    {"Month": "Jan", "Cases": 207.08}, {"Month": "Feb", "Cases": 506.25},
    {"Month": "Mar", "Cases": 353.5},
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

# ── GOPUFF DATA ──────────────────────────────────────────────────────────────
WEEKS = ["Jan 19", "Jan 26", "Feb 2", "Feb 9", "Feb 16", "Feb 23", "Mar 2", "Mar 9", "Mar 16"]
weekly_totals = [5, 6, 8, 26, 21, 15, 8, 15, 12]
gopuff_weekly = pd.DataFrame({"Week": WEEKS, "Units": weekly_totals})

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


# ══════════════════════════════════════════════════════════════════════════════
# NAVIGATION — single row of tabs
# ══════════════════════════════════════════════════════════════════════════════
active_tab = st.radio(
    "Dashboard",
    ["Depletion Overview", "On-Premise", "Off-Premise", "Gopuff", "ReserveBar"],
    horizontal=True,
    label_visibility="collapsed",
)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# DEPLETION OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if active_tab == "Depletion Overview":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi("YTD Total 9L Equiv", "1,402.92", "Nov 2025 - Mar 2026", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("YTD Total PODs", "1,046", "Points of distribution"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("On-Premise YTD", "312.08", "278 PODs - 22% of total"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Off-Premise YTD", "1,079.67", "765 PODs - 77% of total"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        section_title("Total Monthly Depletions (9L Equiv)")
        fig = bar_chart(grand_monthly, "Month", "Cases")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("On vs Off Premise by Month")
        fig = grouped_bar(combined_monthly, "Month", "On-Premise", "Off-Premise", "On-Premise", "Off-Premise")
        st.plotly_chart(fig, use_container_width=True)

    section_title("Monthly Depletion Detail")
    detail = pd.DataFrame([
        {"Month": "Nov 2025", "Total 9L": 1.00, "On-Premise": 0, "Off-Premise": 1.00},
        {"Month": "Dec 2025", "Total 9L": 28.17, "On-Premise": 16.33, "Off-Premise": 11.83},
        {"Month": "Jan 2026", "Total 9L": 248.25, "On-Premise": 30.25, "Off-Premise": 207.08},
        {"Month": "Feb 2026", "Total 9L": 634.83, "On-Premise": 128.33, "Off-Premise": 506.25},
        {"Month": "Mar 2026", "Total 9L": 490.67, "On-Premise": 137.17, "Off-Premise": 353.50},
    ])
    st.dataframe(detail, hide_index=True, use_container_width=True)

    st.markdown("""
    <div class="highlight-banner">
        <div>
            <p style="margin:0; font-size:9px; color:rgba(255,255,255,0.55); letter-spacing:0.2em; text-transform:uppercase;">March 2026 Highlight</p>
            <p style="margin:6px 0 0; font-size:16px; color:white; font-weight:900; font-family:'Anton','Impact',sans-serif; letter-spacing:0.03em;">STRONG MARCH — 490.67 TOTAL 9L CASES ACROSS 17+ STATES</p>
            <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6);">Off-premise 353.5 - On-premise 137.17 - 520 PODs active</p>
        </div>
        <div style="display:flex; gap:28px; flex-shrink:0;">
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; font-family:'Anton','Impact',sans-serif; line-height:1;">490.67</p>
                <p style="margin:4px 0 0; font-size:9px; color:rgba(255,255,255,0.55); letter-spacing:0.15em;">MAR 9L</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; font-family:'Anton','Impact',sans-serif; line-height:1;">520</p>
                <p style="margin:4px 0 0; font-size:9px; color:rgba(255,255,255,0.55); letter-spacing:0.15em;">MAR PODS</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:30px; font-weight:900; color:white; font-family:'Anton','Impact',sans-serif; line-height:1;">17+</p>
                <p style="margin:4px 0 0; font-size:9px; color:rgba(255,255,255,0.55); letter-spacing:0.15em;">STATES</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ON-PREMISE
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "On-Premise":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi("YTD 9L Equiv", "312.08", "On-Premise total", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("YTD PODs", "278", "Points of distribution"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("March 9L", "137.17", "118 active PODs"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Top State (YTD)", "CA", "96 9L - 58 PODs"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("On-Premise Monthly Trend")
    st.plotly_chart(bar_chart(on_monthly, "Month", "Cases"), use_container_width=True)

    section_title("On-Premise by State — YTD vs March")
    st.plotly_chart(
        horizontal_grouped_bar(on_states.head(10), "State", "YTD 9L", "Mar 9L", "YTD 9L", "Mar 9L"),
        use_container_width=True,
    )

    section_title("Full On-Premise State Detail")
    st.dataframe(on_states, hide_index=True, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# OFF-PREMISE
# ══════════════════════════════════════════════════════════════════════════════
elif active_tab == "Off-Premise":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi("YTD 9L Equiv", "1,079.67", "Off-Premise total", dark=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("YTD PODs", "765", "Points of distribution"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("March 9L", "353.50", "402 active PODs"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("Top State (YTD)", "CA", "310.33 9L - 225 PODs"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Off-Premise Monthly Trend")
    st.plotly_chart(bar_chart(off_monthly, "Month", "Cases"), use_container_width=True)

    section_title("Off-Premise by State — YTD vs March")
    st.plotly_chart(
        horizontal_grouped_bar(off_states.head(10), "State", "YTD 9L", "Mar 9L", "YTD 9L", "Mar 9L"),
        use_container_width=True,
    )

    section_title("Full Off-Premise State Detail")
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
    display_df = gopuff_location_detail.fillna("-")
    st.dataframe(display_df, hide_index=True, use_container_width=True)


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
            <div style="background:{RED}; padding:22px 16px; text-align:center;">
                <span style="font-size:48px; font-weight:900; color:white; font-family:'Anton','Impact',sans-serif; line-height:1;">19</span><br>
                <span style="font-size:9px; color:rgba(255,255,255,0.7); letter-spacing:0.12em; text-transform:uppercase;">New Customers</span><br>
                <span style="font-size:22px; color:white; font-weight:900; font-family:'Anton','Impact',sans-serif;">83%</span>
            </div>""", unsafe_allow_html=True)
        with acq2:
            st.markdown(f"""
            <div style="background:{RED_MID}; padding:22px 16px; text-align:center;">
                <span style="font-size:48px; font-weight:900; color:white; font-family:'Anton','Impact',sans-serif; line-height:1;">4</span><br>
                <span style="font-size:9px; color:rgba(255,255,255,0.7); letter-spacing:0.12em; text-transform:uppercase;">Repeat Customers</span><br>
                <span style="font-size:22px; color:white; font-weight:900; font-family:'Anton','Impact',sans-serif;">17%</span>
            </div>""", unsafe_allow_html=True)

    with col4:
        section_title("Discount Code Usage")
        st.dataframe(rb_discounts, hide_index=True, use_container_width=True)
        st.caption("* All coupons had $0.00 discount value")

    # Top SKU banner
    st.markdown(f"""
    <div class="highlight-banner">
        <div>
            <p style="margin:0; font-size:9px; color:rgba(255,255,255,0.55); letter-spacing:0.2em; text-transform:uppercase;">Top Item Sold</p>
            <p style="margin:6px 0 0; font-size:17px; color:white; font-weight:900; font-family:'Anton','Impact',sans-serif; letter-spacing:0.04em;">LUCCI LAMBRUSCO REGGIANO DOC DRY SPARKLING WINE</p>
            <p style="margin:4px 0 0; font-size:11px; color:rgba(255,255,255,0.6);">Only SKU - 100% of Champagne & Sparkling category</p>
        </div>
        <div style="display:flex; gap:28px; flex-shrink:0;">
            <div style="text-align:center;">
                <p style="margin:0; font-size:32px; font-weight:900; color:white; font-family:'Anton','Impact',sans-serif; line-height:1;">73</p>
                <p style="margin:4px 0 0; font-size:9px; color:rgba(255,255,255,0.55); letter-spacing:0.15em;">UNITS</p>
            </div>
            <div style="text-align:center;">
                <p style="margin:0; font-size:32px; font-weight:900; color:white; font-family:'Anton','Impact',sans-serif; line-height:1;">$1,478</p>
                <p style="margin:4px 0 0; font-size:9px; color:rgba(255,255,255,0.55); letter-spacing:0.15em;">REVENUE</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown('<p class="footer-text">Data Period: Nov 2025 - Mar 2026 - Lucci Sales Intelligence</p>', unsafe_allow_html=True)

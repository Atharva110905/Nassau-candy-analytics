import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy | Profitability Dashboard",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — Bold & Colorful Theme ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Global ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0F0C29 0%, #302B63 50%, #24243E 100%);
    min-height: 100vh;
}
[data-testid="stMain"] > div { padding-top: 1rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0533 0%, #2D1B69 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: #E8D5FF !important; }
[data-testid="stSidebar"] .stSlider > div > div > div { background: #FF6B9D !important; }
[data-testid="stSidebar"] label { color: #C9B8E8 !important; font-size: 12px !important; font-weight: 500 !important; }
[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: white !important; border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 8px !important;
}

/* ── KPI metric cards ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 1.1rem 1.25rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: transform 0.2s;
}
[data-testid="metric-container"]:hover { transform: translateY(-2px); }
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 11px !important; font-weight: 600 !important;
    color: #C9B8E8 !important; text-transform: uppercase; letter-spacing: 0.06em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 28px !important; font-weight: 800 !important; color: #FFFFFF !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] { color: #7EFFA0 !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.06);
    border-radius: 12px; padding: 5px; gap: 4px;
    border: 1px solid rgba(255,255,255,0.1);
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 9px; font-size: 13px; font-weight: 500;
    color: #C9B8E8; padding: 8px 20px;
    transition: all 0.2s;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, #FF6B9D, #C850C0) !important;
    color: #FFFFFF !important; font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(255,107,157,0.4) !important;
}

/* ── Section headers ── */
.section-header {
    font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase;
    background: linear-gradient(90deg, #FF6B9D, #C850C0);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 1.5rem 0 0.75rem;
}

/* ── Page title ── */
.page-title {
    font-size: 30px; font-weight: 800;
    background: linear-gradient(90deg, #FF6B9D 0%, #C850C0 50%, #4FACFE 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 2px;
}
.page-sub { font-size: 13px; color: #A89BC8; margin-bottom: 1rem; }

/* ── Insight box ── */
.insight-box {
    background: linear-gradient(135deg, rgba(255,107,157,0.12), rgba(200,80,192,0.08));
    border: 1px solid rgba(255,107,157,0.25);
    border-left: 4px solid #FF6B9D;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px; margin: 10px 0;
    font-size: 13px; color: #E8D5FF; line-height: 1.7;
    backdrop-filter: blur(6px);
}
.insight-box strong { color: #FF6B9D; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    overflow: hidden;
}

/* ── Divider ── */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,107,157,0.4), transparent);
    margin: 1rem 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.04); }
::-webkit-scrollbar-thumb { background: rgba(255,107,157,0.4); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

COLORS   = {"Chocolate": "#FF6B9D", "Sugar": "#4FACFE", "Other": "#FFBE0B"}
ACCENT   = "#FF6B9D"
FONT_COL = "#E8D5FF"

@st.cache_data
def load_data():
    df = pd.read_csv("Nassau Candy Distributor.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  dayfirst=True)
    df["Gross Margin (%)"] = (df["Gross Profit"] / df["Sales"] * 100).round(2)
    df["Profit per Unit"]  = (df["Gross Profit"] / df["Units"]).round(3)
    df["Month"]   = df["Order Date"].dt.to_period("M").astype(str)
    df["Quarter"] = "Q" + df["Order Date"].dt.quarter.astype(str) + " " + df["Order Date"].dt.year.astype(str)
    return df

df_raw = load_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #FF6B9D, #C850C0);
        border-radius: 12px; padding: 14px 16px; margin-bottom: 16px;
        text-align: center;
    ">
        <div style="font-size: 26px;">🍬</div>
        <div style="font-size: 15px; font-weight: 800; color: white;">Nassau Candy</div>
        <div style="font-size: 11px; color: rgba(255,255,255,0.75); margin-top: 2px;">Profitability Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("#### 🔍 Filters")

    min_date = df_raw["Order Date"].min().date()
    max_date = df_raw["Order Date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)

    divisions  = st.multiselect("Division",  sorted(df_raw["Division"].unique()),
                                default=sorted(df_raw["Division"].unique()))
    regions    = st.multiselect("Region",    sorted(df_raw["Region"].unique()),
                                default=sorted(df_raw["Region"].unique()))
    ship_modes = st.multiselect("Ship mode", sorted(df_raw["Ship Mode"].unique()),
                                default=sorted(df_raw["Ship Mode"].unique()))

    st.markdown("#### Margin risk threshold")
    margin_threshold = st.slider("Flag products below (%)", 0, 80, 50, 5)

    st.markdown("#### Product search")
    product_search = st.text_input("Search product name", placeholder="e.g. Wonka, Nerds…")

    st.markdown("---")
    st.markdown("<p style='font-size:11px;'>Data: 2024–2025 · 10,194 orders</p>", unsafe_allow_html=True)

# ── Filters ────────────────────────────────────────────────────────────────────
if len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_date, end_date = df_raw["Order Date"].min(), df_raw["Order Date"].max()

df = df_raw[
    (df_raw["Order Date"] >= start_date) & (df_raw["Order Date"] <= end_date) &
    (df_raw["Division"].isin(divisions)) &
    (df_raw["Region"].isin(regions)) &
    (df_raw["Ship Mode"].isin(ship_modes))
].copy()

if product_search:
    df = df[df["Product Name"].str.contains(product_search, case=False, na=False)]

if df.empty:
    st.warning("No data matches your filters. Please adjust the sidebar selections.")
    st.stop()

# ── Aggregations ───────────────────────────────────────────────────────────────
total_sales  = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
total_units  = df["Units"].sum()
total_orders = len(df)
overall_gm   = total_profit / total_sales * 100 if total_sales > 0 else 0

prod_agg = df.groupby("Product Name").agg(
    Division=("Division", "first"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum"),
    Orders=("Row ID", "count"),
).reset_index()
prod_agg["GM_%"]             = (prod_agg["Total_Profit"] / prod_agg["Total_Sales"] * 100).round(2)
prod_agg["Profit_per_Unit"]  = (prod_agg["Total_Profit"] / prod_agg["Total_Units"]).round(3)
prod_agg["Rev_Share_%"]      = (prod_agg["Total_Sales"]  / total_sales  * 100).round(2)
prod_agg["Profit_Share_%"]   = (prod_agg["Total_Profit"] / total_profit * 100).round(2)

div_agg = df.groupby("Division").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum"),
    Orders=("Row ID", "count"),
).reset_index()
div_agg["GM_%"] = (div_agg["Total_Profit"] / div_agg["Total_Sales"] * 100).round(2)

region_agg = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum"),
).reset_index()
region_agg["GM_%"] = (region_agg["Total_Profit"] / region_agg["Total_Sales"] * 100).round(2)

monthly_agg = df.groupby(["Month", "Division"]).agg(
    Sales=("Sales", "sum"),
    Profit=("Gross Profit", "sum"),
).reset_index().sort_values("Month")

# ── Header & KPIs ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, #FF6B9D 0%, #C850C0 40%, #4FACFE 100%);
    border-radius: 20px; padding: 28px 32px; margin-bottom: 24px;
    box-shadow: 0 20px 60px rgba(255,107,157,0.35);
    position: relative; overflow: hidden;
">
    <div style="position:absolute;top:-40px;right:-40px;width:200px;height:200px;
        background:rgba(255,255,255,0.06);border-radius:50%;"></div>
    <div style="position:absolute;bottom:-60px;right:80px;width:150px;height:150px;
        background:rgba(255,255,255,0.04);border-radius:50%;"></div>
    <div style="font-size:13px;font-weight:600;color:rgba(255,255,255,0.75);
        text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">
        🍬 Nassau Candy Distributor
    </div>
    <div style="font-size:32px;font-weight:800;color:white;line-height:1.15;margin-bottom:8px;">
        Product Line Profitability &<br>Margin Performance Dashboard
    </div>
    <div style="font-size:13px;color:rgba(255,255,255,0.75);">
        2024–2025 · 10,194 Orders · 15 Products · 3 Divisions · 4 Regions
    </div>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 Total Revenue",  f"${total_sales:,.0f}")
k2.metric("📈 Gross Profit",   f"${total_profit:,.0f}")
k3.metric("🎯 Overall Margin", f"{overall_gm:.1f}%")
k4.metric("📦 Units Sold",     f"{total_units:,}")
k5.metric("🧾 Total Orders",   f"{total_orders:,}")
st.markdown("---")

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Product Profitability",
    "🏭 Division Performance",
    "📊 Pareto / Concentration",
    "⚠️ Margin Risk Flags",
])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — Product Profitability
# ══════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<p class="section-header">Gross margin % by product</p>', unsafe_allow_html=True)

    prod_sorted_gm = prod_agg.sort_values("GM_%", ascending=True)
    bar_colors = [COLORS.get(d, "#8B7355") for d in prod_sorted_gm["Division"]]

    fig_gm = go.Figure(go.Bar(
        x=prod_sorted_gm["GM_%"], y=prod_sorted_gm["Product Name"],
        orientation="h", marker_color=bar_colors,
        text=prod_sorted_gm["GM_%"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Margin: %{x:.1f}%<extra></extra>",
    ))
    fig_gm.add_vline(x=margin_threshold, line_dash="dot", line_color="#E8634A",
                     annotation_text=f"Risk threshold {margin_threshold}%",
                     annotation_position="top right", annotation_font_size=11)
    fig_gm.update_layout(
        height=420, margin=dict(l=0, r=60, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Gross margin (%)", gridcolor="rgba(255,255,255,0.08)", range=[0, 105]),
        yaxis=dict(title="", tickfont=dict(size=12, color='#C9B8E8')), showlegend=False,
    )
    st.plotly_chart(fig_gm, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<p class="section-header">Total gross profit by product (top 10)</p>', unsafe_allow_html=True)
        top10 = prod_agg.sort_values("Total_Profit", ascending=False).head(10)
        fig_tp = go.Figure(go.Bar(
            x=top10["Total_Profit"], y=top10["Product Name"], orientation="h",
            marker_color=[COLORS.get(d, "#8B7355") for d in top10["Division"]],
            text=top10["Total_Profit"].apply(lambda v: f"${v:,.0f}"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Profit: $%{x:,.0f}<extra></extra>",
        ))
        fig_tp.update_layout(
            height=340, margin=dict(l=0, r=70, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickprefix="$"),
            yaxis=dict(title="", tickfont=dict(size=11, color='#C9B8E8')), showlegend=False,
        )
        st.plotly_chart(fig_tp, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-header">Profit per unit</p>', unsafe_allow_html=True)
        ppu_sorted = prod_agg.sort_values("Profit_per_Unit", ascending=False)
        ppu_colors = ["#E8634A" if v >= 2 else "#4ABDE8" if v >= 1 else "#F7C59F"
                      for v in ppu_sorted["Profit_per_Unit"]]
        fig_ppu = go.Figure(go.Bar(
            x=ppu_sorted["Product Name"], y=ppu_sorted["Profit_per_Unit"],
            marker_color=ppu_colors,
            text=ppu_sorted["Profit_per_Unit"].apply(lambda v: f"${v:.2f}"),
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Profit/unit: $%{y:.2f}<extra></extra>",
        ))
        fig_ppu.update_layout(
            height=340, margin=dict(l=0, r=10, t=30, b=100),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickangle=-35, tickfont=dict(size=10, color='#C9B8E8'), gridcolor="rgba(255,255,255,0.08)"),
            yaxis=dict(tickprefix="$", gridcolor="rgba(255,255,255,0.08)"), showlegend=False,
        )
        st.plotly_chart(fig_ppu, use_container_width=True)

    st.markdown('<p class="section-header">Full product breakdown</p>', unsafe_allow_html=True)
    display_df = prod_agg.sort_values("Total_Profit", ascending=False)[
        ["Product Name","Division","Total_Sales","Total_Profit","GM_%","Profit_per_Unit","Total_Units","Rev_Share_%"]
    ].rename(columns={
        "Total_Sales":"Revenue ($)","Total_Profit":"Gross Profit ($)",
        "GM_%":"Margin %","Profit_per_Unit":"Profit/Unit ($)",
        "Total_Units":"Units","Rev_Share_%":"Rev Share %",
    }).copy()
    display_df["Revenue ($)"]      = display_df["Revenue ($)"].apply(lambda v: f"${v:,.2f}")
    display_df["Gross Profit ($)"] = display_df["Gross Profit ($)"].apply(lambda v: f"${v:,.2f}")
    display_df["Profit/Unit ($)"]  = display_df["Profit/Unit ($)"].apply(lambda v: f"${v:.2f}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════
# TAB 2 — Division Performance
# ══════════════════════════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<p class="section-header">Revenue vs gross profit by division</p>', unsafe_allow_html=True)
        fig_div = go.Figure()
        fig_div.add_trace(go.Bar(name="Revenue", x=div_agg["Division"], y=div_agg["Total_Sales"],
                                  marker_color=ACCENT,
                                  text=div_agg["Total_Sales"].apply(lambda v: f"${v:,.0f}"),
                                  textposition="outside"))
        fig_div.add_trace(go.Bar(name="Gross Profit", x=div_agg["Division"], y=div_agg["Total_Profit"],
                                  marker_color="#4ABDE8",
                                  text=div_agg["Total_Profit"].apply(lambda v: f"${v:,.0f}"),
                                  textposition="outside"))
        fig_div.update_layout(
            height=360, barmode="group", margin=dict(l=0, r=10, t=30, b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color="#C9B8E8")),
            xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
            yaxis=dict(tickprefix="$", gridcolor="rgba(255,255,255,0.08)"),
        )
        st.plotly_chart(fig_div, use_container_width=True)

    with col2:
        st.markdown('<p class="section-header">Margin % by division</p>', unsafe_allow_html=True)
        fig_dm = go.Figure(go.Bar(
            x=div_agg["Division"], y=div_agg["GM_%"],
            marker_color=[COLORS.get(d, "#8B7355") for d in div_agg["Division"]],
            text=div_agg["GM_%"].apply(lambda v: f"{v:.1f}%"), textposition="outside",
        ))
        fig_dm.add_hline(y=margin_threshold, line_dash="dot", line_color="#E8634A",
                         annotation_text=f"Threshold {margin_threshold}%")
        fig_dm.update_layout(
            height=360, margin=dict(l=0, r=10, t=30, b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            yaxis=dict(ticksuffix="%", gridcolor="rgba(255,255,255,0.08)", range=[0, 90]),
            xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        )
        st.plotly_chart(fig_dm, use_container_width=True)

    st.markdown('<p class="section-header">Monthly revenue trend by division</p>', unsafe_allow_html=True)
    fig_trend = px.line(monthly_agg, x="Month", y="Sales", color="Division",
                        color_discrete_map=COLORS, markers=True,
                        labels={"Sales": "Revenue ($)", "Month": ""})
    fig_trend.update_layout(
        height=300, margin=dict(l=0, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color="#C9B8E8")),
        xaxis=dict(tickangle=-30, tickfont=dict(size=10, color='#C9B8E8'), gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(tickprefix="$", gridcolor="rgba(255,255,255,0.08)"),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown('<p class="section-header">Performance by region</p>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        fig_reg = px.bar(region_agg.sort_values("Total_Sales", ascending=False),
                         x="Region", y=["Total_Sales","Total_Profit"],
                         barmode="group", color_discrete_sequence=[ACCENT, "#4ABDE8"],
                         labels={"value":"Amount ($)","variable":""})
        fig_reg.update_layout(
            height=300, margin=dict(l=0, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color="#C9B8E8")),
            yaxis=dict(tickprefix="$", gridcolor="rgba(255,255,255,0.08)"), xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    with col4:
        fig_reg_gm = px.bar(region_agg.sort_values("GM_%", ascending=False),
                            x="Region", y="GM_%", color="Region", text="GM_%",
                            color_discrete_sequence=[ACCENT,"#4ABDE8","#8B7355","#6B5B95"],
                            labels={"GM_%":"Gross Margin (%)"})
        fig_reg_gm.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_reg_gm.update_layout(
            height=300, margin=dict(l=0, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            yaxis=dict(ticksuffix="%", gridcolor="rgba(255,255,255,0.08)", range=[0, 80]),
            xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        )
        st.plotly_chart(fig_reg_gm, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <strong>Key insight:</strong> Chocolate dominates at 92.9% of revenue and 95.1% of gross profit.
        The "Other" division lags significantly at ~45% margin vs 67.5% for Chocolate.
        All four regions perform within a 65–66% margin band — this is a product mix issue, not a regional one.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 3 — Pareto / Concentration
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-header">Revenue concentration (Pareto chart)</p>', unsafe_allow_html=True)

    pareto = prod_agg.sort_values("Total_Sales", ascending=False).reset_index(drop=True)
    pareto["Cumulative_Rev_%"] = (pareto["Total_Sales"].cumsum() / total_sales * 100).round(2)

    fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
    fig_pareto.add_trace(go.Bar(
        x=pareto["Product Name"], y=pareto["Rev_Share_%"],
        name="Revenue share %",
        marker_color=[COLORS.get(d, "#8B7355") for d in pareto["Division"]],
        text=pareto["Rev_Share_%"].apply(lambda v: f"{v:.1f}%"), textposition="outside",
    ), secondary_y=False)
    fig_pareto.add_trace(go.Scatter(
        x=pareto["Product Name"], y=pareto["Cumulative_Rev_%"],
        name="Cumulative %", mode="lines+markers",
        line=dict(color="#1A1A2E", width=2), marker=dict(size=6),
    ), secondary_y=True)
    fig_pareto.add_hline(y=80, line_dash="dot", line_color="#E8634A",
                         annotation_text="80% threshold", secondary_y=True)
    fig_pareto.update_layout(
        height=380, margin=dict(l=0, r=10, t=30, b=100),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color="#C9B8E8")),
        xaxis=dict(tickangle=-35, tickfont=dict(size=10, color='#C9B8E8'), gridcolor="rgba(255,255,255,0.08)"),
    )
    fig_pareto.update_yaxes(title_text="Revenue share (%)", ticksuffix="%",
                             secondary_y=False, gridcolor="rgba(255,255,255,0.08)")
    fig_pareto.update_yaxes(title_text="Cumulative revenue (%)", ticksuffix="%",
                             secondary_y=True, range=[0, 105])
    st.plotly_chart(fig_pareto, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-header">Revenue share vs gross margin (bubble = revenue size)</p>',
                    unsafe_allow_html=True)
        fig_bubble = px.scatter(
            prod_agg, x="Rev_Share_%", y="GM_%", size="Total_Sales",
            color="Division", color_discrete_map=COLORS,
            hover_name="Product Name", text="Product Name",
            labels={"Rev_Share_%":"Revenue share (%)","GM_%":"Gross margin (%)"},
            size_max=50,
        )
        fig_bubble.add_hline(y=margin_threshold, line_dash="dot", line_color="#E8634A")
        fig_bubble.update_traces(textposition="top center", textfont_size=9)
        fig_bubble.update_layout(
            height=380, margin=dict(l=0, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color="#C9B8E8")),
            xaxis=dict(gridcolor="rgba(255,255,255,0.08)", ticksuffix="%"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.08)", ticksuffix="%"),
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

    with col2:
        st.markdown('<p class="section-header">Gross profit share by division</p>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=div_agg["Division"], values=div_agg["Total_Profit"],
            hole=0.45,
            marker_colors=[COLORS.get(d, "#8B7355") for d in div_agg["Division"]],
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Profit: $%{value:,.0f}<br>Share: %{percent}<extra></extra>",
        ))
        fig_pie.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(text="Profit<br>mix", x=0.5, y=0.5,
                              font_size=13, showarrow=False)],
            legend=dict(orientation="h", yanchor="bottom", y=-0.1),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    top5_rev  = pareto.head(5)["Rev_Share_%"].sum()
    top5_prof = pareto.head(5)["Profit_Share_%"].sum()
    st.markdown(f"""
    <div class="insight-box">
        <strong>Pareto finding:</strong> The top 5 products (all Wonka Bar variants) account for
        <strong>{top5_rev:.1f}%</strong> of revenue and <strong>{top5_prof:.1f}%</strong> of gross profit.
        The remaining 10 products together represent less than 7% of total revenue — a classic 80/20 concentration.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 4 — Margin Risk Flags
# ══════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(f'<p class="section-header">Products flagged below {margin_threshold}% gross margin</p>',
                unsafe_allow_html=True)

    risk_prods = prod_agg[prod_agg["GM_%"] < margin_threshold].sort_values("GM_%").copy()

    if risk_prods.empty:
        st.success(f"No products below the {margin_threshold}% threshold with current filters.")
    else:
        def risk_label(gm):
            if gm < 20: return "Critical"
            if gm < 40: return "High"
            if gm < 50: return "Medium"
            return "Low"

        risk_prods["Risk Level"] = risk_prods["GM_%"].apply(risk_label)
        risk_prods["Recommended Action"] = risk_prods["GM_%"].apply(
            lambda g: "Discontinuation review" if g < 20
            else "Cost renegotiation / reprice" if g < 40
            else "Monitor & review pricing"
        )

        header = st.columns([3, 1.5, 1.5, 1.5, 3])
        for col, label in zip(header, ["Product", "Division", "Margin %", "Risk", "Action"]):
            col.markdown(f"**{label}**")
        st.markdown("---")

        badge_map = {
            "Critical": ("🔴", "#FEE2E2", "#991B1B"),
            "High":     ("🟠", "#FEF3C7", "#92400E"),
            "Medium":   ("🟡", "#FEF9C3", "#713F12"),
            "Low":      ("🟢", "#DCFCE7", "#166534"),
        }
        for _, row in risk_prods.iterrows():
            c1, c2, c3, c4, c5 = st.columns([3, 1.5, 1.5, 1.5, 3])
            c1.markdown(f"**{row['Product Name']}**")
            c2.markdown(row["Division"])
            c3.markdown(f"**{row['GM_%']:.1f}%**")
            emoji, bg, fg = badge_map.get(row["Risk Level"], ("⚪","#F3F4F6","#374151"))
            c4.markdown(f"{emoji} {row['Risk Level']}")
            c5.markdown(f"*{row['Recommended Action']}*")
        st.markdown("---")

    st.markdown('<p class="section-header">Cost vs sales scatter — identify pricing inefficiencies</p>',
                unsafe_allow_html=True)
    scatter_agg = prod_agg.copy()
    scatter_agg["Cost"] = scatter_agg["Total_Sales"] - scatter_agg["Total_Profit"]

    fig_scatter = px.scatter(
        scatter_agg, x="Cost", y="Total_Sales", size="Total_Units",
        color="GM_%", color_continuous_scale=["#E24B4A","#F7C59F","#4ABDE8","#1D9E75"],
        range_color=[0, 100], hover_name="Product Name", text="Product Name",
        labels={"Cost":"Total Cost ($)","Total_Sales":"Total Revenue ($)","GM_%":"Margin %"},
        size_max=50,
    )
    max_val = max(scatter_agg["Total_Sales"].max(), scatter_agg["Cost"].max()) * 1.05
    fig_scatter.add_trace(go.Scatter(
        x=[0, max_val], y=[0, max_val], mode="lines",
        line=dict(color="#E8634A", dash="dot", width=1.5),
        name="Break-even line", hoverinfo="skip",
    ))
    fig_scatter.update_traces(selector=dict(mode="markers+text"),
                               textposition="top center", textfont_size=9)
    fig_scatter.update_layout(
        height=420, margin=dict(l=0, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickprefix="$", gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(tickprefix="$", gridcolor="rgba(255,255,255,0.08)"),
        coloraxis_colorbar=dict(title="Margin %", ticksuffix="%"),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown('<p class="section-header">All products — margin % with risk threshold line</p>',
                unsafe_allow_html=True)
    all_sorted = prod_agg.sort_values("GM_%", ascending=True)
    bar_risk_colors = ["#E24B4A" if v < margin_threshold else ACCENT for v in all_sorted["GM_%"]]

    fig_all = go.Figure(go.Bar(
        x=all_sorted["GM_%"], y=all_sorted["Product Name"], orientation="h",
        marker_color=bar_risk_colors,
        text=all_sorted["GM_%"].apply(lambda v: f"{v:.1f}%"), textposition="outside",
        hovertemplate="<b>%{y}</b><br>Margin: %{x:.1f}%<extra></extra>",
    ))
    fig_all.add_vline(x=margin_threshold, line_dash="dot", line_color="#1A1A2E",
                      annotation_text=f"Threshold: {margin_threshold}%",
                      annotation_position="top right", annotation_font_size=11)
    fig_all.update_layout(
        height=420, margin=dict(l=0, r=70, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
        xaxis=dict(ticksuffix="%", gridcolor="rgba(255,255,255,0.08)", range=[0, 105]),
        yaxis=dict(tickfont=dict(size=11, color='#C9B8E8')),
    )
    st.plotly_chart(fig_all, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <strong>Critical alert — Kazookles:</strong> Only 7.7% gross margin despite 371 units sold.
        Generates just $92.75 in profit on $1,206 revenue — a near-zero contribution.
        <strong>Fun Dip (40%), Nerds (46.7%), and SweeTARTS (46.7%)</strong> also sit dangerously close
        to the threshold. All four at-risk products are in the Sugar or Other divisions.
    </div>""", unsafe_allow_html=True)

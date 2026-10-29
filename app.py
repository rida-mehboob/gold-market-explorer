import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Gold Market Explorer", page_icon="🟡", layout="wide")
DATA = Path(__file__).parent / "data"

@st.cache_data
def load(name):
    df = pd.read_csv(DATA / f"{name}.csv")
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df

price = load("price")
etf = load("etf")
declared = load("declared")
gap = load("gap")
swiss = load("swiss")

st.title("🟡 Gold Market Explorer")
st.caption("Interactive data-visualisation dashboard · All included figures are synthetic practice data, not real market statistics.")
st.info("This dashboard is an educational adaptation. Replace the sample CSVs with verified data and cite the source before using it for real-world analysis.")

latest_price = price.iloc[-1]["price_usd_oz"]
price_change = latest_price - price.iloc[0]["price_usd_oz"]
latest_holdings = etf.iloc[-1]["fund_a_tonnes"] + etf.iloc[-1]["fund_b_tonnes"]
latest_period = price.iloc[-1]["date"].strftime("%b %Y")
c1,c2,c3,c4 = st.columns(4)
c1.metric("Latest sample price", f"${latest_price:,.0f}/oz", f"{price_change:+,.0f} over period")
c2.metric("Latest fund holdings", f"{latest_holdings:,.0f} tonnes", "Fund A + Fund B")
c3.metric("Countries represented", f"{declared['country'].nunique()}")
c4.metric("Latest sample month", latest_period)

tab_declared, tab_inferred, tab_explore = st.tabs(["Declared", "Inferred", "Explore a country"])

with tab_declared:
    st.subheader("Gold price over time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=price["date"], y=price["price_usd_oz"], mode="lines", name="Sample gold price"))
    fig.add_trace(go.Scatter(x=price["date"], y=price["comparison_price_usd_oz"], mode="lines", name="Comparison series", line=dict(dash="dash")))
    fig.update_layout(xaxis_title="Date", yaxis_title="USD per troy ounce", hovermode="x unified", legend_title="")
    st.plotly_chart(fig, use_container_width=True)

    left,right = st.columns([3,2], gap="large")
    with left:
        st.subheader("Investment fund holdings")
        holdings = etf.melt(id_vars="date", var_name="fund", value_name="tonnes")
        holdings["fund"] = holdings["fund"].map({"fund_a_tonnes":"Fund A","fund_b_tonnes":"Fund B"})
        fig = px.line(holdings, x="date", y="tonnes", color="fund", markers=False,
                      labels={"date":"Date","tonnes":"Gold held (tonnes)","fund":"Fund"})
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Net purchases by country")
        totals = declared.groupby("country", as_index=False)["net_purchases_t"].sum().sort_values("net_purchases_t")
        fig = px.bar(totals, x="net_purchases_t", y="country", orientation="h",
                     labels={"net_purchases_t":"Net purchases (tonnes)","country":"Country"})
        fig.add_vline(x=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig, use_container_width=True)
    st.caption("Country bars aggregate all months in the supplied practice dataset. Positive values indicate net buying; negative values indicate net selling.")

with tab_inferred:
    st.subheader("Reported purchases and estimate")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=gap["date"], y=gap["reported_purchases_t"], name="Reported purchases"))
    fig.add_trace(go.Scatter(x=gap["date"], y=gap["estimated_purchases_t"], name="Estimated purchases", mode="lines+markers", line=dict(dash="dash")))
    fig.update_layout(xaxis_title="Quarter", yaxis_title="Tonnes", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Exports by destination")
    fig = px.area(swiss, x="date", y="exports_t", color="destination",
                  labels={"date":"Month","exports_t":"Exports (tonnes)","destination":"Destination"})
    st.plotly_chart(fig, use_container_width=True)
    st.caption("The bars and dashed line distinguish reported values from estimates. Export series show total volume and each destination's contribution.")

with tab_explore:
    st.subheader("Explore monthly activity for one country")
    country = st.selectbox("Choose a country", sorted(declared["country"].unique()))
    country_data = declared[declared["country"] == country].sort_values("date")
    fig = px.bar(country_data, x="date", y="net_purchases_t",
                 labels={"date":"Month","net_purchases_t":"Net purchases / sales (tonnes)"},
                 title=f"{country}: monthly purchases and sales (sample data)")
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("**How to read this chart:** bars above zero represent net buying; bars below zero represent net selling in this sample dataset.")
    with st.expander("View selected country's data"):
        st.dataframe(country_data, use_container_width=True, hide_index=True)

with st.expander("About this adaptation"):
    st.write("The dashboard follows the activity's design principles: summary metrics first, a prominent time-series chart, related comparisons grouped in tabs, consistent labels, and a country selector for monthly detail.")
    st.write("All CSVs in the included data folder are synthetic practice data created for this demonstration. They must not be represented as verified gold-market data.")

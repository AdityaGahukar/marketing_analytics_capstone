import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.title("🏠 Executive Overview")
st.markdown("High-level snapshot of overall marketing campaign performance.")

# ── Filters ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Filters")

    years_df = session.sql("SELECT DISTINCT year FROM dim_date ORDER BY year").to_pandas()
    years = ["All"] + sorted(years_df["YEAR"].dropna().astype(int).tolist())
    selected_year = st.selectbox("Year", years)

    channels_df = session.sql("SELECT DISTINCT channel_used FROM dim_channel ORDER BY channel_used").to_pandas()
    channels = ["All"] + channels_df["CHANNEL_USED"].dropna().tolist()
    selected_channel = st.selectbox("Channel", channels)

    companies_df = session.sql("SELECT DISTINCT company FROM dim_company ORDER BY company").to_pandas()
    companies = ["All"] + companies_df["COMPANY"].dropna().tolist()
    selected_company = st.selectbox("Company", companies)

# ── Build WHERE clause ──────────────────────────────────────────────────────
conditions = []
if selected_year != "All":
    conditions.append(f"d.year = {selected_year}")
if selected_channel != "All":
    conditions.append(f"f.channel_used = '{selected_channel}'")
if selected_company != "All":
    conditions.append(f"f.company = '{selected_company}'")

where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

# ── KPI Cards ───────────────────────────────────────────────────────────────
kpi_query = f"""
    SELECT
        SUM(f.total_clicks)                                              AS total_clicks,
        SUM(f.total_impressions)                                         AS total_impressions,
        SUM(f.total_cost)                                                AS total_cost,
        CASE WHEN SUM(f.total_impressions) > 0
             THEN SUM(f.total_clicks) / SUM(f.total_impressions) END     AS ctr,
        AVG(f.avg_roi)                                                   AS avg_roi,
        AVG(f.avg_conversion_rate)                                       AS avg_conversion_rate
    FROM fact_campaign_performance f
    LEFT JOIN dim_date d ON f.date = d.date
    {where}
"""
kpi = session.sql(kpi_query).to_pandas().iloc[0]

# First row
c1, c2, c3 = st.columns(3)
c1.metric("🖱️ Total Clicks",       f"{int(kpi['TOTAL_CLICKS']):,}")
c2.metric("👁️ Total Impressions",  f"{int(kpi['TOTAL_IMPRESSIONS']):,}")
c3.metric("💰 Total Cost",         f"${kpi['TOTAL_COST']:,.0f}")

# Second row
c4, c5, c6 = st.columns(3)
c4.metric("📊 Avg CTR",            f"{kpi['CTR']*100:.2f}%")
c5.metric("📈 Avg ROI",            f"{kpi['AVG_ROI']:.2f}x")
c6.metric("🔁 Avg Conversion Rate",f"{kpi['AVG_CONVERSION_RATE']*100:.2f}%")
st.divider()

# ── Daily Trend ─────────────────────────────────────────────────────────────
st.subheader("📅 Daily Trend — Clicks & Impressions")

daily_query = f"""
    SELECT
        DATE_TRUNC('day', f.date)                                        AS date,
        SUM(f.total_clicks)                                              AS total_clicks,
        SUM(f.total_impressions)                                         AS total_impressions,
        CASE WHEN SUM(f.total_impressions) > 0
             THEN SUM(f.total_clicks) / SUM(f.total_impressions) END     AS ctr
    FROM fact_campaign_performance f
    LEFT JOIN dim_date d ON f.date = d.date
    {where}
    GROUP BY 1
    ORDER BY 1
"""
daily_df = session.sql(daily_query).to_pandas()
daily_df.columns = daily_df.columns.str.upper()

fig_daily = go.Figure()
fig_daily.add_trace(go.Scatter(x=daily_df["DATE"], y=daily_df["TOTAL_CLICKS"],
                               name="Clicks", mode="lines", line=dict(color="#636EFA")))
fig_daily.add_trace(go.Scatter(x=daily_df["DATE"], y=daily_df["TOTAL_IMPRESSIONS"],
                               name="Impressions", mode="lines", line=dict(color="#EF553B")))
fig_daily.update_layout(title="Daily Clicks vs Impressions", xaxis_title="Date",
                        yaxis_title="Count", legend_title="Metric",
                        hovermode="x unified", height=400)
st.plotly_chart(fig_daily, use_container_width=True)

st.divider()

# ── Channel Quick Compare ───────────────────────────────────────────────────
st.subheader("📣 Channel Performance at a Glance")

channel_query = f"""
    SELECT
        f.channel_used,
        SUM(f.total_clicks)                                              AS total_clicks,
        SUM(f.total_impressions)                                         AS total_impressions,
        CASE WHEN SUM(f.total_impressions) > 0
             THEN SUM(f.total_clicks) / SUM(f.total_impressions) END     AS ctr,
        AVG(f.avg_roi)                                                   AS avg_roi
    FROM fact_campaign_performance f
    LEFT JOIN dim_date d ON f.date = d.date
    {where}
    GROUP BY f.channel_used
    ORDER BY total_clicks DESC
"""
ch_df = session.sql(channel_query).to_pandas()
ch_df.columns = ch_df.columns.str.upper()

col1, col2 = st.columns(2)
with col1:
    fig_ch_clicks = px.bar(ch_df, x="CHANNEL_USED", y="TOTAL_CLICKS",
                           color="CHANNEL_USED", title="Total Clicks by Channel",
                           labels={"CHANNEL_USED": "Channel", "TOTAL_CLICKS": "Clicks"})
    st.plotly_chart(fig_ch_clicks, use_container_width=True)

with col2:
    fig_ch_roi = px.bar(ch_df, x="CHANNEL_USED", y="AVG_ROI",
                        color="CHANNEL_USED", title="Avg ROI by Channel",
                        labels={"CHANNEL_USED": "Channel", "AVG_ROI": "ROI"})
    st.plotly_chart(fig_ch_roi, use_container_width=True)
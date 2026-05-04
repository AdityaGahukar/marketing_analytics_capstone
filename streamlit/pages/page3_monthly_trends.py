import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.title("📈 Monthly Trends")
st.markdown("Month-over-month and quarter-over-quarter performance trends.")

# ── Filters ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Filters")

    years_df = session.sql("SELECT DISTINCT year FROM dim_date ORDER BY year").to_pandas()
    all_years = sorted(years_df["YEAR"].dropna().astype(int).tolist())
    selected_years = st.multiselect("Year", all_years, default=all_years)

    quarters_df = session.sql("SELECT DISTINCT quarter FROM dim_date ORDER BY quarter").to_pandas()
    all_quarters = sorted(quarters_df["QUARTER"].dropna().astype(int).tolist())
    selected_quarters = st.multiselect("Quarter", all_quarters, default=all_quarters)

    channels_df = session.sql("SELECT DISTINCT channel_used FROM dim_channel ORDER BY channel_used").to_pandas()
    channels = channels_df["CHANNEL_USED"].dropna().tolist()
    selected_channels = st.multiselect("Channel", channels, default=channels)

# ── WHERE clause ────────────────────────────────────────────────────────────
def sql_list(lst):
    return "(" + ", ".join(f"'{v}'" for v in lst) + ")"

def sql_int_list(lst):
    return "(" + ", ".join(str(v) for v in lst) + ")"

conditions = []
if selected_years:
    conditions.append(f"d.year IN {sql_int_list(selected_years)}")
if selected_quarters:
    conditions.append(f"d.quarter IN {sql_int_list(selected_quarters)}")
if selected_channels:
    conditions.append(f"f.channel_used IN {sql_list(selected_channels)}")

where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

# ── Monthly Aggregation ─────────────────────────────────────────────────────
monthly_query = f"""
    SELECT
        d.year,
        d.month,
        d.month_name,
        d.quarter,
        SUM(f.total_clicks)                                              AS total_clicks,
        SUM(f.total_impressions)                                         AS total_impressions,
        SUM(f.total_cost)                                                AS total_cost,
        CASE WHEN SUM(f.total_impressions) > 0
             THEN SUM(f.total_clicks) / SUM(f.total_impressions) END     AS ctr,
        AVG(f.avg_roi)                                                   AS avg_roi,
        AVG(f.avg_conversion_rate)                                       AS avg_conversion_rate
    FROM fact_campaign_performance f
    JOIN dim_date d ON f.date = d.date
    {where}
    GROUP BY d.year, d.month, d.month_name, d.quarter
    ORDER BY d.year, d.month
"""
monthly_df = session.sql(monthly_query).to_pandas()
monthly_df.columns = monthly_df.columns.str.upper()
monthly_df["PERIOD"] = monthly_df["MONTH_NAME"] + " " + monthly_df["YEAR"].astype(str)

# ── Charts ──────────────────────────────────────────────────────────────────
st.subheader("🖱️ Monthly Clicks & Impressions")
fig1 = go.Figure()
for yr in monthly_df["YEAR"].unique():
    df_yr = monthly_df[monthly_df["YEAR"] == yr]
    fig1.add_trace(go.Scatter(x=df_yr["MONTH"], y=df_yr["TOTAL_CLICKS"],
                              mode="lines+markers", name=f"Clicks {yr}"))
    fig1.add_trace(go.Scatter(x=df_yr["MONTH"], y=df_yr["TOTAL_IMPRESSIONS"],
                              mode="lines+markers", name=f"Impressions {yr}",
                              line=dict(dash="dash")))
fig1.update_layout(xaxis_title="Month", yaxis_title="Count",
                   hovermode="x unified", height=400)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Monthly CTR Trend")
    fig2 = px.line(monthly_df, x="MONTH", y="CTR", color="YEAR",
                   markers=True, title="CTR by Month",
                   labels={"MONTH": "Month", "CTR": "CTR", "YEAR": "Year"})
    fig2.update_yaxes(tickformat=".2%")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("📈 Monthly ROI Trend")
    fig3 = px.line(monthly_df, x="MONTH", y="AVG_ROI", color="YEAR",
                   markers=True, title="Avg ROI by Month",
                   labels={"MONTH": "Month", "AVG_ROI": "Avg ROI", "YEAR": "Year"})
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ── Quarterly Aggregation ────────────────────────────────────────────────────
st.subheader("🗓️ Quarterly Performance")
quarterly_df = (
    monthly_df.groupby(["YEAR", "QUARTER"], as_index=False)
    .agg(TOTAL_CLICKS=("TOTAL_CLICKS", "sum"),
         TOTAL_IMPRESSIONS=("TOTAL_IMPRESSIONS", "sum"),
         TOTAL_COST=("TOTAL_COST", "sum"),
         AVG_ROI=("AVG_ROI", "mean"),
         CTR=("CTR", "mean"))
)
quarterly_df["LABEL"] = "Q" + quarterly_df["QUARTER"].astype(str) + " " + quarterly_df["YEAR"].astype(str)

col3, col4 = st.columns(2)
with col3:
    fig4 = px.bar(quarterly_df, x="LABEL", y="TOTAL_CLICKS", color="YEAR",
                  title="Total Clicks per Quarter",
                  labels={"LABEL": "Quarter", "TOTAL_CLICKS": "Clicks"})
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    fig5 = px.bar(quarterly_df, x="LABEL", y="AVG_ROI", color="YEAR",
                  title="Avg ROI per Quarter",
                  labels={"LABEL": "Quarter", "AVG_ROI": "Avg ROI"})
    st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ── Cost Trend ──────────────────────────────────────────────────────────────
st.subheader("💰 Monthly Cost Trend")
fig6 = px.area(monthly_df, x="MONTH", y="TOTAL_COST", color="YEAR",
               title="Total Cost by Month",
               labels={"MONTH": "Month", "TOTAL_COST": "Total Cost", "YEAR": "Year"})
st.plotly_chart(fig6, use_container_width=True)
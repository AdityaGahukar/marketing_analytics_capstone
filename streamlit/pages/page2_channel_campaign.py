import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.title("📣 Channel & Campaign Performance")
st.markdown("Detailed breakdown of performance across channels and individual campaigns.")

# ── Filters ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Filters")

    channels_df = session.sql("SELECT DISTINCT channel_used FROM dim_channel ORDER BY channel_used").to_pandas()
    channels = ["All"] + channels_df["CHANNEL_USED"].dropna().tolist()
    selected_channels = st.multiselect("Channel", channels[1:], default=channels[1:])

    camp_type_df = session.sql("SELECT DISTINCT campaign_type FROM dim_campaign ORDER BY campaign_type").to_pandas()
    camp_types = camp_type_df["CAMPAIGN_TYPE"].dropna().tolist()
    selected_types = st.multiselect("Campaign Type", camp_types, default=camp_types)

    audience_df = session.sql("SELECT DISTINCT target_audience FROM dim_campaign ORDER BY target_audience").to_pandas()
    audiences = audience_df["TARGET_AUDIENCE"].dropna().tolist()
    selected_audiences = st.multiselect("Target Audience", audiences, default=audiences)

    segment_df = session.sql("SELECT DISTINCT customer_segment FROM dim_campaign ORDER BY customer_segment").to_pandas()
    segments = segment_df["CUSTOMER_SEGMENT"].dropna().tolist()
    selected_segments = st.multiselect("Customer Segment", segments, default=segments)

# ── Build WHERE clause ──────────────────────────────────────────────────────
def sql_list(lst):
    return "(" + ", ".join(f"'{v}'" for v in lst) + ")"

conditions = []
if selected_channels:
    conditions.append(f"f.channel_used IN {sql_list(selected_channels)}")
if selected_types:
    conditions.append(f"dc.campaign_type IN {sql_list(selected_types)}")
if selected_audiences:
    conditions.append(f"dc.target_audience IN {sql_list(selected_audiences)}")
if selected_segments:
    conditions.append(f"dc.customer_segment IN {sql_list(selected_segments)}")

where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

# ── Channel KPIs ────────────────────────────────────────────────────────────
st.subheader("📊 Channel-Level KPIs")

ch_query = f"""
    SELECT
        f.channel_used,
        SUM(f.total_clicks)                                              AS total_clicks,
        SUM(f.total_impressions)                                         AS total_impressions,
        SUM(f.total_cost)                                                AS total_cost,
        CASE WHEN SUM(f.total_impressions) > 0
             THEN SUM(f.total_clicks) / SUM(f.total_impressions) END     AS ctr,
        AVG(f.avg_roi)                                                   AS avg_roi,
        AVG(f.avg_conversion_rate)                                       AS avg_conversion_rate
    FROM fact_campaign_performance f
    LEFT JOIN dim_campaign dc ON f.campaign_id = dc.campaign_id
    {where}
    GROUP BY f.channel_used
    ORDER BY total_clicks DESC
"""
ch_df = session.sql(ch_query).to_pandas()
ch_df.columns = ch_df.columns.str.upper()

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(ch_df, x="CHANNEL_USED", y=["TOTAL_CLICKS", "TOTAL_IMPRESSIONS"],
                 barmode="group", title="Clicks & Impressions by Channel",
                 labels={"CHANNEL_USED": "Channel", "value": "Count", "variable": "Metric"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.scatter(ch_df, x="CTR", y="AVG_ROI", size="TOTAL_COST",
                      color="CHANNEL_USED", title="CTR vs ROI by Channel (size = Cost)",
                      labels={"CTR": "CTR", "AVG_ROI": "Avg ROI", "CHANNEL_USED": "Channel"})
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    fig3 = px.pie(ch_df, names="CHANNEL_USED", values="TOTAL_COST",
                  title="Cost Distribution by Channel", hole=0.4)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.bar(ch_df, x="CHANNEL_USED", y="AVG_CONVERSION_RATE",
                  color="CHANNEL_USED", title="Avg Conversion Rate by Channel",
                  labels={"CHANNEL_USED": "Channel", "AVG_CONVERSION_RATE": "Conversion Rate"})
    fig4.update_yaxes(tickformat=".2%")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Campaign-Level ──────────────────────────────────────────────────────────
st.subheader("🎯 Campaign-Level Deep Dive")

camp_query = f"""
    SELECT
        f.campaign_id,
        dc.campaign_type,
        dc.target_audience,
        dc.customer_segment,
        f.channel_used,
        SUM(f.total_clicks)                                              AS total_clicks,
        SUM(f.total_impressions)                                         AS total_impressions,
        SUM(f.total_cost)                                                AS total_cost,
        CASE WHEN SUM(f.total_impressions) > 0
             THEN SUM(f.total_clicks) / SUM(f.total_impressions) END     AS ctr,
        AVG(f.avg_roi)                                                   AS avg_roi,
        AVG(f.avg_conversion_rate)                                       AS avg_conversion_rate
    FROM fact_campaign_performance f
    LEFT JOIN dim_campaign dc ON f.campaign_id = dc.campaign_id
    {where}
    GROUP BY f.campaign_id, dc.campaign_type, dc.target_audience, dc.customer_segment, f.channel_used
    ORDER BY total_clicks DESC
"""
camp_df = session.sql(camp_query).to_pandas()
camp_df.columns = camp_df.columns.str.upper()

col5, col6 = st.columns(2)
with col5:
    fig5 = px.bar(
        camp_df.groupby("CAMPAIGN_TYPE", as_index=False)["AVG_ROI"].mean(),
        x="CAMPAIGN_TYPE", y="AVG_ROI", color="CAMPAIGN_TYPE",
        title="Avg ROI by Campaign Type",
        labels={"CAMPAIGN_TYPE": "Type", "AVG_ROI": "Avg ROI"}
    )
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    fig6 = px.bar(
        camp_df.groupby("TARGET_AUDIENCE", as_index=False)["TOTAL_CLICKS"].sum(),
        x="TARGET_AUDIENCE", y="TOTAL_CLICKS", color="TARGET_AUDIENCE",
        title="Total Clicks by Target Audience",
        labels={"TARGET_AUDIENCE": "Audience", "TOTAL_CLICKS": "Clicks"}
    )
    st.plotly_chart(fig6, use_container_width=True)


st.divider()

# Sortable table
st.subheader("📋 Campaign Summary Table")
st.dataframe(
    camp_df[["CAMPAIGN_ID", "CAMPAIGN_TYPE", "TARGET_AUDIENCE",
             "CUSTOMER_SEGMENT", "CHANNEL_USED",
             "TOTAL_CLICKS", "TOTAL_IMPRESSIONS",
             "TOTAL_COST", "CTR", "AVG_ROI", "AVG_CONVERSION_RATE"]],
    use_container_width=True
)
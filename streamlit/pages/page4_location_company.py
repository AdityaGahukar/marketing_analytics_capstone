import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.title("🌍 Location & Company Breakdown")
st.markdown("Performance breakdown by geographic location and company.")

# ── Filters ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Filters")

    loc_df = session.sql("SELECT DISTINCT location FROM dim_location ORDER BY location").to_pandas()
    locations = loc_df["LOCATION"].dropna().tolist()
    selected_locations = st.multiselect("Location", locations, default=locations)

    comp_df = session.sql("SELECT DISTINCT company FROM dim_company ORDER BY company").to_pandas()
    companies = comp_df["COMPANY"].dropna().tolist()
    selected_companies = st.multiselect("Company", companies, default=companies)

    channels_df = session.sql("SELECT DISTINCT channel_used FROM dim_channel ORDER BY channel_used").to_pandas()
    channels = channels_df["CHANNEL_USED"].dropna().tolist()
    selected_channels = st.multiselect("Channel", channels, default=channels)

    years_df = session.sql("SELECT DISTINCT year FROM dim_date ORDER BY year").to_pandas()
    all_years = sorted(years_df["YEAR"].dropna().astype(int).tolist())
    selected_year = st.selectbox("Year", ["All"] + all_years)

# ── WHERE clause ────────────────────────────────────────────────────────────
def sql_list(lst):
    return "(" + ", ".join(f"'{v}'" for v in lst) + ")"

conditions = []
if selected_locations:
    conditions.append(f"f.location IN {sql_list(selected_locations)}")
if selected_companies:
    conditions.append(f"f.company IN {sql_list(selected_companies)}")
if selected_channels:
    conditions.append(f"f.channel_used IN {sql_list(selected_channels)}")
if selected_year != "All":
    conditions.append(f"d.year = {selected_year}")

where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

# ── Location Aggregation ────────────────────────────────────────────────────
loc_query = f"""
    SELECT
        f.location,
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
    GROUP BY f.location
    ORDER BY total_clicks DESC
"""
loc_df = session.sql(loc_query).to_pandas()
loc_df.columns = loc_df.columns.str.upper()

st.subheader("📍 Location Performance")

col1, col2 = st.columns(2)
with col1:
    fig1 = px.bar(loc_df.head(15), x="LOCATION", y="TOTAL_CLICKS",
                  color="LOCATION", title="Top Locations by Total Clicks",
                  labels={"LOCATION": "Location", "TOTAL_CLICKS": "Clicks"})
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(loc_df.head(15), x="LOCATION", y="AVG_ROI",
                  color="LOCATION", title="Top Locations by Avg ROI",
                  labels={"LOCATION": "Location", "AVG_ROI": "Avg ROI"})
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Company Aggregation ─────────────────────────────────────────────────────
comp_query = f"""
    SELECT
        f.company,
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
    GROUP BY f.company
    ORDER BY total_clicks DESC
"""
comp_df = session.sql(comp_query).to_pandas()
comp_df.columns = comp_df.columns.str.upper()

st.subheader("🏢 Company Performance")

col5, col6 = st.columns(2)
with col5:
    fig5 = px.bar(comp_df.head(15), x="COMPANY", y="TOTAL_CLICKS",
                  color="COMPANY", title="Top Companies by Total Clicks",
                  labels={"COMPANY": "Company", "TOTAL_CLICKS": "Clicks"})
    fig5.update_layout(showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    fig6 = px.bar(comp_df.head(15), x="COMPANY", y="TOTAL_COST",
                  color="COMPANY", title="Top Companies by Total Cost",
                  labels={"COMPANY": "Company", "TOTAL_COST": "Cost"})
    fig6.update_layout(showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)

st.divider()

# ── Location × Company Heatmap ──────────────────────────────────────────────
st.subheader("🔥 Location × Company ROI Heatmap")

heat_query = f"""
    SELECT
        f.location,
        f.company,
        AVG(f.avg_roi) AS avg_roi
    FROM fact_campaign_performance f
    LEFT JOIN dim_date d ON f.date = d.date
    {where}
    GROUP BY f.location, f.company
"""
heat_df = session.sql(heat_query).to_pandas()
heat_df.columns = heat_df.columns.str.upper()
heat_pivot = heat_df.pivot_table(index="LOCATION", columns="COMPANY",
                                  values="AVG_ROI", aggfunc="mean")

fig8 = px.imshow(heat_pivot, color_continuous_scale="RdYlGn",
                 title="Avg ROI — Location × Company",
                 labels={"color": "Avg ROI"}, aspect="auto")
st.plotly_chart(fig8, use_container_width=True)
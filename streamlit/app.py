import streamlit as st

st.set_page_config(
    page_title="Marketing Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

pg = st.navigation([
    st.Page("pages/page1_overview.py",          title="Executive Overview",             icon="🏠"),
    st.Page("pages/page2_channel_campaign.py",  title="Channel & Campaign Performance", icon="📣"),
    st.Page("pages/page3_monthly_trends.py",    title="Monthly Trends",                 icon="📈"),
    st.Page("pages/page4_location_company.py",  title="Location & Company Breakdown",   icon="🌍"),
])

pg.run()
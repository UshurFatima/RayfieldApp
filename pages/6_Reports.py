import streamlit as st
from utils.db import get_db_connection
import pandas as pd

def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.set_page_config(
    page_title="Reports Dashboard",
    layout="wide"
)

# Authentication check
if 'current_role' not in st.session_state:
    st.error("Please login first")
    st.stop()

# Main Dashboard
st.title("📊 Reports Dashboard")

# Metrics Overview
st.header("Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>Maintenance Summary</h3>
        <h1>78%</h1>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>Downtime Analysis</h3>
        <h1>75%</h1>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>Equipment Overview</h3>
        <h1>90%</h1>
    </div>
    """, unsafe_allow_html=True)

# Detailed Reports
st.header("Detailed Reports")
conn = get_db_connection()

# Asset Status Report
with st.expander("Asset Status Report", expanded=True):
    assets = pd.read_sql("SELECT name, status, location, alerts FROM assets", conn)
    st.dataframe(
        assets,
        use_container_width=True,
        hide_index=True
    )

# Maintenance History
with st.expander("Maintenance History"):
    work_orders = pd.read_sql("SELECT * FROM alerts", conn)
    st.dataframe(work_orders)

conn.close()

# Export Options
st.divider()
st.download_button(
    "Download Full Report",
    data=assets.to_csv().encode('utf-8'),
    file_name='asset_report.csv',
    mime='text/csv'
)
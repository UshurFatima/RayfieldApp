import streamlit as st
from utils.db import get_db_connection
import pandas as pd


def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

st.set_page_config(
    page_title="Operations Manager Dashboard",
    layout="wide"
)

# Authentication check
if 'current_role' not in st.session_state or st.session_state.current_role != "Operations Manager":
    st.error("You don't have permission to view this page")
    st.stop()

# Main Dashboard
st.title("Operations Manager")

# KPI Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>UPTIME</h3>
        <h1>95.7%</h1>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>OPEN TASKS</h3>
        <h1>5</h1>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>HIGH-RISK ASSETS</h3>
        <h1>2</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Dashboard Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Alerts", "Tasks", "Reports"])

with tab1:
    st.subheader("Asset Overview")

    # Asset Table
    conn = get_db_connection()
    assets = pd.read_sql("""
        SELECT name as ASSET, status as STATUS, 
               location as LOCATION, alerts as ALERTS 
        FROM assets
    """, conn)
    conn.close()

    st.dataframe(
        assets.style.applymap(
            lambda x: "color: red" if x == "Critical" else
            ("color: orange" if x == "Warning" else ""),
            subset=["STATUS"]
        ),
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.button("VIEW ALERTS", use_container_width=True)
    with col2:
        st.button("SCHEDULE MAINTENANCE", use_container_width=True)

with tab2:
    st.subheader("Current Alerts")
    conn = get_db_connection()
    alerts = pd.read_sql("SELECT * FROM alerts", conn)
    conn.close()

    # Alert Sections
    with st.expander("High-Priority Alert", expanded=True):
        high_alerts = alerts[alerts['severity'] == 'High']
        for _, row in high_alerts.iterrows():
            st.markdown(f"""
            <div class="alert-high">
                <p><strong>ASSET:</strong> {row['asset_id']}</p>
                <p><strong>STATUS:</strong> {row['severity']}</p>
                <p><strong>DETECTED:</strong> {row['detected']}</p>
                <p><strong>SUGGESTED ACTION:</strong> {row['suggested_action']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Assign Task", key=f"assign_{row['id']}")

    with st.expander("Medium-Priority Alert"):
        medium_alerts = alerts[alerts['severity'] == 'Medium']
        st.dataframe(medium_alerts, hide_index=True)

with tab3:
    st.subheader("Task Management")
    # Task management implementation would go here

with tab4:
    st.subheader("Reports")
    # Reports implementation would go here

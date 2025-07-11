import streamlit as st
from utils.db import get_db_connection
import pandas as pd
from utils.ai_module import preprocess_solar_data, train_isolation_forest, detect_anomalies


def show_solar_analytics():
    st.subheader("Solar Generation Analytics")

    try:
        solar_data = pd.read_csv("utils/cleaned_solar_data_reduced.csv")
        X_scaled, scaler, processed_data = preprocess_solar_data(solar_data)
        model = train_isolation_forest(X_scaled)
        results = detect_anomalies(model, X_scaled, processed_data)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Generation Overview")
            st.line_chart(results.set_index('timestamp')['generation_kw'])

        with col2:
            st.markdown("### Anomaly Distribution")
            anomaly_count = results['is_anomaly'].value_counts()
            st.bar_chart(anomaly_count)

        with st.expander("Detailed Anomaly Report"):
            anomalies = results[results['is_anomaly'] == 1]
            st.dataframe(anomalies[['timestamp', 'generation_kw', 'hour', 'day_of_week']])

            if st.button("Export Anomaly Report"):
                csv = anomalies.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name='solar_anomalies.csv',
                    mime='text/csv'
                )

    except Exception as e:
        st.error(f"Error loading solar data: {str(e)}")


def get_dashboard_file(role):
    mapping = {
        "Admin": "pages/5_Admin.py",
        "Operations Manager": "pages/1_Operations_Manager.py",
        "Executive Director": "pages/2_Executive_Director.py",
        "Analyst": "pages/3_Analyst.py",
        "Technician": "pages/4_Technician.py"
    }
    return mapping.get(role, "pages/Home.py")

def show_navbar():
    role = st.session_state.get("current_role", "")

    pages = [{"label": "Dashboard", "target": get_dashboard_file(role)}]

    if role != "Analyst":
        pages.append({"label": "Tasks", "target": "pages/8_Tasks.py"})
    if role != "Technician":
        pages.append({"label": "Reports", "target": "pages/7_Reports.py"})

    pages.append({"label": "Alerts", "target": "pages/6_Alerts.py"})
    pages.append({"label": "Profile", "target": "pages/9_Profile.py"})
    pages.append({"label": "Logout", "target": "logout"})

    st.markdown('<div class="navbar">', unsafe_allow_html=True)

    cols = st.columns(len(pages))
    for i, p in enumerate(pages):
        with cols[i]:
            if st.button(p["label"], use_container_width=True):
                if p["target"] == "logout":
                    st.session_state.show_logout_modal = True
                else:
                    st.switch_page(p["target"])

    if st.session_state.get("show_logout_modal", False):
        st.markdown("""
            <div class="logout-modal">
                <h4>Are you sure you want to logout?</h4>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Yes, logout"):
                st.session_state.clear()
                st.switch_page("Home.py")
        with col2:
            if st.button("Cancel"):
                st.session_state.show_logout_modal = False

        st.markdown("</div>", unsafe_allow_html=True)


def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()
show_navbar()

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

show_solar_analytics()

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
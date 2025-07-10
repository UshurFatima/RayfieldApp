import streamlit as st
import pandas as pd
from utils.db import get_db_connection

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

st.set_page_config(page_title="Alerts", layout="wide")

# Auth check
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to view alerts")
    st.stop()

show_navbar()

st.title("🚨 Alerts Overview")
st.markdown("View and manage alert history across all systems.")
st.divider()

conn = get_db_connection()
alerts = pd.read_sql("SELECT * FROM alerts", conn)
conn.close()

# Show alerts in sections
severity_levels = ["High", "Medium", "Low"]
for level in severity_levels:
    st.subheader(f"{level}-Priority Alerts")

    filtered = alerts[alerts['severity'] == level]
    if filtered.empty:
        st.info(f"No {level.lower()} priority alerts")
        continue

    for _, row in filtered.iterrows():
        st.markdown(f"""
        <div class="metric-card">
            <p><strong>Asset:</strong> {row['asset_id']}</p>
            <p><strong>Status:</strong> {row['severity']}</p>
            <p><strong>Detected:</strong> {row['detected']}</p>
            <p><strong>Metric:</strong> {row['metric']}</p>
            <p><strong>Likely Cause:</strong> {row['likely_cause']}</p>
            <p><strong>Suggested Action:</strong> {row['suggested_action']}</p>
        </div>
        """, unsafe_allow_html=True)

        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button("Assign Task", key=f"assign_{row['id']}"):
                st.success(f"Task assigned for alert on asset {row['asset_id']}")
        with btn_cols[1]:
            if st.button("View Asset History", key=f"history_{row['id']}"):
                st.session_state.show_asset_history = True
                st.session_state.selected_asset = row['asset_id']

# Asset History Modal
if st.session_state.get("show_asset_history", False):
    st.markdown("### Asset History")
    asset_id = st.session_state.get("selected_asset", "")
    
    # Simulate asset history data
    st.markdown(f"""
    **Asset:** {asset_id}
    
    **Recent Alerts:**
    - 2025-06-15: High priority - Temperature threshold exceeded
    - 2025-06-10: Medium priority - Vibration levels elevated
    - 2025-06-05: Low priority - Maintenance due
    
    **Maintenance History:**
    - 2025-05-20: Scheduled maintenance completed
    - 2025-04-15: Emergency repair - Phase imbalance
    - 2025-03-10: Routine inspection
    
    **Performance Metrics:**
    - Uptime: 94.2%
    - Last inspection: 2025-06-01
    - Next scheduled maintenance: 2025-07-15
    """)
    
    if st.button("Close History"):
        st.session_state.show_asset_history = False

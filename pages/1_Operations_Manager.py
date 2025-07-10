import streamlit as st
from utils.db import get_db_connection
import pandas as pd


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
st.markdown("## Asset Overview")

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
    if st.button("VIEW ALERTS", use_container_width=True):
        st.switch_page("pages/6_Alerts.py")
with col2:
    if st.button("SCHEDULE MAINTENANCE", use_container_width=True):
        st.switch_page("pages/8_Tasks.py")

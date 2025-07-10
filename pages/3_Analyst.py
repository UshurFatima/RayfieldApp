import streamlit as st


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
    page_title="Analyst Dashboard",
    layout="wide"
)

# Authentication check
if 'current_role' not in st.session_state or st.session_state.current_role != "Analyst":
    st.error("You don't have permission to view this page")
    st.stop()

# Main Dashboard
st.title("Analyst")

# Dashboard Tabs
st.title("Analyst Dashboard")

st.subheader("AI-suggested Insight")
st.markdown("""
<div class="metric-card">
    <p>"12% deviation in Bearing Temp correlates with:</p>
    <ul>
        <li>Past failures (87% match)</li>
        <li>Weather patterns (73% correlation)</li>
    </ul>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Confirm"):
        st.success("Insight confirmed and added to knowledge base!")
with col2:
    if st.button("Decline"):
        st.warning("Insight declined and marked for review.")
with col3:
    if st.button("Compare Similar Cases"):
        st.info("Loading similar cases...")
        st.markdown("""
        **Similar Cases Found:**
        - Case #2024-045: Bearing failure at 12.3% deviation (2024-08-15)
        - Case #2024-032: Bearing failure at 11.8% deviation (2024-07-22)
        - Case #2024-018: Bearing failure at 12.1% deviation (2024-06-10)
        """)

st.markdown("## Active Models")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="metric-card">
        <p><strong>Vibration Analysis v3.2</strong></p>
        <p>Accuracy: 92%</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-card">
        <p><strong>Thermal Anomaly Detector v2.1</strong></p>
        <p>Accuracy: 88%</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Retrain Selected Model"):
        st.success("Model retraining initiated! Estimated completion: 2 hours")
with col2:
    if st.button("Deploy New Model"):
        st.success("New model deployment started! Will be active in 30 minutes")
with col3:
    if st.button("Model Performance Alerts"):
        st.info("Model Performance Alerts:")
        st.markdown("""
        - Vibration Analysis v3.2: Performance dropped 2% in last week
        - Thermal Anomaly Detector v2.1: 5 false positives detected
        """)

st.markdown("## Quick Analysis Types")
st.markdown("""
1. Cross-Asset Correlation  
2. Event Sequence Mining  
3. Maintenance Impact Study  
""")

st.markdown("## Recent Templates")
if st.button("Wind Speed vs. Gearbox Failures"):
    st.info("Loading Wind Speed vs. Gearbox Failures analysis...")
    st.markdown("""
    **Analysis Results:**
    - Correlation coefficient: 0.73
    - High wind speeds (>15 m/s) increase failure risk by 45%
    - Recommended: Increase inspection frequency during high wind periods
    """)

if st.button("Time-to-Repair by Technician"):
    st.info("Loading Time-to-Repair analysis...")
    st.markdown("""
    **Technician Performance:**
    - John Smith: Average repair time 2.3 hours
    - Sarah Johnson: Average repair time 1.8 hours
    - Mike Wilson: Average repair time 2.7 hours
    - Recommended: Assign Sarah to critical repairs
    """)

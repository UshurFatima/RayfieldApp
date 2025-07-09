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
    page_title="📋 Task Manager",
    layout="wide"
)

# Auth check
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to view this page")
    st.stop()

# Page Title
st.title("🗓️ Task Calendar")

# Calendar Header
st.markdown("#### June 2025 | June 16 – 22")
st.divider()

# Top-level Buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("Print Work Order", use_container_width=True)
with col2:
    st.file_uploader("Upload New", type=["pdf", "csv"], label_visibility="collapsed")
with col3:
    st.button("Notify Technician", use_container_width=True)
with col4:
    st.button("Cancel Task", use_container_width=True)

st.markdown("---")

# Task Card
st.subheader("Wind Turbine Inspection")
st.markdown("""
<div class="metric-card">
    <p><strong>Priority:</strong> High (4/5)</p>
    <p><strong>Due:</strong> 2025-06-20 14:30</p>
    <p><strong>Notes:</strong> Check phase imbalance – similar to 2025-04 incident</p>
    <p><strong>Attachments:</strong></p>
    <ul>
        <li>sensor_readings_023.csv</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Task Actions
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Start Task", use_container_width=True)
with col2:
    st.button("Add Notes", use_container_width=True)
with col3:
    st.button("View Details", use_container_width=True)


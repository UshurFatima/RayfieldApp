import streamlit as st


def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

st.set_page_config(
    page_title="Technician Dashboard",
    layout="wide"
)

# Authentication check
if 'current_role' not in st.session_state or st.session_state.current_role != "Technician":
    st.error("You don't have permission to view this page")
    st.stop()

# Main Dashboard
st.title("Technician")

# Priority Tasks
st.subheader("Priority Tasks")

# Task 1
with st.expander("❶ HIGH (Due: Today 14:30)", expanded=True):
    st.markdown("""
    <div class="metric-card">
        <p><strong>Turbine B7 - Gearbox Vibration (7.2mm/s)</strong></p>
        <p>1.2km from your location</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Task", key="task1_start"):
            st.success("Task started")
    with col2:
        if st.button("View Details", key="task1_details"):
            st.session_state.selected_task = 1

# Task 2
with st.expander("❷ CRITICAL (Due: Now)"):
    st.markdown("""
    <div class="metric-card alert-high">
        <p><strong>Substation Delta - Phase 2 Overheating (142°C)</strong></p>
        <p>800m from you</p>
        <p>Safety Protocol Required</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Task", key="task2_start"):
            st.success("Emergency task started")
    with col2:
        if st.button("View Details", key="task2_details"):
            st.session_state.selected_task = 2

# Task Details
if hasattr(st.session_state, 'selected_task'):
    st.markdown("---")
    st.subheader("Task Details")

    if st.session_state.selected_task == 1:
        st.markdown("""
        <div class="metric-card">
            <p><strong>Vibration:</strong> 7.2mm/s (Norm: 4.5mm/s)</p>
            <p><strong>Temp:</strong> 89°C (Norm: 65-75°C)</p>
            <p><strong>Power loss:</strong> 12% (Last 4h)</p>
            <p><strong>Likely Fault:</strong> Bearing wear (87% confidence)</p>
            <p><strong>Risk:</strong> High (15% chance of seizure in 48h)</p>
            <p><strong>Recommended Action:</strong> Inspect + lubricate</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Nearby Stock:**")
        st.markdown("- Gearbox Oil (3L): Warehouse A")
        st.markdown("- Bearings (Type 207): On van #5")
        st.markdown("- Gaskets: Out of stock (order 24h)")

# Personal Progress
st.markdown("---")
st.subheader("Personal Progress")
st.markdown("""
<div class="metric-card">
    <p><strong>Today's Completion:</strong> 4/6 tasks</p>
    <p><strong>Your Average:</strong> 1h22m (Team: 1h45m)</p>
    <p><strong>Rank:</strong> #3/14 technicians</p>
</div>
""", unsafe_allow_html=True)
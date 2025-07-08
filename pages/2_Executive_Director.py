import streamlit as st

def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.set_page_config(
    page_title="Executive Director Dashboard",
    layout="wide"
)

# Authentication check
if 'current_role' not in st.session_state or st.session_state.current_role != "Executive Director":
    st.error("You don't have permission to view this page")
    st.stop()

# Main Dashboard
st.title("Executive Director")

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
tab1, tab2 = st.tabs(["Dashboard", "Reports"])

with tab1:
    st.subheader("Maintenance Summary")
    st.markdown("""
    <div class="metric-card">
        <h3>WORK ORDERS</h3>
        <h1>135</h1>
        <p>78% completion rate</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("Reports")
    # Reports implementation would go here
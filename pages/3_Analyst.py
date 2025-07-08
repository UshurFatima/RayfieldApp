import streamlit as st
from utils.db import get_db_connection
import pandas as pd


def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

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
tab1, tab2, tab3 = st.tabs(["Dashboard", "Tasks", "Reports"])

with tab1:
    # AI Suggested Insight
    st.subheader("AI-suggested insight")
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
        st.button("Confirm", type="primary")
    with col2:
        st.button("Decline", type="secondary")
    with col3:
        st.button("Compare Similar Cases")

    # Active Models
    st.subheader("Active Models")
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
        st.button("Retrain Selected Model")
    with col2:
        st.button("Deploy New Model")
    with col3:
        st.button("Model Performance Alerts")

    # Quick Analysis
    st.subheader("Quick Analysis Types")
    st.markdown("""
    1. Cross-Asset Correlation  
    2. Event Sequence Mining  
    3. Maintenance Impact Study  
    """)

    # Recent Templates
    st.subheader("Recent Templates")
    st.button("Wind Speed vs. Gearbox Failures")
    st.button("Time-to-Repair by Technician")

with tab2:
    st.subheader("Task Management")
    # Task management implementation would go here

with tab3:
    st.subheader("Reports")
    # Reports implementation would go here
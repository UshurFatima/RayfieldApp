# main.py
import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from utils.auth import authenticate_user
from utils.db import init_db, get_db_connection, hash_password
import time
import os

# Initialize database
init_db()

# Configure page
st.set_page_config(
    page_title="Rayfield Systems",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Load custom CSS
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

# Session state management
if 'auth_redirect' not in st.session_state:
    st.session_state.auth_redirect = False
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'current_role' not in st.session_state:
    st.session_state.current_role = None

# Page mapping
PAGE_MAPPING = {
    "Admin": "5_Admin",
    "Operations Manager": "1_Operations_Manager",
    "Executive Director": "2_Executive_Director",
    "Analyst": "3_Analyst",
    "Technician": "4_Technician"
}

# Redirect logic
if st.session_state.get('authenticated'):
    target_page = f"pages/{PAGE_MAPPING[st.session_state.current_role]}.py"
    if os.path.exists(target_page):
        st.switch_page(target_page)
    else:
        st.error("System error: Dashboard not found")

# Login page
if not st.session_state.authenticated:
    st.title("Rayfield Systems")

    with st.form("login_form", clear_on_submit=True):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", list(PAGE_MAPPING.keys()))

        submitted = st.form_submit_button("Login")
        if submitted:
            if authenticate_user(email, password, role):
                st.session_state.authenticated = True
                st.session_state.current_user = email
                st.session_state.current_role = role
                st.session_state.auth_redirect = True
                time.sleep(0.3)
                st.rerun()
            else:
                st.error("Invalid credentials or role mismatch")

    st.markdown("---")
    st.caption("Our privacy policy")
    st.stop()

# Fallback navigation
with st.sidebar:
    # Add this to your CSS in main.py (replace the existing CSS)
    st.markdown("""
    <style>
        /* Base styles - applies to all pages */
        :root {
            --text-color: #333333;
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
        }

        /* Login page specific fixes */
        .stApp {
            background-color: #f5f7fa !important;
        }

        h1 {
            color: var(--primary-color) !important;
        }

        /* Hide all navigation elements */
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"],
        [data-testid="stHeader"],
        [data-testid="manage-app-button"],
        [data-testid="baseButton-header"] {
            display: none !important;
        }

        /* Form input labels */
        .stTextInput label,
        .stPassword label,
        .stSelectbox label {
            color: var(--text-color) !important;
            font-weight: 500 !important;
        }

        /* Remove Streamlit's default hamburger menu */
        .st-emotion-cache-6qob1r {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    if st.button("Logout", type="primary"):
        st.session_state.clear()
        st.rerun()

st.title(f"{st.session_state.current_role} Dashboard")
st.warning("Redirect failed - please use the sidebar navigation")
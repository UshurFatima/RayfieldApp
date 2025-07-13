import streamlit as st
import pandas as pd
from utils.db import get_db_connection, hash_password
import sqlite3


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
    page_title="Admin Dashboard",
    layout="wide"
)

# Authentication check
if 'current_role' not in st.session_state or st.session_state.current_role != "Admin":
    st.error("You don't have permission to view this page")
    st.stop()

# Main Dashboard
st.title("Admin Dashboard")

# User Management Section
st.header("User Management")

tab1, tab2 = st.tabs(["Add Users", "Manage Users"])

with tab1:
    with st.form("add_user_form", clear_on_submit=True):
        st.subheader("Add New User")
        new_email = st.text_input("Email")
        new_pass = st.text_input("Password", type="password")
        new_role = st.selectbox("Role", [
            "Admin",
            "Operations Manager",
            "Executive Director",
            "Analyst",
            "Technician"
        ])

        if st.form_submit_button("Create User"):
            conn = get_db_connection()
            try:
                hashed_pass = hash_password(new_pass)
                conn.execute(
                    "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                    (new_email, hashed_pass, new_role)
                )
                conn.commit()
                st.success(f"User {new_email} created successfully!")
            except sqlite3.IntegrityError:
                st.error("Email already exists")
            finally:
                conn.close()

with tab2:
    st.subheader("Current Users")
    conn = get_db_connection()
    users = pd.read_sql("SELECT email, role FROM users", conn)

    selected_emails = st.multiselect(
        "Select users to delete:",
        options=users["email"],
        format_func=lambda x: f"{x} ({users[users['email'] == x]['role'].values[0]})"
    )

    if st.button("Delete Selected", type="primary"):
        deleted_count = 0
        for email in selected_emails:
            conn.execute("DELETE FROM users WHERE email = ?", (email,))
            deleted_count += 1
        conn.commit()
        if deleted_count > 0:
            st.success(f"Deleted {deleted_count} user(s)")
            st.rerun()

    conn.close()


# System Configuration Section
st.header("⚙️ System Configuration")
with st.expander("Database Maintenance"):
    if st.button("Optimize Database"):
        with st.spinner("Optimizing..."):
            conn = get_db_connection()
            conn.execute("VACUUM")
            conn.close()
            st.success("Database optimized")

with st.expander("Backup/Restore"):
    st.warning("This feature is under development")
    st.file_uploader("Upload backup file")
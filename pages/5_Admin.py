import streamlit as st
import pandas as pd
from utils.db import get_db_connection, hash_password
import sqlite3


def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

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
st.header("👑 User Management")

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

    # Editable user table
    edited_users = st.data_editor(
        users,
        disabled=["email"],
        use_container_width=True
    )

    # Delete selected users
    if st.button("Delete Selected", type="primary"):
        deleted_count = 0
        for email in edited_users.loc[edited_users.index.difference(users.index), 'email']:
            conn.execute("DELETE FROM users WHERE email = ?", (email,))
            deleted_count += 1
        conn.commit()
        if deleted_count > 0:
            st.success(f"Deleted {deleted_count} users")
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
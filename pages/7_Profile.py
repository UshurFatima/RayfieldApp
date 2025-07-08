import streamlit as st
from utils.db import get_db_connection, hash_password


def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

st.set_page_config(
    page_title="User Profile",
    layout="wide"
)

# Add this additional CSS specifically for profile page
st.markdown("""
<style>
    .profile-container {
        color: var(--text-color) !important;
    }
    .profile-card {
        background-color: white;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Authentication check
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to view your profile")
    st.stop()

# Main Profile with fixed colors
st.markdown("<div class='profile-container'>", unsafe_allow_html=True)

st.title("👤 My Profile")

# User Info Card with proper colors
st.markdown(f"""
<div class="profile-card">
    <h3 style='color: var(--primary-color)'>Account Information</h3>
    <p><strong>Email:</strong> {st.session_state.current_user}</p>
    <p><strong>Role:</strong> {st.session_state.current_role}</p>
    <p><strong>Last Login:</strong> Just now</p>
</div>
""", unsafe_allow_html=True)

# Password Update Section
with st.container():
    st.markdown(f"""
    <div class="profile-card">
        <h3 style='color: var(--primary-color)'>Security Settings</h3>
    """, unsafe_allow_html=True)

    with st.form("password_form"):
        current_pass = st.text_input("Current Password", type="password")
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm New Password", type="password")

        if st.form_submit_button("Update Password"):
            conn = get_db_connection()
            user = pd.read_sql(
                "SELECT password FROM users WHERE email = ?",
                conn,
                params=(st.session_state.current_user,)
            ).iloc[0]

            if hash_password(current_pass) == user['password']:
                if new_pass == confirm_pass:
                    conn.execute(
                        "UPDATE users SET password = ? WHERE email = ?",
                        (hash_password(new_pass), st.session_state.current_user)
                    )
                    conn.commit()
                    st.success("Password updated successfully")
                else:
                    st.error("New passwords don't match")
            else:
                st.error("Current password is incorrect")
            conn.close()

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # Close profile-container
# ===============================================================
#  NetDoc AI — Streamlit Frontend Router (Main App)
# ===============================================================

import streamlit as st

# Internal imports
from auth_engine import login_user, signup_user, logout, current_user
from admin_engine import admin_page
from database import init_db

# External pages
from app_pages.dashboard import dashboard_page
from app_pages.upload_and_audit import upload_and_audit_page
from app_pages.topology_page import topology_page

# Top navigation bar component
from components.top_nav import top_nav


# ---------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(
    page_title="NetDoc AI",
    page_icon="⚡",
    layout="wide",
)


# ---------------------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------------------
def load_css():
    try:
        with open("static/global.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass


load_css()


# ---------------------------------------------------------------
# INIT DATABASE
# ---------------------------------------------------------------
init_db()


# ---------------------------------------------------------------
# SESSION DEFAULTS
# ---------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False


# ---------------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------------
def render_sidebar():
    st.markdown("""
        <style>
        .sidebar-icon { font-size: 1.2rem; margin-right: 8px; }
        .sidebar-btn {
            background-color: #2a2d35;
            padding: 0.6rem 1rem;
            border-radius: 10px;
            margin-bottom: 8px;
            transition: 0.2s ease;
            font-weight: 600;
            display: flex;
            align-items: center;
            border: 1px solid #3d414c;
            color: white;
        }
        .sidebar-btn:hover {
            background-color: #5c6bc0;
            border-color: #5c6bc0;
            color: white !important;
            transform: translateX(4px);
            cursor: pointer;
        }
        .active {
            background-color: #5360d9 !important;
            color: white !important;
            border-color: #5360d9;
        }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("## 🔧 Navigation")

    def nav_button(page, label, icon):
        css = "sidebar-btn"
        if st.session_state.page == page:
            css += " active"

        if st.sidebar.button(f"{icon}  {label}", key=page):
            st.session_state.page = page
            st.rerun()

    nav_button("dashboard", "Dashboard", "🏠")
    nav_button("audit", "Upload & Audit", "📤")
    nav_button("topology", "Topology Map", "🌐")

    if st.session_state.get("is_admin"):
        nav_button("admin", "Admin Panel", "🛠")

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 Logout"):
        logout()
        st.session_state.page = "login"
        st.rerun()


# ---------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------
def goto(page_name: str):
    st.session_state.page = page_name
    st.rerun()


# ---------------------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------------------
def login_page():
    st.title("🔐 NetDoc AI — Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        ok, msg, is_admin = login_user(email, password)
        st.info(msg)

        if ok:
            st.session_state.is_admin = is_admin
            st.session_state.page = "dashboard"
            st.rerun()

    if st.button("Create Account"):
        goto("signup")


# ---------------------------------------------------------------
# SIGNUP PAGE
# ---------------------------------------------------------------
def signup_page():
    st.title("📝 Create an Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        ok, msg = signup_user(email, password)
        st.info(msg)
        if ok:
            goto("login")

    if st.button("Back to Login"):
        goto("login")


# ---------------------------------------------------------------
# PROTECTED ROUTES
# ---------------------------------------------------------------
protected_pages = ["dashboard", "audit", "topology", "admin"]

page = st.session_state.page

user = current_user()

# Show sidebar + top nav on logged-in pages
if page in protected_pages and user:
    render_sidebar()
    top_nav(user.email)  # global nav bar


# ---------------------------------------------------------------
# ROUTING
# ---------------------------------------------------------------
if page == "login":
    login_page()

elif page == "signup":
    signup_page()

elif page == "dashboard":
    dashboard_page()

elif page == "audit":
    upload_and_audit_page()

elif page == "topology":
    topology_page()

elif page == "admin":
    admin_page()

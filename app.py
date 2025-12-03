# ===============================================================
#  NetDoc AI — Streamlit Frontend Router (Main App)
# ===============================================================

import streamlit as st

# Internal imports
from auth_engine import login_user, signup_user, logout, current_user
from admin_engine import admin_page
from database import init_db

# External page modules
from app_pages.dashboard import dashboard_page
from app_pages.audit_page import audit_page
from app_pages.topology_page import topology_page


# ---------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(
    page_title="NetDoc AI",
    page_icon="⚡",
    layout="wide",
)


# ---------------------------------------------------------------
# LOAD GLOBAL CSS
# ---------------------------------------------------------------
def load_css():
    try:
        with open("static/global.css", "r") as f:
            css = f"<style>{f.read()}</style>"
            st.markdown(css, unsafe_allow_html=True)
    except:
        pass


load_css()

# ---------------------------------------------------------------
# TOP NAV BAR (Global)
# ---------------------------------------------------------------
def top_nav():
    st.markdown(
        """
        <div class="navbar">
            <div class="nav-title">NetDoc AI</div>
            <img src="https://i.imgur.com/Spd0bQx.png" class="nav-avatar">
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------------
# INIT DATABASE
# ---------------------------------------------------------------
init_db()


# ---------------------------------------------------------------
# SESSION STATE DEFAULTS
# ---------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False


# ---------------------------------------------------------------
# MODERN SIDEBAR (Step 2)
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

    # ---- Internal function for nav buttons ----
    def nav_button(page, label, icon):
        css = "sidebar-btn"
        if st.session_state.page == page:
            css += " active"

        if st.sidebar.button(f"{icon}  {label}", key=page):
            st.session_state.page = page
            st.rerun()

    # ---- Buttons ----
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
# UTIL: Go to page
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


top_nav()

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
# ROUTER — PROTECTED PAGES
# ---------------------------------------------------------------
protected_pages = ["dashboard", "audit", "topology", "admin"]

# Show sidebar only on logged-in pages
if st.session_state.page in protected_pages:
    render_sidebar()
from components.top_nav import top_nav

user = current_user()
if user:
    top_nav(user.email)



# ---------------- ROUTES ----------------
page = st.session_state.page

if page == "login":
    login_page()

elif page == "signup":
    signup_page()

elif page == "dashboard":
    dashboard_page()

elif page == "audit":
    audit_page()

elif page == "topology":
    topology_page()

elif page == "admin":
    admin_page()

# ===============================================================
#  NetDoc AI — Dashboard Page
# ===============================================================

import streamlit as st
from auth_engine import current_user, logout
from database import SessionLocal, Upload, AuditReport, SNMPDevice

# ---------------------------------------------------------------
# NAVBAR HTML (f-string only)
# ---------------------------------------------------------------

def render_navbar(user_email: str):
    avatar_char = user_email[0].upper()

    navbar_html = f"""
    <div class="top-nav">
        <div class="top-left">
            <img src="https://raw.githubusercontent.com/lokauday/netdoc-ai/main/logo.png" class="netdoc-logo">
            <span class="app-title">NetDoc AI</span>
        </div>

        <div class="top-right">
            <span class="bell">🔔</span>
            <div class="avatar">{avatar_char}</div>
        </div>
    </div>
    """

    st.markdown(navbar_html, unsafe_allow_html=True)


# ---------------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------------

def render_sidebar():
    st.sidebar.markdown("## 📌 Navigation")

    if st.sidebar.button("📊 Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    if st.sidebar.button("📁 Upload & Audit"):
        st.session_state.page = "audit"
        st.rerun()

    if st.sidebar.button("🗺 Topology Map"):
        st.session_state.page = "topology"
        st.rerun()

    if st.session_state.get("is_admin", False):
        if st.sidebar.button("🔐 Admin Panel"):
            st.session_state.page = "admin"
            st.rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        logout()
        st.session_state.page = "login"
        st.rerun()


# ---------------------------------------------------------------
# MAIN DASHBOARD
# ---------------------------------------------------------------

def dashboard_page():
    user = current_user()
    if not user:
        st.session_state.page = "login"
        st.rerun()

    # Render Layout
    render_sidebar()
    render_navbar(user.email)

    st.markdown("## 📊 Dashboard")

    # -----------------------------------------------------------
    # Database Counts
    # -----------------------------------------------------------
    db = SessionLocal()
    files_uploaded = db.query(Upload).count()
    audits_run = db.query(AuditReport).count()
    snmp_devices = db.query(SNMPDevice).count()
    db.close()

    # -----------------------------------------------------------
    # Summary Cards
    -----------------------------------------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Files Uploaded", files_uploaded)
    col2.metric("Audits Run", audits_run)
    col3.metric("SNMP Devices", snmp_devices)

    st.markdown("### 🕒 Recent Activity")
    st.info("No recent audits yet. Upload a config file on the **Audit page** to get started.")

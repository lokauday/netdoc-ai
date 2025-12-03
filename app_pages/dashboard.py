# app_pages/dashboard.py
# ===============================================================
#  NetDoc AI — Dashboard Page
# ===============================================================

import streamlit as st
from auth_engine import current_user
from database import SessionLocal, User, Upload, AuditReport
from components.top_navbar import NAVBAR_HTML


def dashboard_page():
    # -----------------------------
    # Auth Guard
    # -----------------------------
    user = current_user()
    if not user:
        # If user is not logged in, send them back to main app router
        st.switch_page("app.py")

    # -----------------------------
    # Top Navbar (HTML, not code)
    # -----------------------------
    st.markdown(NAVBAR_HTML, unsafe_allow_html=True)

    # Small spacing under navbar
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # -----------------------------
    # Load basic stats from DB
    # -----------------------------
    db = SessionLocal()
    total_users = db.query(User).count()
    total_uploads = db.query(Upload).count()
    total_audits = db.query(AuditReport).count()
    db.close()

    # -----------------------------
    # Header
    # -----------------------------
    st.title("📊 Dashboard Overview")

    st.markdown(
        f"""
        <div style="margin-bottom: 1rem; font-size: 0.95rem; color:#cfd3dc;">
            <strong>NetDoc AI</strong><br>
            {user.email}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # Metric Cards Row
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Users", total_users)

    with col2:
        st.metric("Files Uploaded", total_uploads)

    with col3:
        st.metric("Audits Run", total_audits)

    st.markdown("---")

    # -----------------------------
    # Recent Activity placeholder
    # -----------------------------
    st.subheader("Recent Activity")
    if total_audits == 0 and total_uploads == 0:
        st.write("No recent activity yet. Upload a config on the **Upload & Audit** page to get started.")
    else:
        st.write("Activity feed coming soon…")

# =====================================================================
#  NetDoc AI — Dashboard Page (Clean + No Syntax Errors)
# =====================================================================

import streamlit as st
from auth_engine import current_user
from database import SessionLocal, User, Upload, AuditReport, SNMPDevice


# ---------------------------------------------------------------
# TOP NAVBAR HTML (Safe triple quotes)
# ---------------------------------------------------------------
NAVBAR_HTML = """
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


# ---------------------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------------------
def dashboard_page():

    user = current_user()
    if not user:
        st.error("You must log in first.")
        st.stop()

    # ------------------ SAFE AVATAR ------------------
    email = user.email or ""                    # handle None or empty string
    avatar = email[0].upper() if email else "U" # fallback "U" if no email

    # ------------------ NAVBAR ------------------
    st.markdown(
        NAVBAR_HTML.format(avatar_char=avatar),
        unsafe_allow_html=True
    )

    st.write("")  # small spacing

    st.title("📊 Dashboard")

    # ------------------ DATABASE COUNTS ------------------
    db = SessionLocal()
    total_users = db.query(User).count()
    total_uploads = db.query(Upload).count()
    total_audits = db.query(AuditReport).count()
    total_snmp = db.query(SNMPDevice).count()
    db.close()

    # ------------------ METRIC CARDS ------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Users", total_users)
    col2.metric("Files Uploaded", total_uploads)
    col3.metric("Audits Run", total_audits)
    col4.metric("SNMP Devices", total_snmp)

    st.write("## 📌 Recent Activity")

    if total_audits == 0:
        st.info("No audits yet — upload a config file to get started.")
    else:
        st.success("Showing latest audit entries (Coming soon!)")

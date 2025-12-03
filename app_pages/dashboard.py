# ===============================================================
#  NetDoc AI — Dashboard Page (Premium UI)
# ===============================================================

import streamlit as st
from auth_engine import current_user, logout
from database import SessionLocal, SNMPDevice, SNMPPoll, AuditReport


# ---------------------------------------------------------------
# TOP NAV BAR (Global)
# ---------------------------------------------------------------
def top_nav():
    user_email = st.session_state.get("email", "user@example.com")
    avatar_letter = user_email[0].upper() if user_email else "N"

    st.markdown(
        f"""
        <div class="navbar">
            <div class="nav-title">NetDoc AI</div>
            <div style="display:flex;align-items:center;gap:12px;">
                <span style="font-size:13px;opacity:0.8;">{user_email}</span>
                <div class="nav-avatar" style="
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:#11131a;
                    font-weight:bold;
                    color:#4a90e2;">
                    {avatar_letter}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------
# SIDEBAR NAVIGATION  (FIXED WITH UNIQUE BUTTON KEYS)
# ---------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.markdown("### ⚡ NetDoc AI")
        st.markdown("---")

        if st.button("🏠 Dashboard", key="sidebar_dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

        if st.button("📝 Audit Config", key="sidebar_audit"):
            st.session_state.page = "audit"
            st.rerun()

        if st.button("🌐 Topology Map", key="sidebar_topology"):
            st.session_state.page = "topology"
            st.rerun()

        # Future SNMP page
        if st.button("📡 SNMP Devices", key="sidebar_snmp"):
            st.session_state.page = "snmp"
            st.rerun()

        if st.session_state.get("is_admin"):
            if st.button("🛠 Admin Panel", key="sidebar_admin"):
                st.session_state.page = "admin"
                st.rerun()

        if st.button("🚪 Logout", key="sidebar_logout"):
            logout()
            st.session_state.page = "login"
            st.rerun()


# ---------------------------------------------------------------
# DASHBOARD DATA HELPERS
# ---------------------------------------------------------------
def get_dashboard_stats():
    db = SessionLocal()
    try:
        audits_count = db.query(AuditReport).count()
        devices_count = db.query(SNMPDevice).count()
        alerts_count = 0  # placeholder for future SNMP alerts table
    finally:
        db.close()
    return audits_count, devices_count, alerts_count


def get_recent_audits(limit: int = 5):
    db = SessionLocal()
    try:
        audits = (
            db.query(AuditReport)
            .order_by(AuditReport.created_at.desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()
    return audits


# ---------------------------------------------------------------
# MAIN DASHBOARD PAGE
# ---------------------------------------------------------------
def dashboard_page():
    # Auth guard
    user = current_user()
    if not user:
        st.session_state.page = "login"
        st.rerun()

    # Layout chrome
    top_nav()
    render_sidebar()

    st.title("📊 Dashboard")

    # Metric cards
    audits_count, devices_count, alerts_count = get_dashboard_stats()

    st.markdown("### Network Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Audits Run</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(audits_count),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">SNMP Devices</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(devices_count),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Active Alerts</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(alerts_count),
            unsafe_allow_html=True,
        )

    # Recent activity block
    st.markdown("### Recent Activity")

    audits = get_recent_audits()

    if not audits:
        st.markdown(
            '<div class="card">No recent audits yet. Upload a config on the Audit page to get started.</div>',
            unsafe_allow_html=True,
        )
    else:
        for a in audits:
            st.markdown(
                f"""
                <div class="card">
                    <div><strong>Audit ID:</strong> {a.id}</div>
                    <div><strong>Organization:</strong> {a.organization.org_name if a.organization else 'N/A'}</div>
                    <div><strong>Created:</strong> {a.created_at}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

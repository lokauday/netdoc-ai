# ================================
# /app/app_pages/dashboard.py
# ================================

import streamlit as st
from announcement_engine import list_announcements
from auth_engine import current_user
from components.top_navbar import NAVBAR_HTML


def dashboard_page():
    # Require login
    user = current_user()
    if not user:
        st.switch_page("app.py")

    # Announcements
    anns = list_announcements() or []
    unread = len(anns)

    # ----------------------------
    # Safe avatar initial
    # ----------------------------
    email = getattr(user, "email", "") or ""
    full_name = getattr(user, "full_name", "") or getattr(user, "name", "") or ""

    avatar_char = "U"  # default fallback

    if email.strip():
        avatar_char = email.strip()[0].upper()
    elif full_name.strip():
        avatar_char = full_name.strip()[0].upper()

    # ----------------------------
    # Top Navbar (component)
    # ----------------------------
    st.markdown(
        NAVBAR_HTML.format(
            unread=unread,
            avatar=avatar_char,
        ),
        unsafe_allow_html=True,
    )

    # ===== MAIN DASHBOARD BODY =====
    st.title("Welcome back 👋")
    st.caption("Here’s your NetDoc AI overview.")

    # Metric row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Unread Announcements", unread, delta=None)
    with col2:
        st.metric("Configs Processed", 42, delta="+3 today")
    with col3:
        st.metric("Devices Monitored", 18, delta="+1 this week")

    st.markdown("---")

    # Layout: left content + right sidebar
    left, right = st.columns([2.5, 1.5])

    # ----------------------------
    # LEFT: Announcements + Actions
    # ----------------------------
    with left:
        st.subheader("📢 Announcements")
        if anns:
            for ann in anns:
                st.markdown(
                    f"""
                    <div style="
                        padding: 12px 14px;
                        margin-bottom: 8px;
                        border-radius: 8px;
                        background: #1f2125;
                        border: 1px solid #2b2e36;
                    ">
                        <div style="font-weight:600;margin-bottom:4px;">{ann.title}</div>
                        <div style="font-size:0.9rem;color:#d1d5db;">{ann.body}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No announcements yet. You’re all caught up ✅")

        st.markdown("---")
        st.subheader("🚀 Quick Actions")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("➕ Upload Config"):
                st.session_state["nav_action"] = "upload_config"
        with col_b:
            if st.button("🛡 Run Security Audit"):
                st.session_state["nav_action"] = "security_audit"
        with col_c:
            if st.button("🌐 View Topology"):
                st.session_state["nav_action"] = "view_topology"

    # ----------------------------
    # RIGHT: Account + Tips
    # ----------------------------
    with right:
        st.subheader("👤 Account")
        st.markdown(f"**Email:** {email or 'N/A'}")
        st.markdown(f"**Role:** {getattr(user, 'role', 'Member')}")
        st.markdown(f"**Organization:** {getattr(user, 'organization_name', 'N/A')}")

        st.markdown("---")
        st.subheader("⚡ Tips")
        st.markdown(
            """
            - Use the **Upload Config** action to add new devices.
            - Run a **Security Audit** after each change window.
            - Check **Topology** to validate design before rollout.
            """
        )

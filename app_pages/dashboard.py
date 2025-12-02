import streamlit as st
from announcement_engine import list_announcements
from auth_engine import current_user
from database import SessionLocal, SNMPDevice, SNMPPoll
import pandas as pd
import plotly.express as px


def dashboard_page():

    user = current_user()
    if not user:
        st.switch_page("app.py")

    anns = list_announcements()
    unread = len(anns)

    # ----------------------------------
    # TOP NAV BAR
    # ----------------------------------
    st.markdown(f"""
    <div class="top-nav">
        <div class="top-left">
            <img src="/app/static/logo.png" class="netdoc-logo">
            <span class="app-title">NetDoc AI Dashboard</span>
        </div>
        <div class="top-right">
            <div class="bell">🔔</div>
            <div class="badge">{unread}</div>
            <div class="avatar">{user.email[0].upper()}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------------
    # ANNOUNCEMENT DRAWER
    # ----------------------------------
    with st.expander(f"📢 Announcements ({unread})"):
        for ann in anns:
            st.markdown(
                f"""
                <div style="padding:15px;background:#1f2125;border-left:4px solid #3ea6ff;margin-bottom:10px;border-radius:8px;">
                    <strong style="color:#3ea6ff;">{ann.title}</strong>
                    <p>{ann.message}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.subheader("📊 Network Overview")
    st.write("Your main dashboard metrics will appear here soon.")

    # ----------------------------------
    # CALL SNMP UI SECTION
    # ----------------------------------
    dashboard_snmp_ui()



# =====================================================
# SNMP DEVICE HEALTH UI
# =====================================================
def dashboard_snmp_ui():

    st.subheader("📡 SNMP Device Health")

    # Load devices
    db = SessionLocal()
    devices = db.query(SNMPDevice).all()
    db.close()

    if not devices:
        st.info("No SNMP devices added yet.")
        return

    device_names = {d.name: d.id for d in devices}
    selected = st.selectbox("Select Device", list(device_names.keys()))

    dev_id = device_names[selected]

    # Load polling history
    db = SessionLocal()
    polls = (
        db.query(SNMPPoll)
        .filter(SNMPPoll.device_id == dev_id)
        .order_by(SNMPPoll.timestamp)
        .all()
    )
    db.close()

    if not polls:
        st.warning("No polling data available yet.")
        return

    # Build DataFrame
    df = pd.DataFrame([
        {
            "timestamp": p.timestamp,
            "cpu": p.cpu,
            "memory": p.memory,
            "in": p.in_octets,
            "out": p.out_octets
        }
        for p in polls
    ])

    # Charts
    st.plotly_chart(
        px.line(df, x="timestamp", y="cpu", title="CPU Usage (%)"),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(df, x="timestamp", y="memory", title="Memory Usage (%)"),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(df, x="timestamp", y="in", title="Inbound Traffic (Octets)"),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(df, x="timestamp", y="out", title="Outbound Traffic (Octets)"),
        use_container_width=True
    )

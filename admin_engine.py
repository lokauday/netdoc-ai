# ===============================================================
#  NetDoc AI — Admin Panel
# ===============================================================

import streamlit as st
from auth_engine import require_admin
from announcement_engine import (
    create_announcement,
    list_announcements,
    delete_announcement,
)

# SNMP UI imports
from database import SNMPDevice, SessionLocal


# ===============================================================
#  SNMP DEVICE MANAGEMENT UI
# ===============================================================
def admin_snmp_ui():
    st.subheader("🌐 SNMP Device Manager")

    name = st.text_input("Device Name")
    ip = st.text_input("IP Address")
    community = st.text_input("Community String", type="password")
    location = st.text_input("Location")
    desc = st.text_area("Description")

    if st.button("Add SNMP Device"):
        if not (name.strip() and ip.strip() and community.strip()):
            st.error("Name, IP, and Community String are required.")
        else:
            db = SessionLocal()
            dev = SNMPDevice(
                name=name,
                ip_address=ip,
                community=community,
                location=location,
                description=desc
            )
            db.add(dev)
            db.commit()
            db.close()
            st.success("Device added successfully!")
            st.experimental_rerun()

    st.markdown("---")
    st.subheader("📋 Current SNMP Devices")

    db = SessionLocal()
    devices = db.query(SNMPDevice).all()
    db.close()

    if not devices:
        st.info("No SNMP devices added yet.")
    else:
        for d in devices:
            st.markdown(f"""
            **{d.name}**  
            🌐 {d.ip_address}  
            📍 {d.location or '—'}  
            📝 {d.description or '—'}  
            ---
            """)


# ===============================================================
#  ADMIN PAGE
# ===============================================================
def admin_page():
    require_admin()

    st.title("🛠 Admin Control Center")
    st.markdown("Manage announcements, users, SNMP devices, and system settings.")

    # -----------------------------------------------------------
    # ANNOUNCEMENT SECTION
    # -----------------------------------------------------------
    st.subheader("📢 Create Announcement")

    title = st.text_input("Title")
    msg = st.text_area("Message", height=140)

    if st.button("Send Announcement"):
        if title.strip() and msg.strip():
            create_announcement(title, msg)
            st.success("📢 Announcement sent!")
            st.experimental_rerun()
        else:
            st.error("Please enter a title and message.")

    st.markdown("---")
    st.subheader("📜 Announcement History (Newest First)")

    anns = list_announcements()

    for ann in anns:
        with st.container():
            st.markdown(
                f"""
                <div style="padding:15px;background:#212329;border:1px solid #3ea6ff;border-radius:10px;margin-bottom:10px;">
                    <h4 style="color:#3ea6ff;">{ann.title}</h4>
                    <p>{ann.message}</p>
                    <small style="opacity:0.7;">{ann.created_at}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(f"Delete {ann.id}"):
                delete_announcement(ann.id)
                st.experimental_rerun()

    st.markdown("---")

    # -----------------------------------------------------------
    # SNMP DEVICE MANAGEMENT SECTION
    # -----------------------------------------------------------
    admin_snmp_ui()

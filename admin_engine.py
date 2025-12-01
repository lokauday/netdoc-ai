import streamlit as st
from database import SessionLocal, User, Organization, Upload, AuditReport
from sqlalchemy import func

# ===============================================================
#  PROFESSIONAL ADMIN PANEL
# ===============================================================

def admin_page():

    # Check admin privileges
    from auth_engine import current_user
    user = current_user()

    if not user or user.is_admin != 1:
        st.error("❌ Access denied — Admins only.")
        return

    st.title("🛠 Admin Control Panel")

    st.markdown("""
        <style>
            .admin-card {
                background: #2a2d35;
                padding: 18px;
                border-radius: 14px;
                border: 1px solid #3c404a;
                text-align: left;
                margin-bottom: 20px;
                transition: 0.2s ease;
            }
            .admin-card:hover {
                background: #363a45;
                transform: translateY(-3px);
            }
            .admin-title {
                font-size: 14px;
                opacity: 0.8;
            }
            .admin-value {
                font-size: 26px;
                font-weight: 700;
                margin-top: 8px;
            }
            .table-box {
                background: #23262d;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #333740;
            }
        </style>
    """, unsafe_allow_html=True)

    db = SessionLocal()

    # ===============================================================
    #  ADMIN STATS
    # ===============================================================
    st.markdown("## 📊 Platform Overview")

    total_users = db.query(func.count(User.id)).scalar()
    total_orgs = db.query(func.count(Organization.id)).scalar()
    total_uploads = db.query(func.count(Upload.id)).scalar()
    total_audits = db.query(func.count(AuditReport.id)).scalar()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="admin-card">
                <div class="admin-title">Total Users</div>
                <div class="admin-value">{total_users}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="admin-card">
                <div class="admin-title">Organizations</div>
                <div class="admin-value">{total_orgs}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="admin-card">
                <div class="admin-title">Files Uploaded</div>
                <div class="admin-value">{total_uploads}</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="admin-card">
                <div class="admin-title">Security Audits</div>
                <div class="admin-value">{total_audits}</div>
            </div>
        """, unsafe_allow_html=True)

    # ===============================================================
    #  USER MANAGEMENT TABLE
    # ===============================================================
    st.markdown("## 👥 User Management")

    users = db.query(User).all()

    st.markdown("<div class='table-box'>", unsafe_allow_html=True)

    # Table header
    st.markdown("### Users List")

    user_emails = [u.email for u in users]
    selected_user = st.selectbox("Select User", user_emails)

    user_obj = next((u for u in users if u.email == selected_user), None)

    if user_obj:
        st.write("### User Details")
        st.write(f"**Email:** {user_obj.email}")
        st.write(f"**Org ID:** {user_obj.org_id}")
        st.write(f"**Admin:** {'Yes' if user_obj.is_admin else 'No'}")
        st.write(f"**Created:** {user_obj.created_at}")

        # Toggle Admin
        make_admin = st.checkbox("Grant Admin Access", value=user_obj.is_admin == 1)

        if st.button("Update Role"):
            user_obj.is_admin = 1 if make_admin else 0
            db.commit()
            st.success("User role updated!")
            st.rerun()

        # Delete user
        if st.button("Delete User ❌"):
            db.delete(user_obj)
            db.commit()
            st.warning("User deleted!")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ===============================================================
    #  RECENT ACTIVITY LOG
    # ===============================================================
    st.markdown("## 🕒 Recent Uploads")

    recent_uploads = (
        db.query(Upload)
        .order_by(Upload.created_at.desc())
        .limit(10)
        .all()
    )

    if recent_uploads:
        for u in recent_uploads:
            st.info(f"📄 {u.filename} — User {u.user_id} — {u.created_at}")
    else:
        st.write("No uploads found.")

    db.close()


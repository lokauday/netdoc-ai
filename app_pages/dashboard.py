import streamlit as st
from database import SessionLocal, User, Upload, AuditReport
from sqlalchemy import func

# ===============================================================
#   PROFESSIONAL DASHBOARD — NetDoc AI
# ===============================================================

def dashboard_page():
    st.markdown("""
        <style>
            .metric-card {
                background: #2c2f36;
                padding: 18px;
                border-radius: 14px;
                border: 1px solid #3b3e45;
                width: 100%;
                text-align: left;
                transition: 0.2s ease;
            }
            .metric-card:hover {
                background: #373b44;
                transform: translateY(-3px);
            }
            .metric-title {
                font-size: 14px;
                opacity: 0.8;
            }
            .metric-value {
                font-size: 26px;
                font-weight: 700;
                margin-top: 8px;
            }
            .section-title {
                font-size: 20px;
                font-weight: bold;
                margin-top: 30px;
                margin-bottom: 10px;
            }
            .activity-box {
                background: #23262d;
                padding: 14px;
                border-radius: 12px;
                border: 1px solid #343840;
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("📊 Dashboard Overview")

    db = SessionLocal()

    # --------------------------------
    # STATISTICS
    # --------------------------------
    total_users = db.query(func.count(User.id)).scalar()
    total_uploads = db.query(func.count(Upload.id)).scalar()
    total_audits = db.query(func.count(AuditReport.id)).scalar()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Users</div>
                <div class="metric-value">{total_users}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Files Uploaded</div>
                <div class="metric-value">{total_uploads}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Audits Run</div>
                <div class="metric-value">{total_audits}</div>
            </div>
        """, unsafe_allow_html=True)

    # --------------------------------
    # RECENT ACTIVITY
    # --------------------------------
    st.markdown('<div class="section-title">🕒 Recent Activity</div>', unsafe_allow_html=True)

    recent_uploads = (
        db.query(Upload)
        .order_by(Upload.created_at.desc())
        .limit(5)
        .all()
    )

    if not recent_uploads:
        st.info("No recent uploads found.")
    else:
        for u in recent_uploads:
            st.markdown(f"""
                <div class="activity-box">
                    <strong>📄 {u.filename}</strong><br>
                    <span style='opacity:0.7'>Uploaded by User ID {u.user_id}</span><br>
                    <span style='font-size:12px; opacity:0.6'>{u.created_at}</span>
                </div>
            """, unsafe_allow_html=True)

    # --------------------------------
    # RECENT AUDITS
    # --------------------------------
    st.markdown('<div class="section-title">🛡 Security Audits</div>', unsafe_allow_html=True)

    recent_audits = (
        db.query(AuditReport)
        .order_by(AuditReport.created_at.desc())
        .limit(5)
        .all()
    )

    if not recent_audits:
        st.info("No audits run yet.")
    else:
        for a in recent_audits:
            st.markdown(f"""
                <div class="activity-box">
                    <strong>🛡 Audit Report #{a.id}</strong><br>
                    <span style='opacity:0.7'>Run by User ID {a.user_id}</span><br>
                    <span style='font-size:12px; opacity:0.6'>{a.created_at}</span>
                </div>
            """, unsafe_allow_html=True)

    db.close()


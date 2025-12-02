from database import SessionLocal, Announcement
from auth_engine import current_user

def get_unread_count():
    db = SessionLocal()
    count = db.query(Announcement).count()
    db.close()
    return count


def get_navbar_html():
    unread = get_unread_count()

    bell_html = f"""
        <span class="bell">
            🔔<span class="badge">{unread}</span>
        </span>
    """

    return f"""
    <style>
    .badge {{
        background: red;
        color: white;
        padding: 2px 6px;
        border-radius: 50%;
        font-size: 12px;
        margin-left: 3px;
    }}
    </style>

    <div class="top-nav">
        <div class="top-left">
            <img src="https://raw.githubusercontent.com/lokauday/netdoc-ai/main/logo.png" class="netdoc-logo">
            <span class="app-title">NetDoc AI</span>
        </div>

        <div class="top-right">
            {bell_html}
            <div class="avatar">T</div>
        </div>
    </div>
    """

# ================================
# /app/components/top_navbar.py
# ================================

NAVBAR_HTML = """
<style>
.top-nav {
    position: sticky;
    top: 0;
    z-index: 999;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    background: #101218;
    border-bottom: 1px solid #2b2e36;
    margin-bottom: 1rem;
}

.top-left {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.netdoc-logo {
    width: 32px;
    height: 32px;
    border-radius: 8px;
}

.app-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #f9fafb;
}

.top-right {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.bell {
    font-size: 1.2rem;
}

.badge {
    min-width: 22px;
    height: 22px;
    border-radius: 999px;
    background: #3ea6ff;
    color: #020617;
    font-size: 0.75rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 0.4rem;
}

.avatar {
    width: 32px;
    height: 32px;
    border-radius: 999px;
    background: #1f2933;
    border: 1px solid #3b4252;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #e5e7eb;
    font-weight: 600;
    font-size: 0.9rem;
}
</style>

<div class="top-nav">
    <div class="top-left">
        <img src="/app/static/logo.png" class="netdoc-logo">
        <span class="app-title">NetDoc AI Dashboard</span>
    </div>
    <div class="top-right">
        <div class="bell">🔔</div>
        <div class="badge">{unread}</div>
        <div class="avatar">{avatar}</div>
    </div>
</div>
"""

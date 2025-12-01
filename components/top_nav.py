import streamlit as st
import base64

def top_nav(user_email: str):

    st.markdown("""
    <style>
        /* Wrapper */
        .top-nav {
            background: rgba(32, 35, 42, 0.6);
            padding: 12px 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid #2f323a;
            backdrop-filter: blur(6px);
        }

        .top-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .netdoc-logo {
            height: 36px;
        }

        .app-title {
            font-size: 20px;
            font-weight: 700;
            color: white;
        }

        .top-right {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .bell {
            font-size: 22px;
            cursor: pointer;
            padding: 6px 10px;
            border-radius: 8px;
            transition: 0.2s ease;
        }

        .bell:hover {
            background: #5c6bc0;
        }

        .avatar {
            width: 36px;
            height: 36px;
            background: #6a72ff;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 16px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Avatar letter from email
    avatar_letter = user_email[0].upper() if user_email else "U"

    st.markdown(f"""
        <div class="top-nav">

            <div class="top-left">
                <img src="https://raw.githubusercontent.com/lokauday/netdoc-ai/main/logo.png" class="netdoc-logo">
                <span class="app-title">NetDoc AI</span>
            </div>

            <div class="top-right">
                <span class="bell">🔔</span>
                <div class="avatar">{avatar_letter}</div>
            </div>

        </div>
    """, unsafe_allow_html=True)

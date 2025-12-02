# ===============================================================
#  NetDoc AI — Announcement Engine
# ===============================================================

import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal, Announcement, User
from datetime import datetime
import requests
import os


# ---------------------------------------------------------------
# CREATE ANNOUNCEMENT
# ---------------------------------------------------------------
def create_announcement(title: str, message: str):
    db = SessionLocal()
    ann = Announcement(title=title, message=message)
    db.add(ann)
    db.commit()
    db.close()

    # trigger email broadcast
    send_announcement_email(title, message)

    return True


# ---------------------------------------------------------------
# GET ALL ANNOUNCEMENTS
# ---------------------------------------------------------------
def list_announcements():
    db = SessionLocal()
    anns = db.query(Announcement).order_by(Announcement.created_at.desc()).all()
    db.close()
    return anns


# ---------------------------------------------------------------
# DELETE ANNOUNCEMENT
# ---------------------------------------------------------------
def delete_announcement(ann_id: int):
    db = SessionLocal()
    ann = db.query(Announcement).filter(Announcement.id == ann_id).first()
    if ann:
        db.delete(ann)
        db.commit()
    db.close()


# ---------------------------------------------------------------
# SEND EMAILS TO ALL USERS (SENDGRID)
# ---------------------------------------------------------------
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("MAIL_FROM", "netdoc@yourdomain.com")

def send_announcement_email(title, message):
    if not SENDGRID_API_KEY:
        print("❌ No SENDGRID_API_KEY found.")
        return

    db = SessionLocal()
    users = db.query(User).all()
    db.close()

    for u in users:
        send_email(u.email, title, message)


def send_email(to_email, title, message):
    SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"

    html_content = f"""
    <div style='background:#0d1117;padding:25px;color:white;font-family:Arial;border-radius:12px;'>
        <h2 style='color:#3ea6ff;'>{title}</h2>
        <p style='font-size:15px;line-height:1.5;'>{message}</p>
        <br>
        <p style='opacity:0.7;'>NetDoc AI Notification System</p>
    </div>
    """

    data = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": FROM_EMAIL},
        "subject": f"📢 NetDoc AI — {title}",
        "content": [{"type": "text/html", "value": html_content}],
    }

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        requests.post(SENDGRID_URL, json=data, headers=headers)
    except:
        print("Email send failed.")

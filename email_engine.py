import os
import requests

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_NAME = os.getenv("EMAIL_NAME")


def send_email_broadcast(subject, message, recipients):
    url = "https://api.sendgrid.com/v3/mail/send"

    data = {
        "personalizations": [
            {
                "to": [{"email": r} for r in recipients],
                "subject": subject
            }
        ],
        "from": {"email": EMAIL_FROM, "name": EMAIL_NAME},
        "content": [
            {
                "type": "text/html",
                "value": f"""
                <h2>{subject}</h2>
                <p>{message}</p>
                <br>
                <i>This message was sent by NetDoc AI (Admin)</i>
                """
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }

    requests.post(url, headers=headers, json=data)

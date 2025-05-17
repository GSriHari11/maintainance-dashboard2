import smtplib
from email.mime.text import MIMEText
import os

def send_password_email(recipient, new_password):
    EMAIL = os.getenv("EMAIL")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    try:
        msg = MIMEText(f"Your new password is: {new_password}")
        msg["Subject"] = "Password Reset"
        msg["From"] = EMAIL
        msg["To"] = recipient

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print("Email error:", e)
        return False

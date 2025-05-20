# import smtplib
# from email.mime.text import MIMEText
# from dotenv import load_dotenv
# import os

# load_dotenv()

# EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
# SMTP_SERVER = os.getenv("SMTP_SERVER")
# SMTP_PORT = int(os.getenv("SMTP_PORT"))

# def send_password_email(to_email, password):
#     msg = MIMEText(f"Your password for the HPCL dashboard is: {password}")
#     msg["Subject"] = "HPCL Dashboard - Password Recovery"
#     msg["From"] = EMAIL_ADDRESS
#     msg["To"] = to_email

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#         server.send_message(msg)


import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()  # Load .env file

def send_password_email(recipient_email, password):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    # Email content
    subject = "Your Login Password"
    body = f"Your password is: {password}"

    msg = MIMEMultipart()
    msg["From"] = smtp_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print("Failed to send email:", e)


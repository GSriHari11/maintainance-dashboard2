import smtplib
from email.mime.text import MIMEText
import os
import sqlite3
import re

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def is_valid_hpcl_email(email):
    return email.endswith("@hpcl.in")

def signup_user(email, password):
    if not is_valid_hpcl_email(email):
        return False, "Only HPCL email IDs allowed"

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    if c.fetchone():
        return False, "Email already exists"

    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()
    conn.close()
    return True, "User registered successfully"

def login_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def send_password_email(to_email, password):
    msg = MIMEText(f"Your HPCL dashboard password is: {password}")
    msg["Subject"] = "HPCL Dashboard - Password Recovery"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        raise Exception("Failed to send password email. Check your .env credentials.") from e
    
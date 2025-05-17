import smtplib
from email.mime.text import MIMEText
from db import add_user, get_user
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def signup_user(email, password):
    hashed_pwd = hash_password(password)
    add_user(email, hashed_pwd)

def login_user(email, password):
    user = get_user(email)
    if user and check_password(password, user[1]):
        return True
    return False

def send_password_email(to_email, password):
    msg = MIMEText(f"Your password is: {password}")
    msg["Subject"] = "Your HPCL Dashboard Password"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

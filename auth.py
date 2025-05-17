import json, os, hashlib, random
from datetime import datetime, timedelta
import streamlit as st
from email_utils import send_password_email

USERS_FILE = 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup():
    st.subheader("Create Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    if st.button("Signup"):
        if password != confirm:
            st.error("Passwords do not match.")
            return
        users = load_users()
        if email in users:
            st.error("Account already exists.")
            return
        users[email] = {
            "password": hash_password(password),
            "created": str(datetime.now())
        }
        save_users(users)
        st.success("Account created! You can now login.")

def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = load_users()
        if email in users and users[email]["password"] == hash_password(password):
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid credentials.")

def forgot_password():
    st.subheader("Forgot Password")
    email = st.text_input("Registered Email")
    if st.button("Send Password"):
        users = load_users()
        if email in users:
            new_password = ''.join(random.choices("0123456789abcdefghijklmnopqrstuvwxyz", k=8))
            users[email]["password"] = hash_password(new_password)
            save_users(users)
            send_password_email(email, new_password)
            st.success("New password sent to your email.")
        else:
            st.error("Email not found.")

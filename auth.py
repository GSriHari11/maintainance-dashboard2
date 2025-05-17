import streamlit as st
import pandas as pd
import random
import string
from email_utils import send_password_email

USER_DB = "users.xlsx"

def load_users():
    try:
        return pd.read_excel(USER_DB, sheet_name="Users")
    except Exception:
        return pd.DataFrame(columns=["username", "email", "password"])

def save_users(df):
    df.to_excel(USER_DB, sheet_name="Users", index=False)

def signup(username, email, password):
    df = load_users()
    if username in df['username'].values:
        return False, "Username already exists."
    if email in df['email'].values:
        return False, "Email already registered."
    df.loc[len(df)] = [username, email, password]
    save_users(df)
    return True, "User registered successfully."

def login(username, password):
    df = load_users()
    user = df[(df['username'] == username) & (df['password'] == password)]
    return not user.empty

def forgot_password(email):
    df = load_users()
    if email not in df['email'].values:
        return False, "Email not found."

    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    df.loc[df['email'] == email, 'password'] = new_password
    save_users(df)
    
    success = send_password_email(email, new_password)
    if success:
        return True, "A new password has been sent to your email."
    else:
        return False, "Failed to send email. Contact admin."

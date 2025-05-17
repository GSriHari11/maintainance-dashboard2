import streamlit as st
import pandas as pd
import hashlib
import os
from dashboard import show_dashboard  # Import dashboard function

# Path to your user database
USER_DB = "users.csv"

# Password hasher
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load or create user database
if not os.path.exists(USER_DB):
    df_users = pd.DataFrame(columns=["username", "password"])
    df_users.to_csv(USER_DB, index=False)

# Authentication logic
def login(username, password):
    users = pd.read_csv(USER_DB)
    hashed = hash_password(password)
    user = users[(users["username"] == username) & (users["password"] == hashed)]
    return not user.empty

def register(username, password):
    users = pd.read_csv(USER_DB)
    if username in users["username"].values:
        return False  # Username taken
    hashed = hash_password(password)
    new_user = pd.DataFrame([[username, hashed]], columns=["username", "password"])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USER_DB, index=False)
    return True

# App
st.set_page_config(page_title="Login", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Preventive Maintenance Login")

    menu = st.radio("Choose an option", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Login":
        if st.button("Login"):
            if login(username, password):
                st.success("Login successful")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect username or password")
    else:
        if st.button("Register"):
            if register(username, password):
                st.success("Account created! You can now log in.")
            else:
                st.warning("Username already exists.")
else:
    # Once logged in, show dashboard
    show_dashboard()

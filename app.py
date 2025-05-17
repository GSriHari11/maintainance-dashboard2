import streamlit as st
from auth import init_user_data, save_user, check_login, get_password
from email_utils import send_password_email

st.set_page_config(page_title="Maintenance Dashboard", page_icon="🛠️", layout="centered")
init_user_data()

st.title("🔐 HPCL Maintenance Dashboard Login")

menu = st.radio("Choose", ["Login", "Signup", "Forgot Password"])

if menu == "Signup":
    email = st.text_input("Email", placeholder="Only @hpcl.in allowed")
    password = st.text_input("Password", type="password")
    if st.button("Create Account"):
        if not email.endswith("@hpcl.in"):
            st.error("Only @hpcl.in email addresses are allowed.")
        elif save_user(email, password):
            st.success("User registered successfully.")
        else:
            st.warning("User already exists.")

elif menu == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(email, password):
            st.success("Login successful!")
            st.write(f"Welcome, {email}")
            # Place dashboard logic here
        else:
            st.error("Invalid credentials.")

elif menu == "Forgot Password":
    email = st.text_input("Enter your HPCL Email")
    if st.button("Send Password"):
        if not email.endswith("@hpcl.in"):
            st.error("Only @hpcl.in email addresses are allowed.")
        else:
            pwd = get_password(email)
            if pwd:
                send_password_email(email, pwd)
                st.success("Password sent to your email.")
            else:
                st.warning("Email not registered.")

import streamlit as st
from auth import signup_user, login_user, reset_password
from email_utils import send_email
import random
import string

st.set_page_config(page_title="Maintenance Dashboard", layout="centered")

def generate_temp_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

st.title("Dashboard")

menu = st.radio("Choose", ["Login", "Signup", "Forgot Password"])

if menu == "Login":
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if login_user(email, password):
            st.success("Logged in successfully.")
        else:
            st.error("Invalid credentials.")

elif menu == "Signup":
    with st.form("signup_form"):
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        submit = st.form_submit_button("Create Account")

        if submit:
            if not email.endswith("@hpcl.in"):
                st.error("Only @hpcl.in emails are allowed.")
            else:
                success, msg = signup_user(email, password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

elif menu == "Forgot Password":
    email = st.text_input("Enter your registered email")
    if st.button("Send Temporary Password"):
        temp_pass = generate_temp_password()
        success, msg = reset_password(email, temp_pass)
        if success:
            email_body = f"Your temporary password is: {temp_pass}"
            sent = send_email(email, "Password Reset - Maintenance Dashboard", email_body)
            if sent:
                st.success("Temporary password sent to your email.")
            else:
                st.error("Failed to send email. Try again later.")
        else:
            st.error(msg)

import streamlit as st
from auth import signup_user, login_user, send_password_email, is_valid_hpcl_email
from db import create_users_table, get_user

create_users_table()
st.set_page_config(page_title="HPCL Dashboard", page_icon="🛡️", layout="centered")

st.title("🔐 HPCL Dashboard Login")

menu = st.radio("Choose Action", ["Login", "Sign Up", "Forgot Password"])

if menu == "Login":
    st.subheader("Login to your HPCL account")
    email = st.text_input("HPCL Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if not is_valid_hpcl_email(email):
            st.error("Only @hpcl.in email addresses are allowed.")
        elif login_user(email, password):
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = email
            st.success(f"Welcome, {email}")
        else:
            st.error("Incorrect email or password.")

elif menu == "Sign Up":
    st.subheader("Create HPCL Account")
    email = st.text_input("Enter HPCL Email")
    password = st.text_input("Create Password", type="password")
    if st.button("Register"):
        success, msg = signup_user(email, password)
        if success:
            st.success(msg)
        else:
            st.error(msg)

elif menu == "Forgot Password":
    st.subheader("Forgot Password")
    email = st.text_input("Enter your registered HPCL email")
    if st.button("Send Password"):
        user = get_user(email)
        if user:
            try:
                send_password_email(email, user[1])
                st.success("Password has been sent to your email.")
            except Exception as e:
                st.error("Failed to send email. Check your .env settings.")
        else:
            st.error("Email not found.")

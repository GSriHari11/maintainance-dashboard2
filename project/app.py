import streamlit as st
from auth import signup_user, login_user, send_password_email
from db import create_users_table, get_user

create_users_table()

st.set_page_config(page_title="HPCL Dashboard", page_icon="🛡️", layout="centered")

st.markdown("## 🔐 HPCL Login System")

menu = st.radio("Choose an option", ["Login", "Sign Up", "Forgot Password"])

if menu == "Sign Up":
    st.subheader("🔴 Sign Up")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        if "@hpcl.in" in email:
            if get_user(email):
                st.warning("User already exists.")
            else:
                signup_user(email, password)
                st.success("Account created!")
        else:
            st.error("Only @hpcl.in emails are allowed.")

elif menu == "Login":
    st.subheader("🟢 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(email, password):
            st.success("Login successful")
            st.write(f"Welcome, {email.split('@')[0].capitalize()}!")
            # Actual dashboard content goes here
        else:
            st.error("Invalid email or password")

elif menu == "Forgot Password":
    st.subheader("🔵 Forgot Password")
    email = st.text_input("Enter your registered HPCL email")

    if st.button("Send Password"):
        user = get_user(email)
        if user:
            send_password_email(email, user[1])
            st.success("Password sent to your email")
        else:
            st.error("Email not found")

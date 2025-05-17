import streamlit as st
from auth import signup, login, forgot_password
from dotenv import load_dotenv

load_dotenv()

st.title("Preventive Maintenance Dashboard")

menu = st.radio("Choose", ["Login", "Signup", "Forgot Password"])

if menu == "Signup":
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create Account"):
        success, msg = signup(username, email, password)
        st.success(msg) if success else st.error(msg)

elif menu == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success("You are logged in!")
            st.write("Welcome to the Preventive Maintenance Dashboard!")
            st.button("Logout")
        else:
            st.error("Invalid credentials.")

elif menu == "Forgot Password":
    email = st.text_input("Enter your registered email")
    if st.button("Reset Password"):
        success, msg = forgot_password(email)
        st.success(msg) if success else st.error(msg)

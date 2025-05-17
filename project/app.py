import streamlit as st
from auth import signup_user, login_user, reset_password
from database import setup_database
from database import create_connection  # Add this line

setup_database()

st.title("🔐 HPCL Maintenance Dashboard Login")

menu = ["Login", "Sign Up", "Forgot Password", "Admin View"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login to your account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.success("Logged in successfully.")
        else:
            st.error("Invalid credentials")

elif choice == "Sign Up":
    st.subheader("Create New Account")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        success, msg = signup_user(email, password)
        if success:
            st.success(msg)
        else:
            st.error(msg)

elif choice == "Forgot Password":
    st.subheader("Reset Password")
    email = st.text_input("Registered Email")
    if st.button("Send Password"):
        success, msg = reset_password(email)
        if success:
            st.success(msg)
        else:
            st.error(msg)

elif choice == "Admin View":
    st.subheader("All Registered Users (Admin Only)")
    email = st.text_input("Enter your HPCL email to access admin view")
    if st.button("View Registered Users"):
        if email in ADMINS:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT email, password FROM users")
            users = cursor.fetchall()
            conn.close()

            st.write("### Registered HPCL Users")
            for u in users:
                st.write(f"📧 {u[0]} | 🔑 {u[1]}")
        else:
            st.error("Access denied. You are not authorized to view this section.")


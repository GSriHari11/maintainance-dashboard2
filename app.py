import streamlit as st
from auth import login, signup, forgot_password

st.set_page_config(page_title="Login System", page_icon="🔐", layout="centered")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    page = st.sidebar.radio("Choose", ["Login", "Signup", "Forgot Password"])
    if page == "Login":
        login()
    elif page == "Signup":
        signup()
    elif page == "Forgot Password":
        forgot_password()
else:
    st.success("✅ You are logged in!")

    # Placeholder for dashboard content
    st.write("Welcome to the Preventive Maintenance Dashboard!")
    
    if st.button("Logout"):
        st.session_state["authenticated"] = False

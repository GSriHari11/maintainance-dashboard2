import streamlit as st
from auth import signup_user, login_user
from database import init_db

init_db()

def main():
    st.title("🔐 HPCL Maintenance Dashboard - Login")

    option = st.radio("Choose an option", ["Login", "Sign Up"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            success, msg = login_user(email, password)
            st.success(msg) if success else st.error(msg)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["email"] = email
                st.experimental_rerun()
    else:
        if st.button("Create Account"):
            success, msg = signup_user(email, password)
            st.success(msg) if success else st.error(msg)

    if st.session_state.get("logged_in"):
        st.success(f"Welcome {st.session_state['email']}! You are logged in.")
        st.write("Here goes your dashboard...")

if __name__ == "__main__":
    main()

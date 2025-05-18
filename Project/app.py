import streamlit as st
from auth import signup_user, login_user, reset_password
from database import setup_database
from database import create_connection  # Add this line
from excel_processor import build_status_summary, all_months
import pandas as pd
import plotly.express as px

setup_database()

st.title("🔐 HPCL Maintenance Dashboard Login")

menu = ["Login", "Sign Up", "Forgot Password", "Admin View"]

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# List of admin credentials (you can add more here later)
ADMINS = {
    "golla.srihari@hpcl.in": "1234567890"  # <-- your admin password
}

# Sidebar menu
if not st.session_state.logged_in:
    choice = st.sidebar.selectbox("Menu", menu)
else:
    choice = "Dashboard"  # Default page after login
# if choice == "Login":
#     st.subheader("Login to your account")
#     email = st.text_input("Email", key="login_email")
#     password = st.text_input("Password", type="password", key="login_password")
#     if st.button("Login"):
#         user = login_user(email, password)
#         if user:
#             st.success("Logged in successfully.")
#         else:
            # st.error("Invalid credentials")

# --------- LOGIN ---------
if choice == "Login":
    st.subheader("Login to your account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success("✅ Logged in successfully.")
            st.rerun()  # Force rerun to go to dashboard
        else:
            st.error("❌ Invalid credentials.")


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
    st.subheader("🔐 HPCL Maintenance Dashboard Login")
    st.markdown("### All Registered Users (Admin Only)")

    admin_email = st.text_input("Enter Admin HPCL Email")
    admin_password = st.text_input("Enter Admin Password", type="password")

    if st.button("View Registered Users"):
        if admin_email in ADMINS and ADMINS[admin_email] == admin_password:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT email, password FROM users")
            users = cursor.fetchall()
            conn.close()

            st.success("✅ Admin access granted.")
            st.write("### 👥 Registered Users")
            for u in users:
                st.write(f"📧 **{u[0]}** | 🔑 `{u[1]}`")
        else:
            st.error("❌ Invalid admin credentials. Access denied.")

# --------- DASHBOARD ---------
elif choice == "Dashboard" and st.session_state.logged_in:
    st.title("🛠️ Preventive Maintenance Dashboard")
    st.sidebar.success(f"Welcome, {st.session_state.username}!")

    # ---------------- FILTERS ----------------
    all_months = [
        "Apr-24", "May-24", "Jun-24", "Jul-24", "Aug-24", "Sep-24", "Oct-24", "Nov-24", "Dec-24",
        "Jan-25", "Feb-25", "Mar-25", "Apr-25", "May-25", "Jun-25", "Jul-25", "Aug-25", "Sep-25",
        "Oct-25", "Nov-25", "Dec-25", "Jan-26", "Feb-26", "Mar-26"
    ]

    st.sidebar.header("📅 Filter Options")
    selected_month = st.sidebar.selectbox("Select Month", all_months, index=0)
    selected_status = st.sidebar.multiselect("Select Status", ["Completed", "Pending"], default=["Completed", "Pending"])

    # ---------------- DATA PROCESSING ----------------
    summary = build_status_summary(selected_month)
    mon_comp = summary["monthly_completed"]
    mon_pend = summary["monthly_pending"]
    cum_comp = summary["cumulative_completed"]
    cum_pend = summary["cumulative_pending"]

    # ---------------- DASHBOARD DISPLAY ----------------
    st.subheader(f"Maintenance Summary for {selected_month}")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("✅ Completed (Monthly)", mon_comp)
        st.metric("📊 Completed (Cumulative)", cum_comp)

    with col2:
        st.metric("⏳ Pending (Monthly)", mon_pend)
        st.metric("📊 Pending (Cumulative)", cum_pend)

    # Optional: You can expand to show more data or visuals if needed

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

        
    # st.title("🛠️ Preventive Maintenance ")

    # # Filters
    # selected_month = st.selectbox("📅 Select Month", all_months, key="month_filter")
    # selected_status = st.multiselect("✅ Select Status", ["Completed", "Pending"], default=["Completed", "Pending"], key="status_filter")

    # # Load and filter data
    # # df, mon_comp, mon_pend, cum_comp, cum_pend = build_status_summary(selected_month)
    # summary = build_status_summary(selected_month)
    # mon_comp = summary["monthly_completed"]
    # mon_pend = summary["monthly_pending"]
    # cum_comp = summary["cumulative_completed"]
    # cum_pend = summary["cumulative_pending"]

    # # filtered_df = df[df["Status"].isin(selected_status)]

    # st.markdown("### Maintenance Task Overview")
    # st.dataframe(filtered_df)

    # # Summary Stats
    # st.write(f"**{selected_month} Summary:** ✅ Completed: `{mon_comp}`, ❌ Pending: `{mon_pend}`")
    # st.write(f"**Cumulative till {selected_month}:** ✅ Completed: `{cum_comp}`, ❌ Pending: `{cum_pend}`")

    # # Logout button
    # if st.button("Logout"):
    #     st.session_state.logged_in = False
    #     st.session_state.user_email = ""
    #     st.rerun()


# import streamlit as st
# from auth import signup_user, login_user, reset_password
# from database import setup_database, create_connection
# from excel_processor import build_status_summary, all_months

# setup_database()

# st.title("🔐 HPCL Maintenance Dashboard Login")
# menu = ["Login", "Sign Up", "Forgot Password", "Admin View"]
# ADMINS = {"golla.srihari@hpcl.in": "1234567890"}

# choice = st.sidebar.selectbox("Menu", menu)

# if choice == "Login":
#     st.subheader("Login to your account")
#     email = st.text_input("Email", key="login_email")
#     password = st.text_input("Password", type="password", key="login_password")
#     if st.button("Login"):
#         user = login_user(email, password)
#         if user:
#             st.success("Logged in successfully.")
#             st.subheader("📊 Maintenance Data Viewer")
#             selected_month = st.selectbox("Select Month", all_months)
#             if st.button("Show Data"):
#                 df, mon_comp, mon_pend, cum_comp, cum_pend = build_status_summary(selected_month)
#                 st.write(f"### ✅ {selected_month} Summary")
#                 st.write(f"Completed: `{mon_comp}`, Pending: `{mon_pend}`")
#                 st.write(f"Cumulative till {selected_month} - Completed: `{cum_comp}`, Pending: `{cum_pend}`")
#                 st.write("### 📄 Excel Data:")
#                 st.dataframe(df)
#         else:
#             st.error("Invalid credentials")

# elif choice == "Sign Up":
#     st.subheader("Create New Account")
#     email = st.text_input("Email", key="signup_email")
#     password = st.text_input("Password", type="password", key="signup_password")
#     if st.button("Sign Up"):
#         success, msg = signup_user(email, password)
#         st.success(msg) if success else st.error(msg)

# elif choice == "Forgot Password":
#     st.subheader("Reset Password")
#     email = st.text_input("Registered Email")
#     if st.button("Send Password"):
#         success, msg = reset_password(email)
#         st.success(msg) if success else st.error(msg)

# elif choice == "Admin View":
#     st.subheader("🔐 HPCL Maintenance Dashboard Admin View")
#     admin_email = st.text_input("Enter Admin HPCL Email")
#     admin_password = st.text_input("Enter Admin Password", type="password")
#     if st.button("View Registered Users"):
#         if admin_email in ADMINS and ADMINS[admin_email] == admin_password:
#             conn = create_connection()
#             cursor = conn.cursor()
#             cursor.execute("SELECT email, password FROM users")
#             users = cursor.fetchall()
#             conn.close()
#             st.success("✅ Admin access granted.")
#             st.write("### 👥 Registered Users")
#             for u in users:
#                 st.write(f"📧 **{u[0]}** | 🔑 `{u[1]}`")
#         else:
#             st.error("❌ Invalid admin credentials. Access denied.")

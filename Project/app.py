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

# List of admin credentials (you can add more here later)
ADMINS = {
    "golla.srihari@hpcl.in": "1234567890"  # <-- your admin password
}

choice = st.sidebar.selectbox("Menu", menu)

# if choice == "Login":
#     st.subheader("Login to your account")
#     email = st.text_input("Email", key="login_email")
#     password = st.text_input("Password", type="password", key="login_password")
#     if st.button("Login"):
#         user = login_user(email, password)
#         if user:
#             st.success("Logged in successfully.")
#         else:
            st.error("Invalid credentials")

if choice == "Login":
    st.subheader("Login to your account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.success("✅ Logged in successfully.")
            st.markdown("### 🛠️ Preventive Maintenance Dashboard")

            # Filters
            col1, col2 = st.columns(2)
            with col1:
                selected_month = st.selectbox("📅 Select Month", all_months)
            with col2:
                status_filter = st.multiselect("📌 Select Status", ["Pending", "Completed"], default=["Pending", "Completed"])

            # Process summary
            summary = build_status_summary(selected_month)
            total_tasks = summary["monthly_pending"] + summary["monthly_completed"]

            # Pie Chart
            pie_data = []
            if "Pending" in status_filter:
                pie_data.append({"Status": "Pending", "Count": summary["monthly_pending"]})
            if "Completed" in status_filter:
                pie_data.append({"Status": "Completed", "Count": summary["monthly_completed"]})

            if pie_data:
                df_pie = pd.DataFrame(pie_data)
                fig = px.pie(df_pie, names="Status", values="Count", title="Maintenance Status Breakdown")
                st.plotly_chart(fig, use_container_width=True)

            # Task Summary
            st.markdown("### 📊 Task Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("🧮 Total Tasks", total_tasks)
            col2.metric("✅ Completed", summary["monthly_completed"])
            col3.metric("⏳ Pending", summary["monthly_pending"])
        else:
            st.error("❌ Invalid credentials. Please try again.")


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

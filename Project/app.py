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
#             st.error("Invalid credentials")

if choice == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if login_user(email, password):
            st.success("Logged in successfully.")
            
            # Page configuration
            st.set_page_config(page_title="Status Dashboard", layout="wide")

            st.title("✅ Monthly Task Status Dashboard")

            # Month selection
            selected_month = st.selectbox("Select Month", all_months)

            if selected_month:
                # Process the selected month
                summary = build_status_summary(selected_month)

                st.subheader(f"📅 Status Summary for {selected_month}")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("✅ Completed (This Month)", summary["monthly_completed"])
                    st.metric("📊 Cumulative Completed", summary["cumulative_completed"])
                with col2:
                    st.metric("⏳ Pending (This Month)", summary["monthly_pending"])
                    st.metric("📉 Cumulative Pending", summary["cumulative_pending"])

            # st.markdown("### 📊 Maintenance Dashboard")
            
            # selected_month = st.selectbox("Select Month", all_months)
            # status_filter = st.multiselect("Select Status", ["Pending", "Completed"], default=["Pending", "Completed"])

            # # Load and filter data
            # data = build_status_summary(selected_month)

            # # Filter by status
            # pie_data = []
            # if "Pending" in status_filter:
            #     pie_data.append({"Status": "Pending", "Count": data["monthly_pending"]})
            # if "Completed" in status_filter:
            #     pie_data.append({"Status": "Completed", "Count": data["monthly_completed"]})

            # if pie_data:
            #     df_pie = pd.DataFrame(pie_data)
            #     fig = px.pie(df_pie, names="Status", values="Count", title="Task Status Distribution")
            #     st.plotly_chart(fig)

            # # Task Summary
            # total_tasks = data["monthly_pending"] + data["monthly_completed"]
            # st.subheader("Task Summary")
            # st.metric("Total Tasks", total_tasks)
            # st.metric("Pending", data["monthly_pending"])
            # st.metric("Completed", data["monthly_completed"])
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

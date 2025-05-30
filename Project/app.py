# import streamlit as st
# from auth import signup_user, login_user, reset_password
# from database import setup_database
# from database import create_connection  # Add this line
# from excel_processor import build_status_summary, all_months
# import pandas as pd
# import plotly.express as px

# setup_database()


# menu = ["Login", "Sign Up", "Forgot Password", "Admin View"]

# # Initialize session state for login
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "user_email" not in st.session_state:
#     st.session_state.user_email = ""

# # List of admin credentials (you can add more here later)
# ADMINS = {
#     "golla.srihari@hpcl.in": "1234567890"  # <-- your admin password
# }

# # Sidebar menu
# if not st.session_state.logged_in:
#     st.title("🔐 HPCL Maintenance Dashboard Login")
#     choice = st.sidebar.selectbox("Menu", menu)
# else:
#     choice = "Dashboard"  # Default page after login


# # --------- LOGIN ---------
# if choice == "Login":
#     st.subheader("Login to your account")
#     email = st.text_input("Email", key="login_email")
#     password = st.text_input("Password", type="password", key="login_password")

#     if st.button("Login"):
#         user = login_user(email, password)
#         if user:
#             st.session_state.logged_in = True
#             st.session_state.user_email = email
#             st.success("✅ Logged in successfully.")
#             st.rerun()  # Force rerun to go to dashboard
#         else:
#             st.error("❌ Invalid credentials.")


# elif choice == "Sign Up":
#     st.subheader("Create New Account")
#     email = st.text_input("Email", key="signup_email")
#     password = st.text_input("Password", type="password", key="signup_password")
#     if st.button("Sign Up"):
#         success, msg = signup_user(email, password)
#         if success:
#             st.success(msg)
#         else:
#             st.error(msg)

# elif choice == "Forgot Password":
#     st.subheader("Reset Password")
#     email = st.text_input("Registered Email")
#     if st.button("Send Password"):
#         success, msg = reset_password(email)
#         if success:
#             st.success(msg)
#         else:
#             st.error(msg)

# elif choice == "Admin View":
#     st.markdown("### All Registered Users (Admin Only)")

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

# # --------- DASHBOARD ---------
# elif choice == "Dashboard" and st.session_state.logged_in:
#     st.title("🛠️ Preventive Maintenance Compliance")
#     # st.sidebar.success(f"Welcome, {st.session_state.username}!")

#     # ---------------- FILTERS ----------------
#     all_months = [
#         "Apr-24", "May-24", "Jun-24", "Jul-24", "Aug-24", "Sep-24", "Oct-24", "Nov-24", "Dec-24",
#         "Jan-25", "Feb-25", "Mar-25", "Apr-25", "May-25", "Jun-25", "Jul-25", "Aug-25", "Sep-25",
#         "Oct-25", "Nov-25", "Dec-25", "Jan-26", "Feb-26", "Mar-26"
#     ]

#     st.sidebar.header("📅 Filter Options")
#     selected_month = st.sidebar.selectbox("Select Month", all_months, index=0)
#     selected_status = st.sidebar.multiselect("Select Status", ["Completed", "Pending"], default=["Completed", "Pending"])

#     # ---------------- DATA PROCESSING ----------------
#     summary = build_status_summary(selected_month)
#     mon_comp = summary["monthly_completed"]
#     mon_pend = summary["monthly_pending"]
#     cum_comp = summary["cumulative_completed"]
#     cum_pend = summary["cumulative_pending"]

#     # ---------------- DASHBOARD DISPLAY ----------------
#     st.subheader(f"Maintenance Summary for {selected_month}")
#     col1, col2 = st.columns(2)

#     with col1:
#         st.metric("✅ Completed (Monthly)", mon_comp)
#         st.metric("📊 Completed (Cumulative)", cum_comp)

#     with col2:
#         st.metric("⏳ Pending (Monthly)", mon_pend)
#         st.metric("📊 Pending (Cumulative)", cum_pend)

#     # Optional: You can expand to show more data or visuals if needed

#     if st.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = ""
#         # st.experimental_rerun()


#--------------------------------------------------------------------------------------------------------------- 
# import streamlit as st
# from auth import signup_user, login_user, reset_password
# from database import setup_database, create_connection
# from excel_processor import build_status_summary, all_months
# import pandas as pd
# import plotly.express as px

# setup_database()

# menu = ["Login", "Sign Up", "Forgot Password", "Admin View"]

# # Initialize session state
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "user_email" not in st.session_state:
#     st.session_state.user_email = ""
# if "current_page" not in st.session_state:
#     st.session_state.current_page = "Login"

# ADMINS = {
#     "golla.srihari@hpcl.in": "1234567890"
# }

# # ------------------ ROUTING ------------------
# if not st.session_state.logged_in:
#     st.title("🔐 HPCL Maintenance Dashboard Login")
#     choice = st.sidebar.selectbox("Menu", menu)
# else:
#     choice = st.session_state.current_page

# # ------------------ LOGIN ------------------
# if choice == "Login":
#     st.subheader("Login to your account")
#     email = st.text_input("Email", key="login_email")
#     password = st.text_input("Password", type="password", key="login_password")

#     if st.button("Login"):
#         user = login_user(email, password)
#         if user:
#             st.session_state.logged_in = True
#             st.session_state.user_email = email
#             st.session_state.current_page = "Welcome"
#             st.success("✅ Logged in successfully.")
#             st.rerun()
#         else:
#             st.error("❌ Invalid credentials.")

# # ------------------ SIGNUP ------------------
# elif choice == "Sign Up":
#     st.subheader("Create New Account")
#     email = st.text_input("Email", key="signup_email")
#     password = st.text_input("Password", type="password", key="signup_password")
#     if st.button("Sign Up"):
#         success, msg = signup_user(email, password)
#         if success:
#             st.success(msg)
#         else:
#             st.error(msg)

# # ------------------ FORGOT PASSWORD ------------------
# elif choice == "Forgot Password":
#     st.subheader("Reset Password")
#     email = st.text_input("Registered Email")
#     if st.button("Send Password"):
#         success, msg = reset_password(email)
#         if success:
#             st.success(msg)
#         else:
#             st.error(msg)

# # ------------------ ADMIN VIEW ------------------
# elif choice == "Admin View":
#     st.markdown("### All Registered Users (Admin Only)")
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

# # ------------------ WELCOME PAGE ------------------
# elif choice == "Welcome":
#     st.title("👋 Welcome Page")
#     st.markdown(f"## Welcome, 👤 **{st.session_state.user_email}**")
#     st.markdown("### 🛠️ Rotary Equipments Compliance Status")

    
#     with st.expander("📌 Preventive Maintenance Status"):
#         st.write("➡️ Go to sidebar and view maintenance summary for each month.")

#     with st.expander("🔍 Predictive Maintenance Status"):
#         options = ["Vibration Monitoring", "Ultrasound Monitoring", "Lube Oil Analysis", "Coupling Inspection"]
#         # selected = st.radio("Choose a method to explore:", options)

#         # st.subheader("🔍 Choose a Predictive Maintenance Option")
#         option = st.radio("Select Option:", ["None", "Vibration Monitoring", "Ultrasound Monitoring", "Lube Oil Analysis", "Coupling Inspection"])

#     if option == "Vibration Monitoring":
#         st.session_state.current_page = "Dashboard"
#         st.rerun()

# # ------------------ DASHBOARD ------------------
# elif choice == "Dashboard":
#     st.markdown("🔎 Vibration Monitoring Status")
#     # st.image("vibration_status_image.png", caption="Vibration Monitoring Dashboard", use_column_width=True)

#     # st.markdown("---")
#     # st.header("🛠️ Preventive Maintenance Compliance Summary")

#     st.sidebar.header("📅 Filter Options")
#     selected_month = st.sidebar.selectbox("Select Month", all_months, index=0)
#     selected_status = st.sidebar.multiselect("Select Status", ["Completed", "Pending"], default=["Completed", "Pending"])

#     summary = build_status_summary(selected_month)
#     mon_comp = summary["monthly_completed"]
#     mon_pend = summary["monthly_pending"]
#     cum_comp = summary["cumulative_completed"]
#     cum_pend = summary["cumulative_pending"]

#     st.subheader(f"Maintenance Summary for {selected_month}")
#     col1, col2 = st.columns(2)
#     with col1:
#         st.metric("✅ Completed (Monthly)", mon_comp)
#         st.metric("📊 Completed (Cumulative)", cum_comp)
#     with col2:
#         st.metric("⏳ Pending (Monthly)", mon_pend)
#         st.metric("📊 Pending (Cumulative)", cum_pend)

#     if st.button("⬅ Back to Welcome Page"):
#         st.session_state.current_page = "Welcome"
#         st.rerun()

# # ------------------ LOGOUT ------------------
# st.sidebar.markdown("---")
# if st.session_state.logged_in:
#     if st.sidebar.button("🚪 Logout"):
#         for key in ["logged_in", "user_email", "current_page"]:
#             st.session_state[key] = False if key == "logged_in" else ""
#         st.rerun()

#------------------------------------------------------------------------------------------------------------

# import streamlit as st
# from auth import signup_user, login_user, reset_password
# from database import setup_database, create_connection
# from excel_processor import build_status_summary, all_months
# import pandas as pd
# import plotly.express as px

# setup_database()

# menu = ["Login", "Sign Up", "Forgot Password", "Admin View"]

# # Initialize session state
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "user_email" not in st.session_state:
#     st.session_state.user_email = ""
# if "current_page" not in st.session_state:
#     st.session_state.current_page = "Login"

# ADMINS = {
#     "golla.srihari@hpcl.in": "1234567890"
# }

# # ------------------ ROUTING ------------------
# if not st.session_state.logged_in:
#     st.title("🔐 HPCL Maintenance Dashboard Login")
#     choice = st.sidebar.selectbox("Menu", menu)
# else:
#     choice = st.session_state.current_page

# def login_function():
#     st.subheader("Login to your account")
#     email = st.text_input("Email", key="login_email")
#     password = st.text_input("Password", type="password", key="login_password")

#     if st.button("Login"):
#         user = login_user(email, password)
#         if user:
#             st.session_state.logged_in = True
#             st.session_state.user_email = email
#             st.session_state.current_page = "Welcome"
#             st.success("✅ Logged in successfully.")
#             st.rerun()
#         else:
#             st.error("❌ Invalid credentials.")

# def signup_function():
#     st.subheader("Create New Account")
#     email = st.text_input("Email", key="signup_email")
#     password = st.text_input("Password", type="password", key="signup_password")
#     if st.button("Sign Up"):
#         success, msg = signup_user(email, password)
#         if success:
#             st.success(msg)
#         else:
#             st.error(msg)

# def forget_password_function():
#     st.subheader("Reset Password")
#     email = st.text_input("Registered Email")
#     if st.button("Send Password"):
#         success, msg = reset_password(email)
#         if success:
#             st.success(msg)
#         else:
#             st.error(msg)


# def Admin_view_function():
#     st.markdown("### All Registered Users (Admin Only)")
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

# def welcome_function():
#     st.title("👋 Welcome Page")
#     st.markdown(f"## Welcome, 👤 **{st.session_state.user_email}**")
#     st.markdown("### 🛠️ Rotary Equipments Compliance Status")

    
#     with st.expander("📌 Preventive Maintenance Status"):
#         st.write("➡️ Go to sidebar and view maintenance summary for each month.")

#     with st.expander("🔍 Predictive Maintenance Status"):
#         options = ["Vibration Monitoring", "Ultrasound Monitoring", "Lube Oil Analysis", "Coupling Inspection"]
#         # selected = st.radio("Choose a method to explore:", options)

#         # st.subheader("🔍 Choose a Predictive Maintenance Option")
#         option = st.radio("Select Option:", ["Vibration Monitoring", "Ultrasound Monitoring", "Lube Oil Analysis", "Coupling Inspection"])

#     if option == "Vibration Monitoring":
#         st.session_state.current_page = "Dashboard"
#         st.rerun()

# def vibration_monitoring_function():
#     st.markdown("🔎 Vibration Monitoring Status")
#     # st.image("vibration_status_image.png", caption="Vibration Monitoring Dashboard", use_column_width=True)

#     # st.markdown("---")
#     # st.header("🛠️ Preventive Maintenance Compliance Summary")

#     st.sidebar.header("📅 Filter Options")
#     selected_month = st.sidebar.selectbox("Select Month", all_months, index=0)
#     selected_status = st.sidebar.multiselect("Select Status", ["Completed", "Pending"], default=["Completed", "Pending"])

#     summary = build_status_summary(selected_month)
#     mon_comp = summary["monthly_completed"]
#     mon_pend = summary["monthly_pending"]
#     cum_comp = summary["cumulative_completed"]
#     cum_pend = summary["cumulative_pending"]

#     st.subheader(f"Maintenance Summary for {selected_month}")
#     col1, col2 = st.columns(2)
#     with col1:
#         st.metric("✅ Completed (Monthly)", mon_comp)
#         st.metric("📊 Completed (Cumulative)", cum_comp)
#     with col2:
#         st.metric("⏳ Pending (Monthly)", mon_pend)
#         st.metric("📊 Pending (Cumulative)", cum_pend)

#     if st.button("⬅ Back to Welcome Page"):
#         st.session_state.current_page = "Welcome"
#         st.rerun()

# # ------------------ LOGIN ------------------
# if choice == "Login":
#     login_function()

# # ------------------ SIGNUP ------------------
# elif choice == "Sign Up":
#     signup_function()
    
# # ------------------ FORGOT PASSWORD ------------------
# elif choice == "Forgot Password":
#     forget_password_function()

# # ------------------ ADMIN VIEW ------------------
# elif choice == "Admin View":
#     Admin_view_function()

# # ------------------ WELCOME PAGE ------------------
# elif choice == "Welcome":
#     welcome_function()

# # ------------------ DASHBOARD ------------------
# elif choice == "Dashboard":
#     vibration_monitoring_function()

# # ------------------ LOGOUT ------------------
# st.sidebar.markdown("---")
# if st.session_state.logged_in:
#     if st.sidebar.button("🚪 Logout"):
#         for key in ["logged_in", "user_email", "current_page"]:
#             st.session_state[key] = False if key == "logged_in" else ""
#         st.rerun()

#------------------------------------------------------------------------------------------------------------------
import streamlit as st
from auth import signup_user, login_user, reset_password
from database import setup_database, create_connection  
from excel_processor import build_status_summary, all_months
import pandas as pd

# ------------------ SETUP ------------------
setup_database()

menu = ["Login", "Sign Up", "Forgot Password", "Admin View"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "Login"

ADMINS = {
    "golla.srihari@hpcl.in": "1234567890"
}

# ------------------ FUNCTIONS ------------------

def login_function():
    st.subheader("Login to your account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.current_page = "Welcome"
            st.success("✅ Logged in successfully.")
            st.rerun()
        else:
            st.error("❌ Invalid credentials.")

def signup_function():
    st.subheader("Create New Account")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        success, msg = signup_user(email, password)
        if success:
            st.success(msg)
        else:
            st.error(msg)

def forget_password_function():
    st.subheader("Reset Password")
    email = st.text_input("Registered Email")
    if st.button("Send Password"):
        success, msg = reset_password(email)
        if success:
            st.success(msg)
        else:
            st.error(msg)

def admin_view_function():
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

def welcome_function():
    st.title("⚙️Rotary Equipments Compliance Status")
    st.markdown(f"## 👋 Welcome, 👤 **{st.session_state.user_email}**")
    # st.markdown("### 🛠️ Rotary Equipments Compliance Status")

    with st.expander("🧰 Preventive Maintenance Status"):
        st.write("➡️ Go to sidebar and view maintenance summary for each month.")

    with st.expander("🔍 Predictive Maintenance Status"):
        option = st.radio("Select Option:", ["None","Vibration Monitoring", "Ultrasound Monitoring", "Lube Oil Analysis", "Coupling Inspection"])
        if option == "Vibration Monitoring":
            st.session_state.current_page = "Dashboard"
            st.session_state.maintenance_option = "None"  # Reset to prevent re-triggering
            st.rerun()

def vibration_monitoring_function():
    st.header("📈 Vibration Monitoring Status")

    st.sidebar.header("📅 Filter Options")
    selected_month = st.sidebar.selectbox("Select Month", all_months, index=0)
    selected_status = st.sidebar.multiselect("Select Status", ["Completed", "Pending"], default=["Completed", "Pending"])

    summary = build_status_summary(selected_month)
    mon_comp = summary["monthly_completed"]
    mon_pend = summary["monthly_pending"]
    cum_comp = summary["cumulative_completed"]
    cum_pend = summary["cumulative_pending"]

    st.subheader(f"Maintenance Summary for {selected_month}")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ Completed (Monthly)", mon_comp)
        st.metric("📊 Completed (Cumulative)", cum_comp)
    with col2:
        st.metric("⏳ Pending (Monthly)", mon_pend)
        st.metric("📊 Pending (Cumulative)", cum_pend)

    if st.button("⬅ Back to Welcome Page"):
        st.session_state.current_page = "Welcome"
        st.rerun()


# ------------------ PAGE ROUTING ------------------

if not st.session_state.logged_in:
    st.title("🔐 HPCL Maintenance Dashboard Login")
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        login_function()
    elif choice == "Sign Up":
        signup_function()
    elif choice == "Forgot Password":
        forget_password_function()
    elif choice == "Admin View":
        admin_view_function()

else:
    # When logged in, navigate between Welcome and Dashboard based on session state
    if st.session_state.current_page == "Welcome":
        welcome_function()
    elif st.session_state.current_page == "Dashboard":
        vibration_monitoring_function()

    # Show logout in sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        for key in ["logged_in", "user_email", "current_page"]:
            st.session_state[key] = False if key == "logged_in" else ""
        st.rerun()

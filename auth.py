import pandas as pd
import os

EXCEL_FILE = "users.xlsx"

def init_user_data():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=["email", "password"])
        df.to_excel(EXCEL_FILE, index=False)

def read_users():
    return pd.read_excel(EXCEL_FILE)

def save_user(email, password):
    df = read_users()
    if email in df["email"].values:
        return False
    df = df.append({"email": email, "password": password}, ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)
    return True

def check_login(email, password):
    df = read_users()
    return ((df["email"] == email) & (df["password"] == password)).any()

def get_password(email):
    df = read_users()
    user = df[df["email"] == email]
    if not user.empty:
        return user.iloc[0]["password"]
    return None

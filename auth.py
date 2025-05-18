import sqlite3
from database import create_connection
from email_utils import send_password_email

def signup_user(email, password):
    if not email.endswith("@hpcl.in"):
        return False, "Only @hpcl.in email addresses are allowed."

    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        return True, "Signup successful"
    except sqlite3.IntegrityError:
        return False, "User already exists."
    finally:
        conn.close()

def login_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def reset_password(email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        send_password_email(email, user[2])
        return True, "Password sent to your email."
    else:
        return False, "Email not found."

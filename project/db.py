import sqlite3

def create_users_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    password TEXT
                )''')
    conn.commit()
    conn.close()

def add_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()
    conn.close()

def get_user(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    data = c.fetchone()
    conn.close()
    return data

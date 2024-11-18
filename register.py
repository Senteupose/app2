import streamlit as st
import sqlite3

# Database connection
def create_connection():
    conn = sqlite3.connect("https://sqlfiddle.com/sqlite/online-compiler?id=50cfbd42-4451-4517-a4e8-13fdeea5b29d")  # Replace 'app.db' with your database file
    return conn

# Function to create users table if it doesn't exist
def create_users_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Function to add a user to the database
def add_user(username, email, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Ensure the users table is created
create_users_table()

# Streamlit Registration Page
st.title("Register Page")

# Registration form
with st.form("register_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit = st.form_submit_button("Register")

if submit:
    if password == confirm_password:
        if add_user(username, email, password):
            st.success("Registered successfully!")
        else:
            st.error("Username or email already exists. Please try again.")
    else:
        st.error("Passwords do not match!")


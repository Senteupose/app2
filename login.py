import streamlit as st
import sqlite3

# Database connection
def create_connection():
    conn = sqlite3.connect("app.db")  # Replace 'app.db' with your database file
    return conn

def validate_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    # Query to check user credentials
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Streamlit Login Page
st.title("Login Page")

# Login form
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    user = validate_user(username, password)
    if user:
        st.success("Logged in successfully!")
        st.write("Redirecting to trackprogress page...")
        # Redirect logic or session state (Streamlit-specific)
        st.experimental_set_query_params(page="trackprogress")
    else:
        st.error("Invalid username or password.")


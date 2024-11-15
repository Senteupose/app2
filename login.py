import streamlit as st

st.title("Login Page")

# Login form
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    st.success("Logged in successfully!")

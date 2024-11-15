import streamlit as st

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
        st.success("Registered successfully!")
    else:
        st.error("Passwords do not match!")

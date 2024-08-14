import streamlit as st
import pandas as pd
import os
import hashlib

# File to store user credentials
USER_DATA_FILE = 'user_data.csv'

def hash_password(password):
    """Hash a password with SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_user_data():
    """Load user data from the CSV file."""
    if os.path.exists(USER_DATA_FILE):
        return pd.read_csv(USER_DATA_FILE)
    else:
        return pd.DataFrame(columns=['username', 'password'])

def save_user_data(user_data):
    """Save user data to the CSV file."""
    user_data.to_csv(USER_DATA_FILE, index=False)

def signup():
    """User signup function."""
    st.subheader("Sign Up")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match!")
            return
        
        user_data = load_user_data()
        
        if username in user_data['username'].values:
            st.error("Username already exists!")
        else:
            user_data = user_data.append({'username': username, 'password': hash_password(password)}, ignore_index=True)
            save_user_data(user_data)
            st.success("Signup successful! Please log in.")

def login():
    """User login function."""
    st.subheader("Log In")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Log In"):
        user_data = load_user_data()
        
        if username not in user_data['username'].values:
            st.error("Username does not exist!")
        else:
            stored_password = user_data[user_data['username'] == username]['password'].values[0]
            if hash_password(password) == stored_password:
                st.success("Logged in successfully!")
            else:
                st.error("Incorrect password!")

def main():
    """Main function to switch between login and signup."""
    st.title("Login and Signup System")

    choice = st.sidebar.selectbox("Select a page", ["Login", "Sign Up"])

    if choice == "Sign Up":
        signup()
    else:
        login()

if __name__ == "__main__":
    main()

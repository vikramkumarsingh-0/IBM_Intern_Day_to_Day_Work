import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid
import pandas as pd
import os
import hashlib

# File to store user credentials and email verification data
user_data2_FILE = 'user_data2.csv'
email_verification2_FILE = 'email_verification2.csv'

def hash_password(password):
    """Hash a password with SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def send_verification_email(email, token):
    """Send an email with a verification link."""
    sender_email = "mohitkmourya@gmail.com"
    sender_password = "gavo mgvo eqyf joke"
    
    # Create the email content
    subject = "Email Verification"
    body = f"Please verify your email by clicking the following link:\nhttp://localhost:8501/verify?token={token}"
    
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to secure
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        st.success("Verification email sent! Please check your inbox.")
    except Exception as e:
        st.error(f"Error sending email: {e}")

def safe_read_csv(file_path):
    """Read CSV file safely with error handling."""
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            st.warning(f"The file {file_path} is empty.")
            return pd.DataFrame(columns=['username', 'email', 'password', 'verified'])
        return df
    except pd.errors.EmptyDataError:
        st.error(f"EmptyDataError: No columns to parse from file {file_path}.")
        return pd.DataFrame(columns=['username', 'email', 'password', 'verified'])
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame(columns=['username', 'email', 'password', 'verified'])

def load_user_data2():
    """Load user data from the CSV file."""
    return safe_read_csv(user_data2_FILE)

def save_user_data2(user_data2):
    """Save user data to the CSV file."""
    user_data2.to_csv(user_data2_FILE, index=False)

def load_verification_data():
    """Load email verification tokens."""
    return safe_read_csv(email_verification2_FILE)

def save_verification_data(verification_data):
    """Save email verification tokens."""
    verification_data.to_csv(email_verification2_FILE, index=False)

def signup():
    """User signup function."""
    st.subheader("Sign Up")

    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match!")
            return
        
        user_data2 = load_user_data2()
        if username in user_data2['username'].values:
            st.error("Username already exists!")
        elif email in user_data2['email'].values:
            st.error("Email already registered!")
        else:
            token = str(uuid.uuid4())
            user_data2 = user_data2._append({'username': username, 'email': email, 'password': hash_password(password), 'verified': False}, ignore_index=True)
            save_user_data2(user_data2)
            
            verification_data = load_verification_data()
            verification_data = verification_data._append({'email': email, 'token': token}, ignore_index=True)
            save_verification_data(verification_data)
            
            send_verification_email(email, token)

def verify_email(token):
    """Verify email using the token."""
    verification_data = load_verification_data()
    if token in verification_data['token'].values:
        email = verification_data[verification_data['token'] == token]['email'].values[0]
        
        user_data2 = load_user_data2()
        if email in user_data2['email'].values:
            user_data2.loc[user_data2['email'] == email, 'verified'] = True
            save_user_data2(user_data2)
        
        verification_data = verification_data[verification_data['token'] != token]
        save_verification_data(verification_data)
        
        st.success("Email verified successfully! You can now log in.")
    else:
        st.error("Invalid or expired verification token.")

def login():
    """User login function."""
    st.subheader("Log In")

    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    if st.button("Log In"):
        user_data2 = load_user_data2()
        
        if email not in user_data2['email'].values:
            st.error("Email does not exist!")
        else:
            user_row = user_data2[user_data2['email'] == email]
            if user_row.empty:
                st.error("Email does not exist!")
            else:
                if user_row['password'].values[0] != hash_password(password):
                    st.error("Incorrect password!")
                elif not user_row['verified'].values[0]:
                    st.error("Email not verified. Please check your email for the verification link.")
                else:
                    st.success("Logged in successfully!")

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

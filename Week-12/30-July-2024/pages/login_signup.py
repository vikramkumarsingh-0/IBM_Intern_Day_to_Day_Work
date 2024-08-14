import streamlit as st
import pandas as pd
import os
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid

# File to store user credentials
user_data1_FILE = 'user_data1.csv'
EMAIL_VERIFICATION_FILE = 'email_verification.csv'

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
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        st.success("Verification email sent! Please check your inbox.")
    except Exception as e:
        st.error(f"Error sending email: {e}")

def load_user_data1():
    """Load user data from the CSV file."""
    if os.path.exists(user_data1_FILE):
        return pd.read_csv(user_data1_FILE)
    else:
        # Initialize DataFrame with required columns if the file does not exist
        return pd.DataFrame(columns=['username', 'email', 'password', 'verified'])

def save_user_data1(user_data1):
    """Save user data to the CSV file."""
    user_data1.to_csv(user_data1_FILE, index=False)

def load_verification_data():
    """Load email verification tokens."""
    if os.path.exists(EMAIL_VERIFICATION_FILE):
        return pd.read_csv(EMAIL_VERIFICATION_FILE)
    else:
        # Initialize DataFrame with required columns if the file does not exist
        return pd.DataFrame(columns=['email', 'token'])

def save_verification_data(verification_data):
    """Save email verification tokens."""
    verification_data.to_csv(EMAIL_VERIFICATION_FILE, index=False)

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
        
        user_data1 = load_user_data1()
        if username in user_data1['username'].values:
            st.error("Username already exists!")
        elif email in user_data1['email'].values:
            st.error("Email already registered!")
        else:
            token = str(uuid.uuid4())
            user_data1 = user_data1._append({'username': username, 'email': email, 'password': hash_password(password), 'verified': False}, ignore_index=True)
            save_user_data1(user_data1)
            
            verification_data = load_verification_data()
            verification_data = verification_data._append({'email': email, 'token': token}, ignore_index=True)
            save_verification_data(verification_data)
            
            send_verification_email(email, token)

def verify_email(token):
    """Verify email using the token."""
    verification_data = load_verification_data()
    if token in verification_data['token'].values:
        email = verification_data[verification_data['token'] == token]['email'].values[0]
        
        user_data1 = load_user_data1()
        if email in user_data1['email'].values:
            user_data1.loc[user_data1['email'] == email, 'verified'] = True
            save_user_data1(user_data1)
        
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
        user_data1 = load_user_data1()
        
        if email not in user_data1['email'].values:
            st.error("Email does not exist!")
        else:
            user_row = user_data1[user_data1['email'] == email]
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
    token = str(uuid.uuid4())
    send_verification_email("recipient@example.com", token)
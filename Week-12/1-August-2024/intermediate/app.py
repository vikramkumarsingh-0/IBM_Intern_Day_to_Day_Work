import streamlit as st
import sqlite3 as sq
import pandas as pd
import tempfile
# df = pd.read_csv("users.csv")


conn = sq.connect("users.db")
c = conn.cursor()
c.execute("CREATE TABLE if not exists users(Name TEXT, UserName TEXT, Password PASSWORD, Email EMAIL)")

#Validate
st.title("My Form")
with st.form("User Registration"):
    name = st.text_input("Enter Name")
    mail = st.text_input("Enter Mail")
    uname = st.text_input("Username")
    passw = st.text_input("Password", type="password")
    c_pass = st.text_input("Re-Type Password", type="password")
    reg = st.form_submit_button("Register")
    r_but = st.form_submit_button("Show Profile")


if r_but:
    c.execute("SELECT * FROM users")
    data = c.fetchall()
    st.write(data)

if reg:
    if name != ""  and mail != "" and uname != "" and passw != "" and passw == c_pass:
        st.success("Registraion Successful" + " " + uname)
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (name, mail, uname, passw))
        conn.commit()
        st.balloons()
    else:
        st.warning("Please Check the form and fill correctly.")
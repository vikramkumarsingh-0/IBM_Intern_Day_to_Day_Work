import streamlit as st
import sqlite3 as sq
import pandas as pd
# df = pd.read_csv("users.csv")


conn = sq.connect("users.db")
c = conn.cursor()
c.execute("CREATE TABLE if not exists users(username TEXT, password PASSWORD, email EMAIL)")

#Validate
st.title("My Form")
with st.form("User Registration"):
    uname = st.text_input("Username")
    passw = st.text_input("Password", type="password")
    c_pass = st.text_input("Re-Type Password", type="password")
    mail = st.text_input("Mail")
    but = st.form_submit_button("Submit")
    r_but = st.form_submit_button("read")


if r_but:
    c.execute("SELECT * FROM users")
    data = c.fetchall()
    st.write(data)

if but:
    if uname != "" and mail != "" and passw != "" and passw == c_pass:
        st.success("Registraion Successful" + " " + uname)
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (uname, passw, mail))
        conn.commit()
        st.balloons()
    else:
        st.error("Please Check Details.")
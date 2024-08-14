import pandas as pd
import streamlit as st
import joblib

model = joblib.load('mj')

st.title("House Price Prediction")

area = st.number_input("Enter the Area")
bedroom = st.number_input("Enter the Bedroom")


def prediction(area):
    p = model.predict([[area]])
    return p


if(st.button("Predict")):
    result = prediction(area)
    st.success("The House Price is {}".format(result))
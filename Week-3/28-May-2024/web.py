import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import pillow as pil

st.title('My DA/ML web App')
# st.subheader('Data Set')
st.success('Data Set')

# a = st.text_input('Name')

df = pd.read_csv('sales.csv')
# st.dataframe(df)

fig = plt.figure()
plt.plot(df)
st.pyplot(fig)
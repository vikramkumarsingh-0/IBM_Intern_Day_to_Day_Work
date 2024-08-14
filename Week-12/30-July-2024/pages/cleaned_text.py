import streamlit as st

def clean_text(text):
    text = text.replace("`", "").replace("-\n", "").replace("\n\n", "&&***&&").replace("\n", "").replace("&&***&&", "\n\n").strip()
    return (text)


st.title("Intro to Layouts and Images")
st.sidebar.image("logos\smlogo.jpg", caption="Smlogo")
st.sidebar.header("Options")
text = st.sidebar.text_area("Paste Text Here")
button1 = st.sidebar.button("Clean Text")
if button1: 
    col1, col2 = st.columns(2)
    col1_expander = col1.expander("Expand Original")
    with col1_expander:
        col1_expander.header("Original Text")
        col1_expander.write(text)

    col2_expander = col2.expander("Expand Cleaned")
    with col2_expander:
        col2_expander.header("Cleaned Text")
        col2_expander.write(text)
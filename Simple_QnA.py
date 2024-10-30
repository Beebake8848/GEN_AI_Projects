import streamlit as st

import google.generativeai as genai
from api_key import api_key

genai.configure(api_key=api_key)

def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

##initialize our streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini Application")

input=st.text_input("Input: ",key="input")
submit=st.button("Ask the question")

## If ask button is clicked

if submit:
    response=get_gemini_response(input)
    st.write(response)
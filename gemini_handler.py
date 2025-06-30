import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-pro")

def generate_with_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

# === gemini_handler.py ===
import streamlit as st
import google.generativeai as genai

# Streamlit Cloud'dan gelen gizli API anahtarı
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Gemini 1.5 Flash modeli
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def generate_with_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader

# Load .env and configure API
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Use a valid model name
MODEL_NAME = "models/gemini-1.5-flash"

# Function to summarize text using Gemini
def summarize_text(text):
    model = genai.GenerativeModel(MODEL_NAME)
    prompt = f"Summarize the following document:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.set_page_config(page_title="Gemini Document Summarizer")
st.title("📄 Document LLM Summarizer")
st.markdown("Upload a PDF or text file to summarize it using Gemini.")

uploaded_file = st.file_uploader("Upload file", type=["pdf", "txt"])

if uploaded_file:
    if uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    else:
        st.error("Unsupported file type.")
        st.stop()

    with st.spinner("Generating summary..."):
        try:
            summary = summarize_text(text)
            st.subheader("📝 Summary:")
            st.success(summary)
        except Exception as e:
            st.error(f"Error: {str(e)}")

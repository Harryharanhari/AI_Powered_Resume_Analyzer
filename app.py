import streamlit as st
from utils import extract_text_from_pdf, extract_text_from_docx, analyze_resume

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Powered Resume Analyzer")
st.write("Upload your resume and get AI feedback!")

# API Key input
api_key = st.secrets["GROQ_API_KEY"]

uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

if uploaded_file and api_key:

    # Extract text
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_docx(uploaded_file)

    st.success("Resume uploaded successfully!")

    if st.button("Analyze Resume"):

        with st.spinner("Analyzing..."):
            result = analyze_resume(text, api_key)

        st.subheader("📊 Analysis Result")
        st.write(result)

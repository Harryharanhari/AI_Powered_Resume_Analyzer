import streamlit as st
import PyPDF2
import docx
from groq import Groq

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Powered Resume Analyzer")
st.write("Upload your resume and get AI feedback!")

# ---------------- API KEY ----------------
# Use secrets if available, otherwise input box
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = st.text_input("Enter Groq API Key", type="password")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

# ---------------- TEXT EXTRACTION ----------------
def extract_text(file):
    text = ""

    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text

# ---------------- AI ANALYSIS ----------------
def analyze_resume(text, api_key):
    client = Groq(api_key=api_key)

    # LIMIT TEXT SIZE (prevents token errors)
    text = text[:6000]

    prompt = f"""
    You are a professional resume reviewer.

    Analyze this resume and provide:

    1. Overall Score (out of 10)
    2. Strengths
    3. Weaknesses
    4. Suggestions to improve
    5. Missing skills for Data Science/AI roles

    Resume:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content

# ---------------- MAIN LOGIC ----------------
if uploaded_file and api_key:

    text = extract_text(uploaded_file)

    if not text.strip():
        st.error("❌ Could not extract text from file.")
    else:
        st.success("✅ Resume uploaded successfully!")

        if st.button("Analyze Resume"):
            with st.spinner("Analyzing..."):

                try:
                    result = analyze_resume(text, api_key)

                    st.subheader("📊 Analysis Result")
                    st.write(result)

                except Exception as e:
                    st.error(f"❌ Error: {e}")

elif uploaded_file and not api_key:
    st.warning("⚠️ Please enter your Groq API Key")

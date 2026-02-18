import streamlit as st
import PyPDF2
import docx
from groq import Groq
import json
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer (ATS Style)")
st.caption("Hybrid ATS scoring + AI feedback")

# ---------------- API KEY ----------------
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

    else:
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text


# ---------------- REAL ATS SCORING ----------------
def rule_based_scoring(text):
    text_lower = text.lower()

    keywords = [
        "python","machine learning","deep learning","nlp",
        "sql","pandas","numpy","tensorflow","pytorch",
        "power bi","tableau","data analysis","statistics",
        "scikit-learn","ai","data science"
    ]

    keyword_score = sum(1 for k in keywords if k in text_lower)

    numbers = len(re.findall(r"\d+%", text))
    projects = text_lower.count("project")

    education = 5 if any(word in text_lower for word in 
                         ["b.tech","m.tech","bsc","msc","degree"]) else 0

    score = (
        min(keyword_score*3, 30) +
        min(numbers*2, 20) +
        min(projects*5, 20) +
        education +
        10
    )

    return min(score,100)


# ---------------- AI FEEDBACK ----------------
def ai_feedback(text, api_key):
    client = Groq(api_key=api_key)

    text = text[:5000]

    prompt = f"""
You are a professional resume reviewer.

Give ONLY JSON.

Provide:
strengths (list of 3-5)
weaknesses (list of 3-5)
suggestions (list of 3-5)

Resume:
{text}

Format:
{{
 "strengths": ["..."],
 "weaknesses": ["..."],
 "suggestions": ["..."]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content


# ---------------- MAIN ----------------
if uploaded_file and api_key:

    text = extract_text(uploaded_file)

    if not text.strip():
        st.error("❌ Could not extract text.")
    else:
        st.success("✅ Resume uploaded")

        if st.button("Analyze Resume"):

            with st.spinner("Analyzing..."):

                # -------- REAL SCORE --------
                score = rule_based_scoring(text)

                st.subheader("🎯 ATS Score")
                st.metric("Overall Score", f"{score}/100")
                st.progress(score/100)

                # -------- CATEGORY BARS --------
                st.subheader("📊 Score Breakdown")

                bars = {
                    "Keyword Match": min(score,30),
                    "Projects": min(text.lower().count("project")*5,20),
                    "Achievements": min(len(re.findall(r"\d+%", text))*2,20),
                    "Education": 10 if "b.tech" in text.lower() else 5,
                    "Formatting": 10
                }

                st.bar_chart(bars)

                # -------- AI FEEDBACK --------
                try:
                    result = ai_feedback(text, api_key)
                    data = json.loads(result)

                    st.subheader("✅ Strengths")
                    for s in data["strengths"]:
                        st.write("✔️", s)

                    st.subheader("⚠️ Weaknesses")
                    for w in data["weaknesses"]:
                        st.write("❌", w)

                    st.subheader("🚀 Suggestions")
                    for sug in data["suggestions"]:
                        st.write("💡", sug)

                except:
                    st.warning("AI feedback parsing issue. Try again.")

elif uploaded_file and not api_key:
    st.warning("Enter API key")

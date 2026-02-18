import streamlit as st
import PyPDF2
import docx
from groq import Groq
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer (ATS Style)")
st.caption("Recruiter-style AI resume evaluation")

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


# ---------------- AI ANALYSIS ----------------
def analyze_resume(text, api_key):
    client = Groq(api_key=api_key)

    text = text[:6000]

    prompt = f"""
You are an ATS system.

Score the resume strictly.

Return ONLY valid JSON.

Scoring (Total 100):
skills (0-25)
projects (0-20)
education (0-15)
format (0-10)
impact (0-15)
ats (0-15)

Also include:
strengths
weaknesses
suggestions

Resume:
{text}

Return format:

{{
 "skills": 20,
 "projects": 15,
 "education": 10,
 "format": 8,
 "impact": 12,
 "ats": 10,
 "strengths": ["..."],
 "weaknesses": ["..."],
 "suggestions": ["..."]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
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

                try:
                    result = analyze_resume(text, api_key)

                    data = json.loads(result)

                    total_score = (
                        data["skills"]
                        + data["projects"]
                        + data["education"]
                        + data["format"]
                        + data["impact"]
                        + data["ats"]
                    )

                    # ---------- TOP SCORE ----------
                    st.subheader("🎯 Overall ATS Score")
                    st.metric("Total Score", f"{total_score}/100")

                    st.progress(total_score / 100)

                    # ---------- SCORE BARS ----------
                    st.subheader("📊 Section Scores")

                    scores = {
                        "Skills": data["skills"],
                        "Projects": data["projects"],
                        "Education": data["education"],
                        "Format": data["format"],
                        "Impact": data["impact"],
                        "ATS Keywords": data["ats"],
                    }

                    st.bar_chart(scores)

                    # ---------- FEEDBACK ----------
                    st.subheader("✅ Strengths")
                    for s in data["strengths"]:
                        st.write("✔️", s)

                    st.subheader("⚠️ Weaknesses")
                    for w in data["weaknesses"]:
                        st.write("❌", w)

                    st.subheader("🚀 Suggestions")
                    for sug in data["suggestions"]:
                        st.write("💡", sug)

                except Exception as e:
                    st.error(f"Error: {e}")

elif uploaded_file and not api_key:
    st.warning("Enter API key")

 📄 AI Resume Analyzer (Multi-Domain ATS)

An AI-powered Resume Analyzer built with **Streamlit + Groq LLaMA 3.1** that evaluates resumes like a real Applicant Tracking System (ATS).

Unlike basic resume checkers, this tool performs **domain-agnostic scoring**, meaning it works across:

- Engineering
- IT / Software
- Medical / Healthcare
- Business / Management
- Arts & Science
- General resumes

---

## 🚀 Features

### ✅ Multi-Domain ATS Scoring
- Automatically detects resume domain
- Applies domain-specific evaluation
- Produces realistic score variations

### ✅ Hybrid Scoring System
- Rule-based ATS scoring (deterministic)
- AI-powered qualitative feedback

### ✅ Visual Dashboard
- ATS Score meter
- Score breakdown charts
- Clean recruiter-style UI

### ✅ AI Feedback
- Strengths
- Weaknesses
- Suggestions for improvement

---

## 🧠 How It Works

### 1. Resume Parsing
Extracts text from:
- PDF
- DOCX

### 2. Domain Detection
Identifies whether the resume belongs to:
Tech, Core Engineering, Medical, Business, or Arts & Science.

### 3. ATS Rule-Based Scoring
Scores based on:
- Domain keyword relevance
- Projects & practical work
- Measurable achievements
- Experience mentions
- Education
- Formatting quality

### 4. AI Feedback
Uses LLaMA 3.1 via Groq API for:
- Strengths
- Weaknesses
- Suggestions

---

## 🛠 Tech Stack

- Python
- Streamlit
- Groq API (LLaMA 3.1)
- PyPDF2
- python-docx
- Regex-based NLP

---

## 📦 Installation

```bash
pip install -r requirements.txt

▶️ Run Locally
streamlit run app.py

🔑 API Key Setup

Option 1 — Input in UI
Enter Groq API key in the app.

Option 2 — Streamlit Secrets (Recommended)

GROQ_API_KEY="your_key_here"

🎯 Use Cases

Students improving resumes

Job seekers optimizing CVs

Career counselors

Recruiters pre-screening candidates

💡 Future Improvements

Resume vs Job Description matching

Skill-gap detection

Downloadable reports

Login & resume history

Advanced UI dashboard

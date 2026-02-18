import PyPDF2
import docx
from groq import Groq

# ---------- TEXT EXTRACTION ----------

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


# ---------- AI ANALYSIS ----------

def analyze_resume(text, api_key):
    client = Groq(api_key=api_key)

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

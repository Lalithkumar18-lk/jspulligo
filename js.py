import streamlit as st
import pdfplumber
import docx
import re
import spacy
from transformers import pipeline

# Load NLP models
nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

st.set_page_config(page_title="AI Resume Parser", page_icon="📄")

st.title("📄 AI Resume Parser with NLP Summary")
st.write("Upload a Resume (PDF or DOCX)")

# ----------- FILE READING FUNCTIONS -----------

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# ----------- REGEX EXTRACTION -----------

def extract_email(text):
    match = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match[0] if match else "Not Found"

def extract_phone(text):
    match = re.findall(r"\+?\d[\d\s-]{8,12}\d", text)
    return match[0] if match else "Not Found"

def extract_skills(text):
    skills_list = [
        "python", "machine learning", "deep learning", "sql",
        "excel", "power bi", "tensorflow", "pytorch",
        "nlp", "data analysis", "html", "css", "javascript"
    ]
    found_skills = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    return found_skills

def extract_education(text):
    education_keywords = ["B.Tech", "M.Tech", "Bachelor", "Master", "MBA", "PhD"]
    education = []
    for line in text.split("\n"):
        for keyword in education_keywords:
            if keyword.lower() in line.lower():
                education.append(line.strip())
    return education

def extract_experience(text):
    experience_keywords = ["experience", "worked", "intern", "project"]
    experience = []
    for line in text.split("\n"):
        for keyword in experience_keywords:
            if keyword.lower() in line.lower():
                experience.append(line.strip())
    return experience[:5]

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not Found"

# ----------- STREAMLIT UI -----------

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file:

    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    st.subheader("📌 Extracted Information")

    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    skills = extract_skills(resume_text)
    education = extract_education(resume_text)
    experience = extract_experience(resume_text)

    st.write("### 👤 Name:", name)
    st.write("### 📧 Email:", email)
    st.write("### 📱 Phone:", phone)
    st.write("### 🛠 Skills:", skills)
    st.write("### 🎓 Education:", education)
    st.write("### 💼 Experience:", experience)

    # ----------- SUMMARY USING TRANSFORMER -----------

    st.subheader("📝 Resume Summary (AI Generated)")

    if len(resume_text) > 500:
        summary = summarizer(resume_text[:1000], max_length=150, min_length=50, do_sample=False)
        st.success(summary[0]['summary_text'])
    else:
        st.info("Resume too short for summary generation.")

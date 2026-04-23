from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import spacy
import re

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
    "python","java","c++","machine learning","deep learning",
    "data science","nlp","react","node","sql","mongodb",
    "html","css","javascript","flask","fastapi","django",
    "tensorflow","pytorch","git","docker","kubernetes","aws"
]

# -------- HELPERS --------

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

# 🧠 Smart skill extraction
def extract_skills(text):
    synonyms = {
        "ml": "machine learning",
        "ai": "machine learning",
        "js": "javascript"
    }

    found = []

    for skill in SKILLS_DB:
        if skill in text:
            found.append(skill)

    for short, full in synonyms.items():
        if short in text:
            found.append(full)

    return list(set(found))

def calculate_ats_score(skills, text):
    score = min(len(skills)*5, 40)

    if 300 <= len(text.split()) <= 800:
        score += 20

    for sec in ["education","experience","projects","skills"]:
        if sec in text:
            score += 10

    return min(score, 100)

def job_match(resume_text, job_desc):
    if not job_desc:
        return 0

    resume_words = set(re.findall(r'\w+', resume_text))
    job_words = set(re.findall(r'\w+', job_desc.lower()))

    return int(len(resume_words & job_words)/len(job_words)*100) if job_words else 0

# 📊 Skill Gap
def skill_gap(resume_skills, job_desc):
    job_desc = job_desc.lower()

    matched, missing = [], []

    for skill in SKILLS_DB:
        if skill in job_desc:
            if skill in resume_skills:
                matched.append(skill)
            else:
                missing.append(skill)

    return matched, missing

# 📈 Score Breakdown
def score_breakdown(skills, text):
    return {
        "skills": min(len(skills)*5, 40),
        "structure": 20 if "experience" in text else 10,
        "keywords": 20 if len(skills) > 5 else 10,
        "formatting": 20 if "projects" in text else 10
    }

# 💼 Job Recommendation
def recommend_jobs(skills):
    if "machine learning" in skills:
        return ["ML Engineer","Data Scientist"]
    if "react" in skills:
        return ["Frontend Developer"]
    if "python" in skills:
        return ["Backend Developer","Data Analyst"]
    return ["Software Developer"]

# 🤖 Feedback
def generate_feedback(ats_score, match_score):
    fb = []

    if ats_score < 60:
        fb.append("Improve structure and add more relevant content.")
    elif ats_score < 80:
        fb.append("Good resume, but optimize keywords and formatting.")
    else:
        fb.append("Excellent resume!")

    if match_score < 50:
        fb.append("Add job-specific keywords.")
    else:
        fb.append("Strong job match.")

    return fb

# -------- ROUTES --------

@app.get("/")
def home():
    return {"message": "API Running 🚀"}

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form("")
):
    try:
        text = extract_text_from_pdf(file.file)

        skills = extract_skills(text)
        ats_score = calculate_ats_score(skills, text)
        match_score = job_match(text, job_description)

        matched, missing = skill_gap(skills, job_description)
        breakdown = score_breakdown(skills, text)
        jobs = recommend_jobs(skills)
        feedback = generate_feedback(ats_score, match_score)

        return {
            "ats_score": ats_score,
            "skills_found": skills,
            "job_match_score": match_score,
            "matched_skills": matched,
            "missing_skills": missing,
            "score_breakdown": breakdown,
            "job_recommendations": jobs,
            "feedback": feedback
        }

    except Exception as e:
        return {"error": str(e)}
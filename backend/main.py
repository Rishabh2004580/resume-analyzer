from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUIRED_SKILLS = ["python", "sql", "machine learning", "data analysis", "excel"]


def build_mandatory_changes(missing_skills):
    changes = []

    for skill in missing_skills:
        changes.append(
            f"Add '{skill}' with a real project or job achievement (not just a keyword list)."
        )

    changes.append("Add measurable impact (numbers like %, $, time saved) in at least 3 bullet points.")
    changes.append("Tailor your summary and top skills to the exact job description before applying.")
    changes.append("Use ATS-friendly headings: Summary, Skills, Experience, Projects, Education.")

    # Keep output concise and focused on the most impactful fixes.
    return changes[:6]


def build_job_advice(score, found_skills, missing_skills):
    advice = []

    if score >= 80:
        advice.append("You are close to interview-ready. Focus on role-specific achievements and portfolio links.")
    elif score >= 60:
        advice.append("You have a solid base. Fill missing skills and add stronger project outcomes.")
    else:
        advice.append("Your resume needs core upgrades before broad applications. Prioritize missing must-have skills first.")

    if "python" in found_skills and "sql" in found_skills:
        advice.append("Good fit for Data Analyst / Junior Data Scientist tracks.")

    if "machine learning" in missing_skills:
        advice.append("If targeting ML roles, add one end-to-end ML project with deployment or business impact.")

    if "excel" in missing_skills:
        advice.append("For analyst roles, include Excel evidence (pivot tables, lookups, dashboards, automation).")

    advice.append("Customize resume keywords for each job posting and keep resume to 1 page if you are early career.")
    return advice[:5]


def compute_score_and_breakdown(text, found_skills):
    # Weighted heuristic:
    # - Skills: 60% (based on REQUIRED_SKILLS found)
    # - Experience indicators: up to 15%
    # - Achievements / numbers: up to 15%
    # - Projects / portfolio: up to 5%
    # - Education signals: up to 5%

    max_skills_weight = 60
    max_experience = 15
    max_achievements = 15
    max_projects = 5
    max_education = 5

    # Skills score
    skills_score = 0
    if REQUIRED_SKILLS:
        skills_score = (len(found_skills) / len(REQUIRED_SKILLS)) * max_skills_weight

    # Experience detection: look for 'years', 'experience', 'worked at', 'intern'
    exp_signals = 0
    if re.search(r"\b\d+\s+years?\b", text):
        exp_signals += 1
    if re.search(r"\bexperience\b", text):
        exp_signals += 1
    if re.search(r"\bworked at\b|\bintern\b|\bcontractor\b", text):
        exp_signals += 1

    experience_score = min(max_experience, (exp_signals / 3) * max_experience)

    # Achievements detection: look for percentages, $, numbers with improvements words
    ach_signals = 0
    if re.search(r"\b\d+%\b|\bpercent\b", text):
        ach_signals += 1
    if re.search(r"\$\d+|\b\d+k\b", text):
        ach_signals += 1
    if re.search(r"\bimprov|reduci|increas|decreas|boost|saved\b", text):
        ach_signals += 1

    achievements_score = min(max_achievements, (ach_signals / 3) * max_achievements)

    # Projects / portfolio
    proj_signals = 0
    if re.search(r"\bproject\b", text):
        proj_signals += 1
    if re.search(r"\bgithub\b|\bportfolio\b|\bdeployed\b", text):
        proj_signals += 1

    projects_score = min(max_projects, (proj_signals / 2) * max_projects)

    # Education signals
    edu_signals = 0
    if re.search(r"\bbachelor\b|\bmaster\b|\bb\.sc\b|\bm\.sc\b|\bdegree\b", text):
        edu_signals += 1

    education_score = min(max_education, (edu_signals / 1) * max_education)

    total = skills_score + experience_score + achievements_score + projects_score + education_score
    # Normalize just in case
    total = max(0, min(100, total))

    breakdown = {
        "skills": round(skills_score, 1),
        "experience": round(experience_score, 1),
        "achievements": round(achievements_score, 1),
        "projects": round(projects_score, 1),
        "education": round(education_score, 1),
        "total": int(round(total)),
    }

    return breakdown

@app.get("/")
def home():
    return {"message": "API is working"}

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    text = text.lower()

    found_skills = [skill for skill in REQUIRED_SKILLS if skill in text]
    missing_skills = [skill for skill in REQUIRED_SKILLS if skill not in text]

    # compute improved score breakdown
    breakdown = compute_score_and_breakdown(text, found_skills)
    score = breakdown.get("total", 0)
    mandatory_changes = build_mandatory_changes(missing_skills)
    job_advice = build_job_advice(score, found_skills, missing_skills)

    return {
        "score": score,
        "score_breakdown": breakdown,
        "found_skills": found_skills,
        "missing_skills": missing_skills,
        "mandatory_changes": mandatory_changes,
        "job_advice": job_advice,
        "suggestions": "Prioritize missing skills, quantify your impact, and tailor your resume for each target role."
    }

from fastapi import FastAPI, UploadFile, File
import pdfplumber

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUIRED_SKILLS = ["python", "sql", "machine learning", "data analysis", "excel"]

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

    score = int((len(found_skills) / len(REQUIRED_SKILLS)) * 100)

    return {
        "score": score,
        "found_skills": found_skills,
        "missing_skills": missing_skills,
        "suggestions": "Add missing skills to improve your resume."
    }
# resume-analyzer
link "[resume-analyzer-flame-pi.vercel.app](https://resume-analyzer-flame-pi.vercel.app/)"
# 📄 AI Resume Analyzer (Full-Stack Web Application)

## 🚀 Project Overview

AI Resume Analyzer is a full-stack web application that analyzes resumes and provides insights based on required skills. It helps users understand their strengths, missing skills, and suggestions to improve their resume for better job opportunities.

---

## 🌐 Live Application

👉 https://resume-analyzer-flame-pi.vercel.app/

---

## 📂 GitHub Repository

👉 (Paste your GitHub repo link here)

---

## 🎯 Features

### 📄 Resume Upload

* Upload PDF resumes
* Supports text-based PDF files

### 🤖 AI-Based Analysis

* Detects key skills in resume
* Compares with required skills

### 📊 Results Display

* Resume score (%)
* Found skills
* Missing skills
* Suggestions for improvement

### 💡 Smart Suggestions

* Helps improve resume quality
* Provides actionable feedback

---

## 🛠️ Tech Stack

### Frontend(ai)

* HTML
* CSS
* JavaScript

### Backend

* Python (FastAPI)

### Libraries Used

* pdfplumber (PDF text extraction)

---

## ⚙️ How It Works

1. User uploads resume (PDF)
2. Backend extracts text using pdfplumber
3. Skills are matched with predefined list
4. Score is calculated
5. Results are displayed on UI

---

## 🧪 API Endpoint
link  https://resume-analyzer-5-y1g2.onrender.com  ##check backend also

### POST /analyze

* Upload resume file
* Returns:

  * score
  * found_skills
  * missing_skills
  * suggestions

---

## 📦 Run Locally

### 1. Clone repository

```
git clone <your-repo-link>
```

### 2. Navigate to project

```
cd resume-analyzer
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run backend

```
python -m uvicorn main:app --reload
```

### 5. Open frontend

Open `index.html` in browser

---

## ⚠️ Limitations

* Works best with text-based PDFs
* Scanned/image resumes may not be analyzed correctly

---


## 👨‍💻 Author

Rishabh Jain

---


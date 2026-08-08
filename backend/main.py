import os
import sqlite3
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

DB = "career_compass.db"
app = FastAPI(title="CareerCompass AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CAREERS = {
    "Full Stack Developer": {
        "skills": ["HTML","CSS","JavaScript","React","Node.js","SQL","Git","REST API"],
        "projects": ["Job application tracker","E-commerce application","AI-powered dashboard"]
    },
    "Python Backend Developer": {
        "skills": ["Python","FastAPI","SQL","REST API","Git","Testing","Docker"],
        "projects": ["FastAPI job portal API","REST API with authentication","Data analytics API"]
    },
    "AI/ML Engineer": {
        "skills": ["Python","NumPy","Pandas","Machine Learning","SQL","Git","APIs"],
        "projects": ["Student performance predictor","Recommendation system","AI resume analyzer"]
    },
    "Frontend Developer": {
        "skills": ["HTML","CSS","JavaScript","React","Git","REST API"],
        "projects": ["Responsive portfolio","Productivity dashboard","Accessible job-search UI"]
    }
}

JOBS = [
    {"id":1,"title":"Frontend Developer Intern","company":"SampleTech","mode":"Remote","skills":["HTML","CSS","JavaScript","React"],"type":"Internship"},
    {"id":2,"title":"Python Backend Intern","company":"CloudWorks","mode":"Remote","skills":["Python","FastAPI","SQL","Git"],"type":"Internship"},
    {"id":3,"title":"Full Stack Developer Intern","company":"BuildLabs","mode":"Hybrid","skills":["React","Node.js","SQL","REST API","Git"],"type":"Internship"},
    {"id":4,"title":"Junior AI Developer","company":"FutureAI","mode":"Remote","skills":["Python","Machine Learning","APIs","SQL"],"type":"Entry-level"}
]

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = db()
    c.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            status TEXT NOT NULL,
            link TEXT DEFAULT ''
        )
    """)
    c.commit()
    c.close()

init_db()

class Profile(BaseModel):
    education: str = ""
    skills: List[str] = []
    interests: List[str] = []
    target_role: Optional[str] = None

class ResumeRequest(BaseModel):
    resume: str

class InterviewRequest(BaseModel):
    role: str
    level: str = "Entry-level"
    count: int = 5

class AdviceRequest(BaseModel):
    message: str

class Application(BaseModel):
    title: str
    company: str
    status: str = "Applied"
    link: str = ""

def normalize(items):
    return {x.strip().lower() for x in items if x.strip()}

def analyze(profile):
    user = normalize(profile.skills)
    matches = []
    for role, data in CAREERS.items():
        required = normalize(data["skills"])
        matched = sorted(user & required)
        missing = sorted(required - user)
        score = round(len(matched) / len(required) * 100)
        matches.append({
            "role": role,
            "score": score,
            "matched": matched,
            "missing": missing,
            "projects": data["projects"]
        })
    matches.sort(key=lambda x: x["score"], reverse=True)
    best = matches[0]
    gaps = best["missing"]
    roadmap = [
        f"Week 1: Strengthen {gaps[0] if gaps else 'your core skills'}.",
        f"Week 2: Build a practical {best['role']} project.",
        "Week 3: Add testing, GitHub documentation and deployment.",
        "Week 4: Improve your resume and apply to targeted roles."
    ]
    return {
        "readiness_score": best["score"],
        "recommended_role": best["role"],
        "matched_skills": best["matched"],
        "skill_gaps": gaps,
        "project_ideas": best["projects"],
        "roadmap": roadmap,
        "career_matches": matches
    }

@app.get("/")
def root():
    return {"service":"CareerCompass AI","status":"online"}

@app.get("/api/health")
def health():
    return {"status":"healthy"}

@app.post("/api/profile/analyze")
def profile_analyze(profile: Profile):
    return analyze(profile)

@app.post("/api/resume/analyze")
def resume_analyze(request: ResumeRequest):
    text = request.resume.lower()
    keywords = ["python","java","javascript","typescript","react","node.js",
                "fastapi","sql","git","github","api","machine learning",
                "project","internship","communication"]
    found = [x for x in keywords if x in text]
    missing = [x for x in keywords if x not in text]
    return {
        "score": min(100, 35 + len(found)*5),
        "detected_skills": found,
        "possible_missing_keywords": missing[:8],
        "suggestions": [
            "Add 2–3 project bullets with measurable results.",
            "Include GitHub or deployed-project links.",
            "Tailor your skills to each job description.",
            "Use action verbs and keep the resume concise."
        ]
    }

@app.post("/api/interview")
def interview(request: InterviewRequest):
    questions = {
        "Full Stack Developer": [
            "Explain how a React frontend communicates with a backend API.",
            "What is REST and how would you design a simple API?",
            "How would you debug a slow web application?",
            "Explain SQL joins with an example.",
            "Describe a project you built and one difficult problem you solved."
        ],
        "Python Backend Developer": [
            "What is the difference between a list, tuple and set in Python?",
            "How would you design a FastAPI endpoint?",
            "What is database indexing?",
            "How would you test an API?",
            "How would you secure an authentication endpoint?"
        ],
        "AI/ML Engineer": [
            "Explain supervised vs unsupervised learning.",
            "What is overfitting and how can you reduce it?",
            "How would you evaluate a classification model?",
            "How can an AI application use an external API?",
            "Explain one machine-learning project you have built."
        ],
        "Frontend Developer": [
            "What is the difference between state and props in React?",
            "How does responsive design work?",
            "What is the DOM?",
            "How would you improve website performance?",
            "Explain a frontend project you built."
        ]
    }
    return {"role":request.role,"questions":questions.get(request.role, questions["Full Stack Developer"])[:5]}

@app.post("/api/ai-advice")
def advice(request: AdviceRequest):
    key = os.getenv("OPENAI_API_KEY")
    if not key or key == "your_api_key_here":
        return {"reply":
            "30-day plan: choose one target role, close your top 2 skill gaps, "
            "build two practical projects, publish them on GitHub, improve your "
            "resume around those projects, practice interviews, and apply to "
            "targeted internships every week. Never rely only on mass applications."
        }
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":
                 "You are CareerCompass AI. Give practical career advice to "
                 "students and fresh graduates. Focus on skills, projects, "
                 "resumes and interviews. Never guarantee employment."},
                {"role":"user","content":request.message}
            ],
            temperature=0.5
        )
        return {"reply":response.choices[0].message.content}
    except Exception:
        return {"reply":"AI service unavailable. Use the built-in career roadmap and skill-gap analysis."}

@app.get("/api/jobs")
def jobs():
    return JOBS

@app.get("/api/applications")
def applications():
    c = db()
    rows = c.execute("SELECT * FROM applications ORDER BY id DESC").fetchall()
    c.close()
    return [dict(r) for r in rows]

@app.post("/api/applications")
def add_application(a: Application):
    c = db()
    cur = c.execute(
        "INSERT INTO applications(title,company,status,link) VALUES(?,?,?,?)",
        (a.title,a.company,a.status,a.link)
    )
    c.commit()
    new_id = cur.lastrowid
    c.close()
    return {"id":new_id, **a.model_dump()}

@app.patch("/api/applications/{application_id}")
def update_application(application_id: int, status: str):
    c = db()
    c.execute("UPDATE applications SET status=? WHERE id=?", (status,application_id))
    c.commit()
    c.close()
    return {"updated":True}

@app.delete("/api/applications/{application_id}")
def delete_application(application_id: int):
    c = db()
    c.execute("DELETE FROM applications WHERE id=?", (application_id,))
    c.commit()
    c.close()
    return {"deleted":True}

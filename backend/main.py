from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text(file):
    text = ""
    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text.lower()

    return text


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile,
    name: str = Form(...),
    company: str = Form(...),
    role: str = Form(...)
):

    file_bytes = await file.read()
    file_stream = io.BytesIO(file_bytes)

    resume_text = extract_text(file_stream)

    role_lower = role.lower()
    company_lower = company.lower()

    role_skills = {
        "software engineer": ["python","java","sql","data structures","algorithms","git"],
        "data analyst": ["python","sql","excel","statistics","data visualization"],
        "frontend developer": ["html","css","javascript","react"],
        "backend developer": ["python","java","node","rest api","docker"]
    }

    company_skills = {
        "google": ["system design","distributed systems"],
        "amazon": ["aws","microservices"],
        "microsoft": ["azure",".net"],
        "meta": ["graphql","react"]
    }

    if role_lower not in role_skills:
        return {"error":"Unknown role"}

    skills_db = role_skills[role_lower].copy()

    if company_lower in company_skills:
        skills_db += company_skills[company_lower]

    strengths=[]
    missing=[]

    for skill in skills_db:
        if skill in resume_text:
            strengths.append(skill)
        else:
            missing.append(skill)

    ats_score = int((len(strengths)/len(skills_db))*100)

    job_match = "Yes" if ats_score >= 70 else "No"

    # interview questions
    interview_questions=[
        "Explain one of your recent projects.",
        "What are your strongest technical skills?",
        "How do you debug a production issue?"
    ]

    # improvement suggestions
    suggestions=[]
    for skill in missing:
        suggestions.append(f"Consider improving your knowledge in {skill} by building projects or completing courses.")

    # role suggestions
    role_suggestions=[]

    if "python" in resume_text and "sql" in resume_text and role_lower!="data analyst":
        role_suggestions.append("Data Analyst")

    if "html" in resume_text and "css" in resume_text and role_lower!="frontend developer":
        role_suggestions.append("Frontend Developer")

    if "node" in resume_text or "docker" in resume_text:
        if role_lower!="backend developer":
            role_suggestions.append("Backend Developer")

    if "java" in resume_text or "data structures" in resume_text:
        if role_lower!="software engineer":
            role_suggestions.append("Software Engineer")

    if len(role_suggestions)==0:
        role_suggestions.append("Software Developer")

    return {
        "Name":name,
        "Company":company,
        "Role":role,
        "ATS Score":ats_score,
        "Strengths":strengths,
        "Missing Skills":missing,
        "Job Match":job_match,
        "Interview Questions":interview_questions,
        "Suggestions":suggestions,
        "Role Suggestions":role_suggestions
    }
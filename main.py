from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import io
import PyPDF2
import google.generativeai as genai
import os
from dotenv import load_dotenv

import crud, models, schemas
from database import SessionLocal, engine, get_db

load_dotenv()

# Configure Gemini
GEMINI_API_KEY = "AIzaSyBbAHhfzd0Upx2PEg66cSNhiNokYzGaiKU"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobStream API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/jobs", response_model=List[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs

@app.get("/api/jobs/{job_id}", response_model=schemas.Job)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.post("/api/referrals", response_model=schemas.Referral)
def create_referral(referral: schemas.ReferralCreate, db: Session = Depends(get_db)):
    return crud.create_referral(db=db, referral=referral)

@app.post("/api/match-resume", response_model=List[schemas.Job])
async def match_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Read PDF content
    content = await file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    resume_text = ""
    for page in pdf_reader.pages:
        resume_text += page.extract_text() or ""
    
    # Stage 1: Fast Filter (Keywords)
    all_jobs = crud.get_jobs(db, skip=0, limit=1000)
    scored_jobs = []
    
    resume_lower = resume_text.lower()
    for job in all_jobs:
        score = 0
        if job.title.lower() in resume_lower: score += 10
        if job.tags:
            for tag in job.tags:
                if tag.lower() in resume_lower: score += 5
        if score > 0:
            scored_jobs.append({"job": job, "score": score})
    
    # Take top 20 for Deep AI Ranking
    scored_jobs.sort(key=lambda x: x["score"], reverse=True)
    top_candidates = scored_jobs[:20]
    
    if not top_candidates:
        return []

    # Stage 2: Deep AI Ranking (Gemini)
    final_ordered_jobs = []
    try:
        jobs_info = "\n".join([f"ID: {i}, Title: {c['job'].title}, Tags: {c['job'].tags}" for i, c in enumerate(top_candidates)])
        prompt = f"""
        You are an elite career recruiter. Analyze this resume and rank the provided job listings based on 90%+ match accuracy.
        Return ONLY a comma-separated list of IDs in order of best match.
        
        RESUME:
        {resume_text[:2000]}
        
        JOBS:
        {jobs_info}
        """
        
        response = model.generate_content(prompt)
        order_text = response.text.strip()
        ordered_ids = [int(x.strip()) for x in order_text.split(",") if x.strip().isdigit()]
        
        # Build the prioritized list
        ranked_jobs = []
        ranked_job_ids = set()
        
        for idx in ordered_ids:
            if idx < len(top_candidates):
                job = top_candidates[idx]["job"]
                ranked_jobs.append(job)
                ranked_job_ids.add(job.id)
        
        # Add the remaining top candidates that Gemini might have missed
        for c in top_candidates:
            if c["job"].id not in ranked_job_ids:
                ranked_jobs.append(c["job"])
                ranked_job_ids.add(c["job"].id)
                
        # Now add ALL other jobs from the database that weren't in the top matches
        others = [job for job in all_jobs if job.id not in ranked_job_ids]
        final_ordered_jobs = ranked_jobs + others
        
        return final_ordered_jobs
        
    except Exception as e:
        print(f"Gemini Error: {e}")
        # Fallback: Top keywords first, then others
        top_ids = {c["job"].id for c in top_candidates}
        others = [job for job in all_jobs if job.id not in top_ids]
        return [c["job"] for c in top_candidates] + others

@app.get("/")
def read_root():
    return {"message": "JobStream AI Backend with Gemini Accuracy Active"}
@app.post("/api/analytics/{metric_name}")
def record_metric(metric_name: str, update: schemas.AnalyticsUpdate, db: Session = Depends(get_db)):
    return crud.update_analytics(db=db, metric_name=metric_name, increment_by=update.increment_by)

@app.get("/api/analytics", response_model=List[schemas.Analytics])
def get_analytics(db: Session = Depends(get_db)):
    return crud.get_all_analytics(db=db)

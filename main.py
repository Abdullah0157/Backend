from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import io
import PyPDF2

import crud, models, schemas
from database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobStream API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
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
        
    resume_text = resume_text.lower()
    
    # Get all jobs
    jobs = crud.get_jobs(db, skip=0, limit=1000)
    
    # Score jobs based on simple keyword matching
    scored_jobs = []
    for job in jobs:
        score = 0
        
        # Check job title words
        title_words = job.title.lower().split()
        for word in title_words:
            if len(word) > 3 and word in resume_text:
                score += 5
                
        # Check tags
        if job.tags:
            for tag in job.tags:
                tag_lower = tag.lower()
                if tag_lower in resume_text:
                    score += 10
                    
        # Check description
        desc_words = job.description.lower().split()
        for word in desc_words:
            if len(word) > 4 and word in resume_text:
                score += 1
                
        if score > 0:
            scored_jobs.append({"job": job, "score": score})
            
    # Sort jobs by score descending
    scored_jobs.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top matched jobs
    return [item["job"] for item in scored_jobs]

@app.get("/")
def read_root():
    return {"message": "Welcome to JobStream API"}

import json
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Job
from database import SQLALCHEMY_DATABASE_URL, engine, SessionLocal

db = SessionLocal()

jobs_data = [
    {
        "title": "Electronics expert - LTspice",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$30 - $100/hour",
        "posted_at": "3 days ago",
        "logo": "/images/logo.jpeg",
        "tags": ["Electronics engineering", "Pcb layout", "Circuit simulation"],
        "description": "We are seeking an Electronics expert with proficiency in LTspice to join our remote talent network. High demand role.",
        "benefits": ["Flexible hours", "Remote work", "High pay"],
        "referral_bonus": 500,
        "openings_count": 20,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/e9ee912f-5558-42bd-8cb3-d77d1ee71359?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
    },
    {
        "title": "Electronics Expert - DesignSpark PCB",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$30 - $100/hour",
        "posted_at": "3 days ago",
        "logo": "/images/logo.jpeg",
        "tags": ["Designspark pcb", "Electronics engineering", "Circuits simulation"],
        "description": "We are looking for an Electronics Expert specialized in DesignSpark PCB. Apply now through our portal.",
        "benefits": ["Flexible hours", "Remote work", "High pay"],
        "referral_bonus": 500,
        "openings_count": 20,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/c4dcf219-4064-4ae3-9d8f-c76937fbcdaa?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
    },
    {
        "title": "Senior Game QA Tester",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$25 - $50/hour",
        "posted_at": "Yesterday",
        "logo": "/images/logo.jpeg",
        "tags": ["Qa", "Gaming"],
        "description": "Seeking a Senior Game QA Tester for an exciting upcoming project. Experience in the gaming industry is required.",
        "benefits": ["Remote work", "Flexible hours", "Gaming perks"],
        "referral_bonus": 300,
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": False,
        "apply_url": "https://jobs.micro1.ai/post/23962884-f66f-48f1-8a27-34c652cdb88a?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
    },
    {
        "title": "Energy Compliance Attorney",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$100 - $135/hour",
        "posted_at": "Yesterday",
        "logo": "/images/logo.jpeg",
        "tags": ["Pjm interconnection compliance", "Ferc regulations", "Energy permitting"],
        "description": "We are seeking an Energy Compliance Attorney familiar with FERC regulations and PJM interconnection.",
        "benefits": ["Remote work", "High pay", "Career growth"],
        "referral_bonus": 1000,
        "openings_count": 100,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/da472a74-0ccc-4006-b84c-c4ad6b3b823c?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
    },
    {
        "title": "Video related professional for AI training",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$20 - $70/hour",
        "posted_at": "Yesterday",
        "logo": "/images/logo.jpeg",
        "tags": ["Video editing", "Video production workflows", "Motion graphics"],
        "description": "Looking for video professionals to assist with AI training models. High demand role with flexible hours.",
        "benefits": ["Remote work", "Flexible hours"],
        "referral_bonus": 200,
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/b0bba9cf-0617-4dd2-9cb7-ee348936e72f?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
    },
    {
        "title": "Financial Due Diligence Analyst",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$35 - $70/hour",
        "posted_at": "Yesterday",
        "logo": "/images/logo.jpeg",
        "tags": ["Personally identifiable information", "Confidential information memorandums", "Mergers and acquisitions"],
        "description": "Seeking a Financial Due Diligence Analyst with M&A experience. Secure and confidential environment.",
        "benefits": ["Remote work", "Competitive pay"],
        "referral_bonus": 500,
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/3136cc03-42c3-4b16-a591-e74c486ab8fe?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
    },
    {
        "title": "Software Engineer - Open 3D Engine (O3DE)",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$50 - $120/hour",
        "posted_at": "Today",
        "logo": "/images/logo.jpeg",
        "tags": ["Python", "C++", "O3de"],
        "description": "Software Engineer role specializing in O3DE. Python and C++ experience required. Competitive pay and multiple openings.",
        "benefits": ["Remote work", "Career growth", "High pay"],
        "referral_bonus": 1000,
        "openings_count": 20,
        "is_new": True,
        "is_high_demand": False,
        "apply_url": "https://jobs.micro1.ai/post/10b6ac1c-a009-44ca-bc88-5c4c29d92421?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
    },
    {
        "title": "Law Clerk",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$42 - $55/hour",
        "posted_at": "Today",
        "logo": "/images/logo.jpeg",
        "tags": ["Right-of-way acquisition", "Site control documentation", "Easement agreements"],
        "description": "We are seeking a Law Clerk with experience in right-of-way acquisition and site control documentation.",
        "benefits": ["Remote work", "Flexible hours"],
        "referral_bonus": 250,
        "openings_count": 100,
        "is_new": True,
        "is_high_demand": False,
        "apply_url": "https://jobs.micro1.ai/post/285bbb2e-67a1-4bd8-9aeb-2a3d5977c534?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
    },
    {
        "title": "Financial Data Privacy Analyst",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$35 - $70/hour",
        "posted_at": "Yesterday",
        "logo": "/images/logo.jpeg",
        "tags": ["Personally identifiable information", "Data protection laws", "Gdpr"],
        "description": "Financial Data Privacy Analyst needed to ensure compliance with GDPR and data protection laws.",
        "benefits": ["Remote work", "Flexible hours"],
        "referral_bonus": 400,
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/8d79de53-a823-4c72-b352-44ec5644a0f1?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
    }
]

for job_data in jobs_data:
    new_job = Job(**job_data)
    db.add(new_job)

db.commit()
print("Jobs added successfully.")


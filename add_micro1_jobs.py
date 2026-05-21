import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Job
from dotenv import load_dotenv

load_dotenv()

# Supabase URL
SUPABASE_URL = "postgresql://postgres.lssvpgbokrkxbytrifax:WHYsoserious%40%401@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"

engine = create_engine(SUPABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

new_jobs = [
    {
        "title": "Electronics expert - LTspice",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$30 - $100/hour",
        "posted_at": "Today",
        "tags": ["Electronics engineering", "Pcb layout", "Circuit simulation"],
        "description": "Seeking an Electronics Expert specializing in LTspice for high-impact projects.",
        "openings_count": 20,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/e9ee912f-5558-42bd-8cb3-d77d1ee71359?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Electronics Expert - DesignSpark PCB",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$30 - $100/hour",
        "posted_at": "Today",
        "tags": ["Designspark pcb", "Electronics engineering", "Circuits simulation"],
        "description": "Required skills in DesignSpark PCB and Electronics engineering for remote roles.",
        "openings_count": 20,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/c4dcf219-4064-4ae3-9d8f-c76937fbcdaa?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Senior Game QA Tester",
        "company": "micro1",
        "location": "Remote",
        "type": "Full-time",
        "salary": "$25 - $50/hour",
        "posted_at": "Yesterday",
        "tags": ["Qa", "Gaming"],
        "description": "Senior QA role for high-tier gaming projects. Manual and automated testing required.",
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": False,
        "apply_url": "https://jobs.micro1.ai/post/23962884-f66f-48f1-8a27-34c652cdb88a?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Energy Compliance Attorney",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$100 - $135/hour",
        "posted_at": "Yesterday",
        "tags": ["Pjm interconnection compliance", "Ferc regulations", "Energy permitting"],
        "description": "High demand role for Energy Compliance professionals with legal expertise.",
        "openings_count": 100,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/da472a74-0ccc-4006-b84c-c4ad6b3b823c?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Video related professional for AI training",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$20 - $70/hour",
        "posted_at": "Yesterday",
        "tags": ["Video editing", "Video production workflows", "Motion graphics"],
        "description": "Helping train AI models for video generation and production workflows.",
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/b0bba9cf-0617-4dd2-9cb7-ee348936e72f?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Financial Due Diligence Analyst",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$35 - $70/hour",
        "posted_at": "Yesterday",
        "tags": ["Personally identifiable information", "Confidential information memorandums", "Mergers and acquisitions"],
        "description": "Analyst role for M&A and financial due diligence projects.",
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/3136cc03-42c3-4b16-a591-e74c486ab8fe?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Software Engineer - Open 3D Engine (O3DE)",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$50 - $120/hour",
        "posted_at": "Today",
        "tags": ["Python", "C++", "O3de"],
        "description": "Software Engineer specializing in O3DE. Python and C++ experience required.",
        "openings_count": 20,
        "is_new": True,
        "is_high_demand": False,
        "apply_url": "https://jobs.micro1.ai/post/10b6ac1c-a009-44ca-bc88-5c4c29d92421?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Law Clerk",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$42 - $55/hour",
        "posted_at": "Today",
        "tags": ["Right-of-way acquisition", "Site control documentation", "Easement agreements"],
        "description": "Law Clerk role for right-of-way acquisition and site control projects.",
        "openings_count": 100,
        "is_new": True,
        "is_high_demand": False,
        "apply_url": "https://jobs.micro1.ai/post/285bbb2e-67a1-4bd8-9aeb-2a3d5977c534?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Financial Data Privacy Analyst",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$35 - $70/hour",
        "posted_at": "Yesterday",
        "tags": ["Personally identifiable information", "Data protection laws", "Gdpr"],
        "description": "Ensuring data privacy and compliance for financial projects.",
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/8d79de53-a823-4c72-b352-44ec5644a0f1?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Data Scientist",
        "company": "micro1",
        "location": "Remote",
        "type": "Full-time",
        "salary": "$65 - $130/hour",
        "posted_at": "Yesterday",
        "tags": ["Statistics & mathematics", "Data handling", "Data collecting"],
        "description": "Data Scientist role for statistics, mathematics, and data handling.",
        "openings_count": 10,
        "is_new": True,
        "is_high_demand": False,
        "apply_url": "https://jobs.micro1.ai/post/cef89677-efa9-44af-8043-c05fd78d7b85?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Senior Media Designer",
        "company": "micro1",
        "location": "Remote",
        "type": "Full-time",
        "salary": "Competitive",
        "posted_at": "Yesterday",
        "tags": ["Powerpoint", "Keynote", "Google slides"],
        "description": "Senior role for media and presentation design.",
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/2d670241-6164-4498-bd68-9a6ee1b7cac4?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Legal Expert",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$42 - $55/hour",
        "posted_at": "Yesterday",
        "tags": ["Right-of-way acquisition", "Site control documentation", "Easement agreements"],
        "description": "Legal expert needed for large scale right-of-way and site control projects.",
        "openings_count": 100,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/14a074c9-5718-48a8-943b-856545e11525?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Arabic Language Expert",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$10 - $41/hour",
        "posted_at": "Yesterday",
        "tags": ["Proficiency in arabic", "Msa", "Phonetics"],
        "description": "Language expert for Arabic phonetics and MSA proficiency.",
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": False,
        "apply_url": "https://jobs.micro1.ai/post/91007b77-0525-4013-a8ea-d89a8bcf72f8?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Motorola Razr User Tester",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$20 - $30/hour",
        "posted_at": "Yesterday",
        "tags": ["Motorola razr", "Tech experience", "Phone usage"],
        "description": "Tester role for Motorola Razr users to help improve the device experience.",
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/593fc550-be1e-45d2-a0ec-abdc890ac9b1?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "French Language Expert (Canada)",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$15 - $25/hour",
        "posted_at": "Yesterday",
        "tags": ["Vocal clarity & diction", "Audio recording proficiency", "Attention to detail"],
        "description": "French language expert for Canadian region. Focus on audio recording and diction.",
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/095731d4-16e3-4605-871d-6d8a96586fea?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Senior Powerpoint Presentation Designer",
        "company": "micro1",
        "location": "Remote",
        "type": "Full-time",
        "salary": "$100 - $200/hour",
        "posted_at": "Yesterday",
        "tags": ["Microsoft powerpoint", "Presentation", "Storytelling"],
        "description": "Senior designer role focused on high-stakes Powerpoint presentations and storytelling.",
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/9a601fb4-bdfd-4b45-8337-2afdf8814dc6?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "French Language Expert",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$15 - $23/hour",
        "posted_at": "Yesterday",
        "tags": ["Native french", "Transcript correction", "Attention to detail"],
        "description": "Native French expert for transcript correction and data validation.",
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/c8ca7e91-45b5-4a7e-ab53-35596dd19f78?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "SDR, New Grad (Enterprise AI)",
        "company": "micro1",
        "location": "Remote",
        "type": "Full-time",
        "salary": "$90,000 - $110,000/year",
        "posted_at": "Today",
        "tags": ["Outbound prospecting", "Crm", "Enterprise ai"],
        "description": "Sales Development Representative role for new grads interested in Enterprise AI.",
        "openings_count": 1,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/3380e3d0-2a8b-488a-81f9-bb721f987257?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    },
    {
        "title": "Video Data Reviewer",
        "company": "micro1",
        "location": "Remote",
        "type": "Contract",
        "salary": "$10 - $15/hour",
        "posted_at": "Today",
        "tags": ["Visual discrimination", "Process adherence", "Written clarity"],
        "description": "Video data reviewer role for large scale visual content evaluation.",
        "openings_count": 250,
        "is_new": True,
        "is_high_demand": True,
        "apply_url": "https://jobs.micro1.ai/post/e5c13a49-f401-4db1-aee8-2416ffc319c6?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf"
    }
]

for job_data in new_jobs:
    # Set default values for missing fields
    job_data.setdefault("benefits", ["Remote", "Healthcare", "Flexible"])
    job_data.setdefault("logo", "/images/logo.jpeg")
    job_data.setdefault("referral_bonus", 500)
    
    db_job = Job(**job_data)
    db.add(db_job)

db.commit()
print(f"Successfully added {len(new_jobs)} high-demand Micro1 roles to Supabase!")
db.close()

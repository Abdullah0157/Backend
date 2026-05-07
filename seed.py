import json
from database import SessionLocal, engine
import models

# Create tables
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

def seed_final_data():
    db = SessionLocal()
    
    # VIP Jobs with rich manual data and exact direct URLs
    jobs_data = [
        {
            "title": "Energy Regulatory Attorney",
            "posted_at": "Today",
            "is_new": True,
            "is_high_demand": True,
            "openings_count": 100,
            "salary": "$100 - $135/hour",
            "referral_bonus": 500,
            "tags": ["Pjm interconnection compliance", "Ferc regulations", "Energy permitting"],
            "apply_url": "https://jobs.micro1.ai/post/a3769b75-c39f-4227-a03d-1e4e6f1ab035?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
        },
        {
            "title": "Paralegal",
            "posted_at": "Today",
            "is_new": True,
            "is_high_demand": True,
            "openings_count": 100,
            "salary": "$42 - $55/hour",
            "referral_bonus": 500,
            "tags": ["Right-of-way acquisition", "Site control documentation", "Easement agreements"],
            "apply_url": "https://jobs.micro1.ai/post/b0233e00-ed98-491d-b15c-c2b5bce27388?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
        },
        {
            "title": "Law Clerk (Commercial Real Estate / Energy)",
            "posted_at": "Today",
            "is_new": True,
            "is_high_demand": False,
            "openings_count": 50,
            "salary": "$50 - $120/hour",
            "referral_bonus": 500,
            "tags": ["Commercial real estate document review", "Title & ownership understanding", "Data extraction"],
            "apply_url": "https://jobs.micro1.ai/post/03032271-800c-4013-8c48-821f281f705e?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
        },
        {
            "title": "Corporate M&A Paralegal",
            "posted_at": "Yesterday",
            "is_new": True,
            "is_high_demand": True,
            "openings_count": 1,
            "salary": "$40 - $70/hour",
            "referral_bonus": 1000,
            "tags": ["Personally identifiable information", "Compliance", "Mergers & acquisitions"],
            "apply_url": "https://jobs.micro1.ai/post/a945e259-58b0-48c3-9eeb-77e935cd6d97?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
        },
        {
            "title": "Corporate/M&A Attorney",
            "posted_at": "Yesterday",
            "is_new": True,
            "is_high_demand": True,
            "openings_count": 1,
            "salary": "$40 - $70/hour",
            "referral_bonus": 1000,
            "tags": ["Personally identifiable information", "Compliance", "Mergers & acquisitions"],
            "apply_url": "https://jobs.micro1.ai/post/b22ee3a5-69b5-455f-a8a2-27951ee9d575?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
        },
        {
            "title": "Visual Evaluation Specialist",
            "posted_at": "Recently",
            "is_new": False,
            "is_high_demand": False,
            "openings_count": 499,
            "salary": "$20 - $70/hour",
            "referral_bonus": 500,
            "tags": ["Visual content evaluation", "Written communication", "Analytical skills"],
            "apply_url": "https://jobs.micro1.ai/post/937562ec-bc66-4321-afa7-19ea26fa838b?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral"
        }
    ]
    
    for i, item in enumerate(jobs_data):
        job = {
            "id": i + 1,
            "title": item["title"],
            "company": "micro1",
            "location": "Remote",
            "type": "Contract",
            "salary": item["salary"],
            "posted_at": item["posted_at"],
            "logo": "https://media.licdn.com/dms/image/C4D0BAQG7X7X7X7X7X7/company-logo_200_200/0/1630123456789", 
            "tags": item["tags"],
            "description": f"Join the micro1 network as a {item['title']}. Work with elite global teams on cutting-edge projects.",
            "benefits": ["Remote", "Global Impact", "Flexible"],
            "referral_bonus": item["referral_bonus"],
            "openings_count": item["openings_count"],
            "is_new": item["is_new"],
            "is_high_demand": item["is_high_demand"],
            "apply_url": item["apply_url"]
        }
        db_job = models.Job(**job)
        db.add(db_job)
    
    db.commit()
    print(f"Restored {len(jobs_data)} VIP jobs with direct links and rich details.")
    db.close()

if __name__ == "__main__":
    seed_final_data()

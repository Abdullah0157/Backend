import os
import requests
from sqlalchemy.orm import sessionmaker
from database import SessionLocal, engine
from models import Job
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# CONFIGURATION
# ==========================================
RAPIDAPI_KEY = "e952acf465msh1f9147278186d44p1baaa0jsna53819973d0d"
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
# ==========================================

def sync_jsearch_jobs(query_prefix, source_name):
    url = "https://jsearch.p.rapidapi.com/search"
    
    # We combine the category with the source for better results
    full_query = f"{query_prefix} jobs on {source_name}"
    
    querystring = {
        "query": full_query,
        "page": "1",
        "num_pages": "1"
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    print(f"Fetching {source_name} jobs for '{query_prefix}'...")
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return

        data = response.json()
        jobs_list = data.get("data", [])
        
        db = SessionLocal()
        new_jobs_count = 0
        
        for item in jobs_list:
            title = item.get("job_title")
            company = item.get("employer_name") or "Confidential"
            
            # Deduplication
            exists = db.query(Job).filter(Job.title == title, Job.company == company).first()
            if exists:
                continue

            # Parse Salary
            salary = "Competitive"
            min_sal = item.get("job_min_salary")
            max_sal = item.get("job_max_salary")
            currency = item.get("job_salary_currency", "$")
            period = item.get("job_salary_period", "year")
            
            if min_sal and max_sal:
                salary = f"{currency}{min_sal} - {currency}{max_sal}/{period}"
            elif min_sal:
                salary = f"{currency}{min_sal}/{period}"

            job = Job(
                title=title,
                company=company,
                location=f"{item.get('job_city', '')}, {item.get('job_country', 'Remote')}",
                type=item.get("job_employment_type", "Full-time"),
                salary=salary,
                posted_at="Recent",
                logo=item.get("employer_logo") or "/images/logo.jpeg",
                tags=[query_prefix, source_name],
                description=item.get("job_description", "High impact role. View details to apply.")[:500] + "...",
                benefits=["Remote/Hybrid", "Professional Growth"],
                referral_bonus=0,
                openings_count=1,
                is_new=True,
                is_high_demand=False,
                apply_url=item.get("job_apply_link") or "https://www.google.com"
            )
            
            db.add(job)
            new_jobs_count += 1
            
        db.commit()
        print(f"Added {new_jobs_count} jobs from {source_name} for {query_prefix}.")
        db.close()
        
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    categories = [
        "Software Engineer", "Marketing", "Data Science", "Sales", 
        "Customer Service", "Graphic Design", "Project Management", 
        "Finance", "Healthcare", "Education"
    ]
    
    # Split the 20 requests: 10 for LinkedIn, 10 for Glassdoor
    for cat in categories:
        sync_jsearch_jobs(cat, "LinkedIn")
        sync_jsearch_jobs(cat, "Glassdoor")

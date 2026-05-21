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
RAPIDAPI_HOST = "indeed12.p.rapidapi.com"
# ==========================================

def sync_indeed_jobs(query="Remote", location="USA", limit=50):
    url = "https://indeed12.p.rapidapi.com/jobs/search"
    
    querystring = {
        "query": query,
        "location": location,
        "locality": "us",
        "radius": "50",
        "start": "0",
        "sort": "date",
        "age": "30"
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    print(f"Fetching Indeed jobs for '{query}' in '{location}'...")
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code != 200:
        print(f"Error fetching from Indeed: {response.status_code} - {response.text}")
        return

    data = response.json()
    # Note: The 'indeed12' API usually returns jobs in data['hits'] or data['results']
    jobs_list = data.get("hits") or data.get("results") or []
    
    if not jobs_list:
        print("No jobs found for this search.")
        return

    print(f"Found {len(jobs_list)} jobs. Syncing to database...")
    db = SessionLocal()
    
    try:
        new_jobs_count = 0
        for item in jobs_list:
            # Check if job already exists by title and company
            title = item.get("title")
            company = item.get("company_name") or "Unknown Company"
            job_id = item.get("id")
            
            exists = db.query(Job).filter(Job.title == title, Job.company == company).first()
            if exists:
                continue

            # Format Salary
            salary_data = item.get("salary")
            if isinstance(salary_data, dict):
                min_val = salary_data.get("min")
                max_val = salary_data.get("max")
                s_type = salary_data.get("type", "").lower()
                if min_val and min_val > 0:
                    salary_str = f"${min_val}"
                    if max_val and max_val > 0:
                        salary_str += f" - ${max_val}"
                    salary_str += f"/{s_type}" if s_type else ""
                else:
                    salary_str = "Competitive"
            else:
                salary_str = str(salary_data) if salary_data else "Competitive"

            # Format Link
            apply_url = f"https://www.indeed.com/viewjob?jk={job_id}" if job_id else item.get("link")

            job = Job(
                title=title,
                company=company,
                location=item.get("location", "Remote"),
                type="Full-time",
                salary=salary_str,
                posted_at=item.get("formatted_relative_time") or "Today",
                logo="/images/logo.jpeg",
                tags=[query, "Indeed"],
                description=f"Remote opportunity at {company}. Apply now to join their team.",
                benefits=["Remote work", "Career growth"],
                referral_bonus=0,
                openings_count=1,
                is_new=True,
                is_high_demand=False,
                apply_url=apply_url
            )
            
            db.add(job)
            new_jobs_count += 1
            
        db.commit()
        print(f"Successfully added {new_jobs_count} new jobs from Indeed!")
        
    except Exception as e:
        print(f"Error saving to database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    categories = [
        "Software Engineer Remote",
        "Data Analyst Remote",
        "Virtual Assistant",
        "Digital Marketing Remote",
        "Customer Support Remote",
        "Graphic Designer Remote",
        "Project Manager Remote",
        "Content Writer Remote",
        "Social Media Manager",
        "Sales Representative Remote",
        "Accountant Remote",
        "HR Coordinator Remote",
        "UI/UX Designer Remote",
        "Copywriter Remote",
        "SEO Specialist Remote"
    ]
    
    for category in categories:
        sync_indeed_jobs(query=category)

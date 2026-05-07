import json
import os
import sys
from sqlalchemy.orm import sessionmaker

# Import database configuration and Job model from your existing backend
from database import SessionLocal, engine
from models import Job

# ==========================================
# CONFIGURATION
# ==========================================
MERCOR_REFERRAL_CODE = "t8o9i"
OBFUSCATED_COMPANY_NAME = "Confidential Partner"
GENERIC_LOGO_URL = "/images/logo.jpeg"  # The generic logo we used for Micro1
JSON_FILE_PATH = "mercor_data.json"
# ==========================================

def sync_local_mercor():
    if not os.path.exists(JSON_FILE_PATH):
        print(f"Error: {JSON_FILE_PATH} not found. Please make sure you saved the JSON data in the backend folder.")
        return

    print("Reading local JSON file...")
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to read JSON: {e}")
        return

    # Depending on Mercor's API response structure, the jobs might be in a list or inside a key (like 'data', 'jobs', etc.)
    # Let's handle both common cases
    jobs_list = []
    if isinstance(data, list):
        jobs_list = data
    elif isinstance(data, dict):
        # Look for common array keys
        for key in ["data", "jobs", "results", "listings"]:
            if key in data and isinstance(data[key], list):
                jobs_list = data[key]
                break
        
        # If still empty, maybe the dict itself is a single job
        if not jobs_list:
            jobs_list = [data]

    if not jobs_list:
        print("Could not find a list of jobs in the JSON file. Make sure you copied the correct response.")
        return

    print(f"Found {len(jobs_list)} jobs in the JSON file. Syncing to database...")
    db = SessionLocal()
    
    try:
        new_jobs_count = 0
        
        for item in jobs_list:
            # Mercor's JSON structure might vary, so we use .get() with fallbacks
            title = item.get("title") or item.get("jobTitle") or item.get("name") or "Software Engineer"
            
            # Format salary
            salary_min = item.get("minSalary") or item.get("salaryMin")
            salary_max = item.get("maxSalary") or item.get("salaryMax")
            
            if salary_min and salary_max:
                salary = f"${salary_min} - ${salary_max}/hour"
            else:
                salary = item.get("salaryRange") or item.get("salary") or "Competitive"
            
            # Extract skills/tags
            tags = item.get("skills") or item.get("tags") or item.get("requirements") or []
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",")][:4]
            elif isinstance(tags, list):
                tags = [str(t) for t in tags][:4]
            else:
                tags = []
                
            # Referral URL
            original_url = item.get("applyUrl") or item.get("url") or "https://t.mercor.com"
            if "mercor.com" not in original_url:
                original_url = f"https://t.mercor.com/{MERCOR_REFERRAL_CODE}"
            else:
                separator = "&" if "?" in original_url else "?"
                original_url = f"{original_url}{separator}referralCode={MERCOR_REFERRAL_CODE}"

            job = Job(
                title=title,
                company=OBFUSCATED_COMPANY_NAME,
                location=item.get("location", "Remote"),
                type=item.get("jobType") or item.get("type", "Full-time"),
                salary=salary,
                posted_at="Today", 
                logo=GENERIC_LOGO_URL,
                tags=tags,
                description=item.get("description", "Join our elite partner network. Fast-tracked remote opportunity."),
                benefits=["Remote work", "Flexible hours", "High pay"],
                referral_bonus=item.get("referralBonus", 0),
                openings_count=item.get("openings") or item.get("vacancies", 1),
                is_new=True,
                is_high_demand=True,
                apply_url=original_url
            )
            
            db.add(job)
            new_jobs_count += 1
            
        db.commit()
        print(f"Successfully synced {new_jobs_count} jobs from local JSON!")
        
    except Exception as e:
        print(f"An error occurred during sync: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    sync_local_mercor()

import os
import sys
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from apify_client import ApifyClient

# Import database configuration and Job model from your existing backend
from database import SessionLocal, engine
from models import Job

# ==========================================
# CONFIGURATION - FILL THESE IN
# ==========================================
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "YOUR_APIFY_API_TOKEN_HERE")
MERCOR_REFERRAL_CODE = "t8o9i"

# The name you want to display instead of 'Mercor'
OBFUSCATED_COMPANY_NAME = "Confidential Partner"
GENERIC_LOGO_URL = "/images/logo.jpeg"  # The generic logo we used for Micro1
# ==========================================

def sync_mercor_jobs():
    if APIFY_API_TOKEN == "YOUR_APIFY_API_TOKEN_HERE":
        print("Error: Please set your APIFY_API_TOKEN in the script.")
        return

    print("Initializing Apify Client...")
    client = ApifyClient(APIFY_API_TOKEN)

    # The Apify actor for Mercor
    actor_id = "fantastic-jobs/mercor-job-search-api"

    # Input for the Apify Actor (you can adjust filters like keywords if needed)
    run_input = {
        "limit": 50, # Number of jobs to fetch
    }

    print("Starting Apify Actor run to fetch Mercor jobs... This may take a moment.")
    run = client.actor(actor_id).call(run_input=run_input)

    print("Fetching results from Apify dataset...")
    dataset_items = client.dataset(run["defaultDatasetId"]).iterate_items()

    db = SessionLocal()
    
    try:
        # Optional: Remove old Mercor jobs to keep the list fresh
        # db.query(Job).filter(Job.company == OBFUSCATED_COMPANY_NAME).delete()
        # db.commit()
        
        new_jobs_count = 0
        
        for item in dataset_items:
            title = item.get("title", "Software Engineer")
            
            # Format salary properly or set a default
            salary_raw = item.get("salaryRange") or item.get("salary")
            salary = salary_raw if salary_raw else "Competitive/Negotiable"
            
            # Format tags/skills
            skills = item.get("skills", [])
            tags = skills[:4] if isinstance(skills, list) else []
            
            # Generate Referral URL
            original_url = item.get("applyUrl") or item.get("url", "")
            # Ensure the URL doesn't already have query parameters before appending
            separator = "&" if "?" in original_url else "?"
            referral_url = f"{original_url}{separator}referralCode={MERCOR_REFERRAL_CODE}"

            job = Job(
                title=title,
                company=OBFUSCATED_COMPANY_NAME,
                location=item.get("location", "Remote"),
                type=item.get("jobType", "Full-time"),
                salary=salary,
                posted_at="Today", # Or parse from item.get("postedAt")
                logo=GENERIC_LOGO_URL,
                tags=tags,
                description=item.get("description", "Join our elite partner network. High demand role."),
                benefits=["Remote work", "Flexible hours", "High pay"],
                referral_bonus=item.get("referralBonus", 0),
                openings_count=item.get("openings", 1),
                is_new=True,
                is_high_demand=True,
                apply_url=referral_url
            )
            
            db.add(job)
            new_jobs_count += 1
            
        db.commit()
        print(f"Successfully synced {new_jobs_count} jobs from Mercor!")
        
    except Exception as e:
        print(f"An error occurred during sync: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    sync_mercor_jobs()

import re
import os
from database import SessionLocal, engine
import models

# Ensure tables exist
models.Base.metadata.create_all(bind=engine)

def parse_and_append(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    # Split into chunks based on "Posted" or "osted" markers
    # But some jobs might not have the "Posted" line at the start of the chunk in the raw text.
    # A better delimiter might be the URL or a combination.
    
    lines = content.split('\n')
    jobs = []
    current_job = {}
    current_skills = []
    in_skills = False
    
    # helper to clean lines
    def clean(s):
        return s.strip()

    for line in lines:
        line = clean(line)
        if not line:
            continue
            
        lower = line.lower()
        
        # URL line - usually marks the end of a job block
        if lower.startswith('http'):
            # Some URLs have garbage mashed at the end in the raw text
            url_match = re.match(r'(https?://[^\s]+)', line)
            if url_match:
                current_job['apply_url'] = url_match.group(1)
            
            if current_job.get('title'):
                current_job['tags'] = current_skills[:5]
                jobs.append(current_job)
                
            # Reset for next
            current_job = {}
            current_skills = []
            in_skills = False
            continue

        # Date markers
        if lower.startswith('posted') or lower.startswith('osted') or 'a month ago' in lower or '2 months ago' in lower:
            current_job['posted_at'] = line.replace('osted', 'Posted')
            if 'new' in lower:
                current_job['is_new'] = True
            continue

        # High demand
        if 'high demand' in lower:
            current_job['is_high_demand'] = True
            continue

        # micro1
        if lower == 'micro1':
            in_skills = False
            continue

        # Required skills
        if 'required skills' in lower:
            in_skills = True
            continue

        # Pay
        if lower.startswith('pay:') or lower.startswith('pay :'):
            current_job['salary'] = line.split(':', 1)[1].strip()
            in_skills = False
            continue

        # Openings
        opening_match = re.search(r'(\d+)\s+opening', lower)
        if opening_match:
            current_job['openings_count'] = int(opening_match.group(1))
            continue

        # Skills or mashed titles
        if in_skills:
            if line.startswith('+'):
                in_skills = False
            else:
                current_skills.append(line)
            continue
            
        # If we get here and don't have a title, it's probably the title
        if not current_job.get('title') and not lower.startswith('+') and 'refer and earn' not in lower:
            current_job['title'] = line
            continue

    # DB Insertion
    db = SessionLocal()
    existing = db.query(models.Job.title).all()
    existing_titles = set(t[0].lower() for t in existing)
    
    added = 0
    skipped = 0
    
    for j in jobs:
        title = j.get('title', '').strip()
        if not title or title.lower() in existing_titles:
            skipped += 1
            continue
            
        job = models.Job(
            title=title,
            company="micro1",
            location="Remote",
            type="Contract",
            salary=j.get('salary', 'Competitive'),
            posted_at=j.get('posted_at', 'Posted 18 days ago'),
            logo="",
            tags=j.get('tags', []),
            description=f"VIP role: {title} at micro1.",
            benefits=["Remote", "Flexible Schedule"],
            referral_bonus=300,
            openings_count=j.get('openings_count', 1),
            is_new=j.get('is_new', False),
            is_high_demand=j.get('is_high_demand', False),
            apply_url=j.get('apply_url', ''),
        )
        db.add(job)
        existing_titles.add(title.lower())
        added += 1

    db.commit()
    db.close()
    print(f"DONE: Added {added} new jobs. Skipped {skipped} duplicates.")

if __name__ == "__main__":
    parse_and_append('new_jobs_raw.txt')

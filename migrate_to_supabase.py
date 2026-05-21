import os
import sqlite3
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Job, Base
from dotenv import load_dotenv

load_dotenv()

# Supabase URL
SUPABASE_URL = "postgresql://postgres.lssvpgbokrkxbytrifax:WHYsoserious%40%401@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"

# 1. Connect to Local SQLite
sqlite_conn = sqlite3.connect('jobstream.db')
sqlite_conn.row_factory = sqlite3.Row
cursor = sqlite_conn.cursor()

# 2. Connect to Supabase
engine = create_engine(SUPABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def migrate():
    # Clear Supabase jobs table first for a clean migration
    print("Clearing existing jobs from Supabase...")
    db.query(Job).delete()
    db.commit()

    print("Fetching jobs from local database...")
    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} jobs locally.")

    print("Migrating to Supabase...")
    for row in rows:
        job_data = dict(row)
        if 'id' in job_data:
            del job_data['id'] # Let Postgres handle ID generation
        
        # Parse JSON fields
        if isinstance(job_data.get('tags'), str):
            try:
                job_data['tags'] = json.loads(job_data['tags'])
            except:
                pass
        if isinstance(job_data.get('benefits'), str):
            try:
                job_data['benefits'] = json.loads(job_data['benefits'])
            except:
                pass

        db_job = Job(**job_data)
        db.add(db_job)
    
    db.commit()
    print(f"Successfully migrated {len(rows)} jobs to Supabase!")
    db.close()

if __name__ == "__main__":
    migrate()

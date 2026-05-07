from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from datetime import datetime
from database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, default="micro1")
    location = Column(String)
    type = Column(String)
    salary = Column(String) # Pay range
    posted_at = Column(String)
    logo = Column(String)
    tags = Column(JSON) # Required skills
    description = Column(String)
    benefits = Column(JSON)
    referral_bonus = Column(Integer)
    openings_count = Column(Integer)
    is_new = Column(Boolean, default=False)
    is_high_demand = Column(Boolean, default=False)
    apply_url = Column(String) # Your referral link

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer)
    referral_code = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

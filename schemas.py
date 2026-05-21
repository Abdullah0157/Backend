from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class JobBase(BaseModel):
    title: str
    company: str = "micro1"
    location: str
    type: str
    salary: str
    posted_at: str
    logo: str
    tags: List[str]
    description: str
    benefits: List[str]
    referral_bonus: Optional[int] = 0
    openings_count: Optional[int] = 0
    is_new: Optional[bool] = False
    is_high_demand: Optional[bool] = False
    apply_url: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int

    class Config:
        from_attributes = True

class ReferralBase(BaseModel):
    job_id: int
    referral_code: str

class ReferralCreate(ReferralBase):
    pass

class Referral(ReferralBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class AnalyticsBase(BaseModel):
    metric_name: str
    value: int

class AnalyticsUpdate(BaseModel):
    increment_by: int = 1

class Analytics(AnalyticsBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True

class ChatMessagePart(BaseModel):
    text: str

class ChatMessage(BaseModel):
    role: str
    parts: List[ChatMessagePart]

class ChatRequest(BaseModel):
    contents: List[ChatMessage]

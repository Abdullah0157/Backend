from sqlalchemy.orm import Session
import models, schemas

def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()

def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def create_referral(db: Session, referral: schemas.ReferralCreate):
    db_referral = models.Referral(**referral.model_dump())
    db.add(db_referral)
    db.commit()
    db.refresh(db_referral)
    return db_referral

def update_analytics(db: Session, metric_name: str, increment_by: int = 1):
    db_metric = db.query(models.Analytics).filter(models.Analytics.metric_name == metric_name).first()
    if not db_metric:
        db_metric = models.Analytics(metric_name=metric_name, value=increment_by)
        db.add(db_metric)
    else:
        db_metric.value += increment_by
    db.commit()
    db.refresh(db_metric)
    return db_metric

def get_all_analytics(db: Session):
    return db.query(models.Analytics).all()

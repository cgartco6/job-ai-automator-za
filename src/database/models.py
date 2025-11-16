from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    subscription_tier = Column(String, default="basic")
    created_at = Column(DateTime, default=datetime.utcnow)

class UserDocument(Base):
    __tablename__ = "user_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    document_type = Column(String)  # resume, cover_letter, photo, certificate
    original_path = Column(String)
    processed_path = Column(String)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    job_title = Column(String)
    company = Column(String)
    job_url = Column(String)
    application_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="applied")  # applied, interview, rejected, offered
    match_score = Column(Float)
    application_data = Column(JSON)
    follow_up_tasks = Column(JSON)

class ApplicationSettings(Base):
    __tablename__ = "application_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    preferences = Column(JSON)
    target_companies = Column(JSON)
    excluded_companies = Column(JSON)
    salary_range = Column(JSON)
    locations = Column(JSON)
    auto_apply = Column(Boolean, default=True)

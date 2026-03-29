from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    status = Column(String, default="queued")  # queued, started, success, failed
    video_title = Column(String, nullable=True)
    video_duration = Column(Integer, nullable=True)
    options = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    clips_created = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Clip(Base):
    __tablename__ = "clips"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, nullable=False)
    clip_index = Column(Integer, nullable=False)
    clip_path = Column(String, nullable=True)
    start_time = Column(Float, nullable=True)
    end_time = Column(Float, nullable=True)
    viral_score = Column(Integer, nullable=True)
    hook = Column(String, nullable=True)
    platform_content = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
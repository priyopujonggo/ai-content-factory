from pydantic import BaseModel
from typing import Optional, Any


class JobOptions(BaseModel):
    max_clips: int = 5
    min_clip_duration: int = 30
    max_clip_duration: int = 90
    target_platforms: list[str] = ["tiktok", "instagram_reels", "youtube_shorts"]
    language: str = "auto"
    whisper_model: str = "base"


class JobCreate(BaseModel):
    url: str
    options: Optional[JobOptions] = None


class JobResponse(BaseModel):
    job_id: str
    status: str
    url: Optional[str] = None
    result: Optional[Any] = None
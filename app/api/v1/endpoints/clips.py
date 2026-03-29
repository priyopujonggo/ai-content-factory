from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.job_service import JobService

router = APIRouter()


@router.get("/{job_id}/clips")
async def get_clips(job_id: str, db: AsyncSession = Depends(get_db)):
    job_service = JobService(db)

    # pastikan job ada
    job = await job_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    clips = await job_service.get_clips_by_job(job_id)
    if not clips:
        raise HTTPException(status_code=404, detail="No clips found for this job")

    return {
        "job_id": job_id,
        "video_title": job.video_title,
        "total_clips": len(clips),
        "clips": [
            {
                "clip_index": clip.clip_index,
                "clip_path": clip.clip_path,
                "start_time": clip.start_time,
                "end_time": clip.end_time,
                "duration": round(clip.end_time - clip.start_time, 1),
                "viral_score": clip.viral_score,
                "hook": clip.hook,
                "platform_content": clip.platform_content,
            }
            for clip in clips
        ],
    }


@router.get("/{job_id}/clips/{clip_index}")
async def get_clip(job_id: str, clip_index: int, db: AsyncSession = Depends(get_db)):
    job_service = JobService(db)

    clips = await job_service.get_clips_by_job(job_id)
    clip = next((c for c in clips if c.clip_index == clip_index), None)

    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")

    return {
        "clip_index": clip.clip_index,
        "clip_path": clip.clip_path,
        "start_time": clip.start_time,
        "end_time": clip.end_time,
        "duration": round(clip.end_time - clip.start_time, 1),
        "viral_score": clip.viral_score,
        "hook": clip.hook,
        "platform_content": clip.platform_content,
    }
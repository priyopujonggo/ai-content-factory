from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.job import JobCreate, JobResponse
from app.tasks.ingest import ingest_video_task
from app.services.job_service import JobService
from app.core.database import get_db
from worker.celery_app import celery_app
import uuid

router = APIRouter()


@router.post("/", response_model=JobResponse, status_code=202)
async def create_job(payload: JobCreate, db: AsyncSession = Depends(get_db)):
    job_id = str(uuid.uuid4())

    # simpan job ke database dulu
    job_service = JobService(db)
    await job_service.create_job(
        job_id=job_id,
        url=payload.url,
        options=payload.options.model_dump() if payload.options else {},
    )

    # kirim ke Celery
    ingest_video_task.apply_async(
        kwargs={
            "url": payload.url,
            "options": payload.options.model_dump() if payload.options else {},
        },
        task_id=job_id,
    )

    return JobResponse(job_id=job_id, status="queued", url=payload.url)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)):
    job_service = JobService(db)
    job = await job_service.get_job(job_id)

    if not job:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Job not found")

    return JobResponse(
        job_id=job.id,
        status=job.status,
        url=job.url,
        result=job.result,
    )


@router.get("/")
async def list_jobs(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    from app.models.job import Job
    result = await db.execute(select(Job).order_by(Job.created_at.desc()))
    jobs = result.scalars().all()
    return [
        {
            "job_id": job.id,
            "url": job.url,
            "status": job.status,
            "video_title": job.video_title,
            "clips_created": job.clips_created,
            "created_at": job.created_at,
        }
        for job in jobs
    ]
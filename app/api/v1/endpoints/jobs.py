from fastapi import APIRouter
from app.schemas.job import JobCreate, JobResponse
from app.tasks.ingest import ingest_video_task
from worker.celery_app import celery_app

router = APIRouter()


@router.post("/", response_model=JobResponse, status_code=202)
async def create_job(payload: JobCreate):
    task = ingest_video_task.delay(
        url=payload.url,
        options=payload.options.model_dump() if payload.options else {},
    )
    return JobResponse(
        job_id=task.id,
        status="queued",
        url=payload.url,
    )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    result = celery_app.AsyncResult(job_id)

    return JobResponse(
        job_id=job_id,
        status=result.status.lower(),
        result=result.result if result.ready() else None,
    )
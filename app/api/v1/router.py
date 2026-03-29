from fastapi import APIRouter
from app.api.v1.endpoints.jobs import router as jobs_router
from app.api.v1.endpoints.clips import router as clips_router

api_router = APIRouter()

api_router.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(clips_router, prefix="/jobs", tags=["Clips"])
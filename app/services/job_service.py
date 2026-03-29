from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.job import Job, Clip


class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_job(self, job_id: str, url: str, options: dict) -> Job:
        job = Job(
            id=job_id,
            url=url,
            status="queued",
            options=options,
        )
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        return job

    async def update_job_status(
        self,
        job_id: str,
        status: str,
        video_title: str = None,
        clips_created: int = None,
        result: dict = None,
        error: str = None,
    ) -> None:
        result_query = await self.db.execute(select(Job).where(Job.id == job_id))
        job = result_query.scalar_one_or_none()
        if not job:
            return

        job.status = status
        if video_title:
            job.video_title = video_title
        if clips_created is not None:
            job.clips_created = clips_created
        if result:
            job.result = result
        if error:
            job.error = error

        await self.db.commit()

    async def save_clip(
        self,
        job_id: str,
        clip_index: int,
        clip_path: str,
        start_time: float,
        end_time: float,
        viral_score: int,
        hook: str,
        platform_content: dict,
    ) -> Clip:
        clip = Clip(
            job_id=job_id,
            clip_index=clip_index,
            clip_path=clip_path,
            start_time=start_time,
            end_time=end_time,
            viral_score=viral_score,
            hook=hook,
            platform_content=platform_content,
        )
        self.db.add(clip)
        await self.db.commit()
        await self.db.refresh(clip)
        return clip

    async def get_job(self, job_id: str) -> Job:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        return result.scalar_one_or_none()

    async def get_clips_by_job(self, job_id: str) -> list[Clip]:
        result = await self.db.execute(select(Clip).where(Clip.job_id == job_id))
        return result.scalars().all()
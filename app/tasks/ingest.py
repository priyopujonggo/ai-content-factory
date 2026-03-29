import os
import asyncio
from worker.celery_app import celery_app
from app.services.ingestion.downloader import VideoDownloader
from app.services.ai.transcriber import VideoTranscriber
from app.services.ai.clip_analyzer import ClipAnalyzer
from app.services.ai.content_generator import ContentGenerator
from app.services.processing.video_processor import VideoProcessor
from app.services.job_service import JobService
from app.core.database import AsyncSessionLocal


def run_async(coro):
    """Helper untuk jalankan coroutine dari dalam Celery task."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)


async def update_status(job_id: str, **kwargs):
    """Helper untuk update status job ke database."""
    async with AsyncSessionLocal() as db:
        job_service = JobService(db)
        await job_service.update_job_status(job_id, **kwargs)


async def save_clip_to_db(job_id: str, **kwargs):
    """Helper untuk simpan clip ke database."""
    async with AsyncSessionLocal() as db:
        job_service = JobService(db)
        await job_service.save_clip(job_id=job_id, **kwargs)


@celery_app.task(bind=True, name="tasks.ingest_video", max_retries=3)
def ingest_video_task(self, url: str, options: dict = None):
    opts = options or {}
    job_id = self.request.id

    print(f"[{job_id}] Pipeline started: {url}")

    try:
        # ── 1. Download ──────────────────────────────────
        run_async(update_status(job_id, status="started"))

        print(f"[{job_id}] Step 1: Downloading...")
        output_dir = os.path.join(os.getcwd(), "output")
        downloader = VideoDownloader(output_dir=output_dir)
        video_info = downloader.download(url=url, job_id=job_id)
        print(f"[{job_id}] Downloaded: {video_info['title']}")

        run_async(update_status(
            job_id,
            status="transcribing",
            video_title=video_info["title"],
        ))

        # ── 2. Transcribe ────────────────────────────────
        print(f"[{job_id}] Step 2: Transcribing...")
        transcriber = VideoTranscriber(model_name=opts.get("whisper_model", "base"))
        transcript = transcriber.transcribe(
            video_path=video_info["local_path"],
            language=opts.get("language", "auto"),
        )
        print(f"[{job_id}] Transcribed: {len(transcript['segments'])} segments")

        run_async(update_status(job_id, status="analyzing"))

        # ── 3. Analyze clips ─────────────────────────────
        print(f"[{job_id}] Step 3: Analyzing clips...")
        analyzer = ClipAnalyzer()
        clips = analyzer.analyze(
            segments=transcript["segments"],
            max_clips=opts.get("max_clips", 5),
            min_duration=opts.get("min_clip_duration", 30),
            max_duration=opts.get("max_clip_duration", 90),
        )
        print(f"[{job_id}] Found {len(clips)} clips")

        run_async(update_status(job_id, status="processing"))

        # ── 4. Process + generate content ────────────────
        print(f"[{job_id}] Step 4: Processing clips...")
        clips_dir = os.path.join(output_dir, job_id, "clips")
        processor = VideoProcessor(output_dir=clips_dir)
        generator = ContentGenerator()

        results = []
        for idx, clip in enumerate(clips, 1):
            print(f"[{job_id}] Clip {idx}/{len(clips)}...")

            output_name = f"clip_{idx:02d}_score{clip['viral_score']}.mp4"
            clip_path = processor.cut_clip(
                source_path=video_info["local_path"],
                start_time=clip["start_time"],
                end_time=clip["end_time"],
                output_name=output_name,
                portrait=True,
            )

            clip_text = " ".join(
                seg["text"] for seg in transcript["segments"]
                if clip["start_time"] <= seg["start"] <= clip["end_time"]
            )

            platforms = opts.get(
                "target_platforms",
                ["tiktok", "instagram_reels", "youtube_shorts"]
            )
            content = generator.generate_all_platforms(
                clip_text=clip_text,
                hook=clip["hook"],
                platforms=platforms,
            )

            # simpan clip ke database
            run_async(save_clip_to_db(
                job_id=job_id,
                clip_index=idx,
                clip_path=clip_path,
                start_time=clip["start_time"],
                end_time=clip["end_time"],
                viral_score=clip["viral_score"],
                hook=clip["hook"],
                platform_content=content,
            ))

            results.append({
                "clip_index": idx,
                "clip_path": clip_path,
                "viral_score": clip["viral_score"],
                "hook": clip["hook"],
                "platform_content": content,
            })

        # update job selesai
        run_async(update_status(
            job_id,
            status="success",
            clips_created=len(results),
            result={"clips": results},
        ))

        print(f"[{job_id}] Pipeline completed! {len(results)} clips ready.")
        return {
            "status": "success",
            "job_id": job_id,
            "video_title": video_info["title"],
            "clips_created": len(results),
            "clips": results,
        }

    except Exception as exc:
        print(f"[{job_id}] Pipeline failed: {exc}")
        run_async(update_status(job_id, status="failed", error=str(exc)))
        raise self.retry(exc=exc, countdown=60)
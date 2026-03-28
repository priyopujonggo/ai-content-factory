import yt_dlp
import os
from pathlib import Path


class VideoDownloader:
    def __init__(self, output_dir: str = "/tmp/content_factory"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download(self, url: str, job_id: str) -> dict:
        job_dir = self.output_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        output_template = str(job_dir / "%(title)s.%(ext)s")

        ydl_opts = {
            # coba format terbaik dulu, fallback ke single file kalau ffmpeg tidak ada
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": output_template,
            "quiet": False,
            "no_warnings": False,
            "merge_output_format": "mp4",
            # tambahan: install deno atau node untuk JS runtime, tapi ini workaround sementara
            "extractor_args": {"youtube": {"player_client": ["android"]}},
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            local_path = ydl.prepare_filename(info)

            if not local_path.endswith(".mp4"):
                local_path = os.path.splitext(local_path)[0] + ".mp4"

            return {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "description": info.get("description"),
                "upload_date": info.get("upload_date"),
                "channel": info.get("uploader"),
                "view_count": info.get("view_count"),
                "local_path": local_path,
                "job_dir": str(job_dir),
            }
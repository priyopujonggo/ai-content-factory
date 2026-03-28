import subprocess
from pathlib import Path


class VideoProcessor:
    def __init__(self, output_dir: str = "/tmp/content_factory"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def cut_clip(
        self,
        source_path: str,
        start_time: float,
        end_time: float,
        output_name: str,
        portrait: bool = True,
    ) -> str:
        output_path = self.output_dir / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        duration = end_time - start_time

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-i", source_path,
            "-t", str(duration),
            "-c:v", "libx264",
            "-c:a", "aac",
            "-movflags", "+faststart",
        ]

        if portrait:
            cmd += ["-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black"]

        cmd.append(str(output_path))

        print(f"Cutting clip: {start_time:.1f}s – {end_time:.1f}s → {output_name}")
        subprocess.run(cmd, check=True, capture_output=True)
        return str(output_path)
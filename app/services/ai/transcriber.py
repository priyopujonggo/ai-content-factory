import whisper
from pathlib import Path


class VideoTranscriber:
    def __init__(self, model_name: str = "base"):
        print(f"Loading Whisper model: {model_name} ...")
        self.model = whisper.load_model(model_name)
        print("Model loaded.")

    def transcribe(self, video_path: str, language: str = None) -> dict:
        print(f"Transcribing: {video_path}")

        options = {"word_timestamps": True}
        if language and language != "auto":
            options["language"] = language

        result = self.model.transcribe(str(video_path), **options)

        return {
            "text": result["text"],
            "language": result["language"],
            "segments": [
                {
                    "id": seg["id"],
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"].strip(),
                }
                for seg in result["segments"]
            ],
        }
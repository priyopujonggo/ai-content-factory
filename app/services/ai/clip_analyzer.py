import json
from groq import Groq
from app.core.config import settings


SYSTEM_PROMPT = """You are an expert social media content strategist specializing in short-form video.

Given a video transcript with timestamps, identify the most engaging segments 
that would perform well as short-form clips (30–90 seconds).

For each recommended clip return ONLY a JSON array with objects containing:
- start_time: float (seconds)
- end_time: float (seconds)
- viral_score: int 1–10
- hook: string (opening 5–8 words that grab attention)
- reason: string (why this segment is engaging, max 20 words)
- best_platforms: array of strings (youtube_shorts, instagram_reels, tiktok, twitter)

Rules:
- Each clip must be 30–90 seconds long
- Prioritize: strong hooks, emotional moments, surprising facts, actionable tips, humor
- Avoid: long intros, sponsor segments, off-topic tangents
- Return ONLY valid JSON array, no explanation outside the array"""


class ClipAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    def analyze(
        self,
        segments: list[dict],
        max_clips: int = 5,
        min_duration: int = 30,
        max_duration: int = 90,
    ) -> list[dict]:

        transcript_text = "\n".join(
            f"[{seg['start']:.1f}s – {seg['end']:.1f}s] {seg['text']}"
            for seg in segments
        )

        user_prompt = f"""Analyze this transcript and recommend up to {max_clips} clips.
Each clip must be {min_duration}–{max_duration} seconds long.

Transcript:
{transcript_text}

Return a JSON array only."""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=2000,
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        clips = json.loads(raw)
        return sorted(clips, key=lambda x: x.get("viral_score", 0), reverse=True)
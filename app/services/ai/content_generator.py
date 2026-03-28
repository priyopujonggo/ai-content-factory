import json
from groq import Groq
from app.core.config import settings


SYSTEM_PROMPT = """You are an expert social media copywriter.
Given a video clip transcript, hook, and target platform, generate optimized content.
Return ONLY valid JSON, no explanation outside the JSON object."""

PLATFORM_RULES = {
    "tiktok": "Short punchy caption max 150 chars. Hook in first line. 5–8 trending hashtags. Casual tone.",
    "instagram_reels": "Engaging caption 100–200 chars. Include emoji. 10–15 hashtags. Conversational tone.",
    "youtube_shorts": "Title max 60 chars, catchy. Caption 2–3 sentences. 5–8 hashtags. No emoji in title.",
    "twitter": "Tweet max 240 chars including hashtags. 2–3 hashtags max. Punchy and direct.",
}


class ContentGenerator:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    def generate(self, clip_text: str, platform: str, hook: str) -> dict:
        """
        Returns:
        {
            "title": "...",
            "caption": "...",
            "hashtags": ["#tag1", "#tag2"],
            "call_to_action": "..."
        }
        """
        rules = PLATFORM_RULES.get(platform, "Optimize for engagement.")

        user_prompt = f"""Platform: {platform}
Rules: {rules}
Hook: {hook}

Clip transcript:
{clip_text}

Generate content as JSON with keys: title, caption, hashtags (array), call_to_action."""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        return json.loads(raw)

    def generate_all_platforms(
        self, clip_text: str, hook: str, platforms: list[str]
    ) -> dict:
        """Generate content untuk semua platform sekaligus."""
        results = {}
        for platform in platforms:
            print(f"  Generating content for {platform}...")
            results[platform] = self.generate(
                clip_text=clip_text,
                platform=platform,
                hook=hook,
            )
        return results
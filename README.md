# AI Content Factory 🎬

Pipeline otomatis untuk mengubah video panjang menjadi short-form clips yang siap didistribusikan ke berbagai platform media sosial.

```
YouTube URL → Download → Transcribe → AI Clip Selection → Cut + Caption → Distribute
```

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI + Python 3.14 |
| Task Queue | Celery + Redis |
| Database | PostgreSQL + SQLAlchemy |
| Transcription | OpenAI Whisper |
| AI | Anthropic Claude API |
| Video Processing | FFmpeg + yt-dlp |
| Storage | Cloudflare R2 (S3-compatible) |
| Distribution | YouTube / Instagram / TikTok / Twitter API |

## Project Structure

```
ai-content-factory/
├── app/
│   ├── main.py                         # FastAPI entry point
│   ├── core/
│   │   ├── config.py                   # Settings via pydantic-settings
│   │   └── database.py                 # SQLAlchemy async engine
│   ├── api/v1/
│   │   ├── router.py                   # API router aggregator
│   │   └── endpoints/
│   │       ├── jobs.py                 # POST /jobs — submit URL
│   │       ├── clips.py                # GET /clips — list clips
│   │       ├── content.py              # GET /content — platform content
│   │       ├── platforms.py            # Platform OAuth management
│   │       └── webhooks.py             # Incoming webhooks
│   ├── services/
│   │   ├── ingestion/
│   │   │   ├── downloader.py           # yt-dlp wrapper ✅
│   │   │   └── storage.py              # S3/R2 upload
│   │   ├── ai/
│   │   │   ├── transcriber.py          # Whisper transcription ✅
│   │   │   ├── clip_analyzer.py        # Claude — pilih clip viral
│   │   │   └── content_generator.py    # Claude — caption + hashtag
│   │   ├── processing/
│   │   │   ├── video_processor.py      # FFmpeg cut + resize
│   │   │   ├── scene_detector.py       # PySceneDetect
│   │   │   └── caption_burner.py       # Burn SRT ke video
│   │   └── distribution/
│   │       ├── base.py                 # Abstract distributor
│   │       ├── youtube.py              # YouTube Shorts
│   │       ├── instagram.py            # Instagram Reels
│   │       ├── tiktok.py               # TikTok
│   │       └── twitter.py              # Twitter/X
│   ├── tasks/
│   │   ├── ingest.py                   # Pipeline orchestrator (Celery)
│   │   └── distribute.py               # Distribution task (Celery)
│   ├── models/                         # SQLAlchemy ORM models
│   └── schemas/                        # Pydantic request/response schemas
├── worker/
│   ├── celery_app.py                   # Celery config
│   └── beat_schedule.py                # Scheduled auto-posting
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Prerequisites

- Python 3.14+
- FFmpeg — `winget install ffmpeg` (Windows) / `brew install ffmpeg` (Mac)
- Node.js — untuk JS runtime yt-dlp
- Redis — untuk Celery task queue
- PostgreSQL

## Installation

```bash
# 1. Clone repo
git clone <repo-url>
cd ai-content-factory

# 2. Buat virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate
# Mac / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# edit .env dan isi API keys
```

## Environment Variables

Salin `.env.example` ke `.env` lalu isi:

```env
# AI
ANTHROPIC_API_KEY=sk-ant-...
WHISPER_MODEL=base

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/content_factory

# Redis
REDIS_URL=redis://localhost:6379/0

# Storage (Cloudflare R2 / AWS S3)
S3_ENDPOINT_URL=https://<ACCOUNT_ID>.r2.cloudflarestorage.com
S3_ACCESS_KEY_ID=
S3_SECRET_ACCESS_KEY=
S3_BUCKET_NAME=content-factory-media

# Platform APIs
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
INSTAGRAM_APP_ID=
INSTAGRAM_APP_SECRET=
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
TWITTER_API_KEY=
TWITTER_API_SECRET=
```

## Running

### Development (tanpa Docker)

```bash
# Terminal 1 — FastAPI server
uvicorn app.main:app --reload

# Terminal 2 — Celery worker
celery -A worker.celery_app worker --loglevel=info

# Terminal 3 — Celery beat (scheduler)
celery -A worker.celery_app beat --loglevel=info

# Terminal 4 — Flower (monitoring dashboard)
celery -A worker.celery_app flower
```

API docs tersedia di: `http://localhost:8000/docs`
Flower dashboard: `http://localhost:5555`

### Production (Docker)

```bash
docker compose up -d
```

## Usage

Submit video untuk diproses:

```bash
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtube.com/watch?v=XXXXX",
    "options": {
      "max_clips": 5,
      "min_clip_duration": 30,
      "max_clip_duration": 90,
      "target_platforms": ["tiktok", "instagram_reels"],
      "burn_captions": true
    }
  }'
```

Cek status job:

```bash
curl http://localhost:8000/api/v1/jobs/{job_id}
```

## Build Progress

### Phase 1 — Core Pipeline
- [x] `downloader.py` — download video via yt-dlp
- [x] `transcriber.py` — transkripsi audio via Whisper
- [ ] `clip_analyzer.py` — seleksi clip via Claude API
- [ ] `video_processor.py` — potong dan resize video via FFmpeg
- [ ] `tasks/ingest.py` — rangkai seluruh pipeline

### Phase 2 — Content Generation
- [ ] `content_generator.py` — generate caption dan hashtag per platform
- [ ] `caption_burner.py` — burn subtitle ke video
- [ ] `storage.py` — upload ke Cloudflare R2

### Phase 3 — Distribution
- [ ] `tiktok.py`
- [ ] `instagram.py`
- [ ] `youtube.py`
- [ ] `twitter.py`

### Phase 4 — Dashboard & Scheduling
- [ ] Database models + Alembic migrations
- [ ] Monitoring dashboard
- [ ] `beat_schedule.py` — auto-post terjadwal

## Contributing

1. Fork repo
2. Buat branch baru: `git checkout -b feat/nama-fitur`
3. Commit: `git commit -m "feat: deskripsi singkat"`
4. Push: `git push origin feat/nama-fitur`
5. Buat Pull Request

## License

MIT

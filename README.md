# AI Content Factory 🎬

Pipeline otomatis untuk mengubah video panjang menjadi short-form clips yang siap didistribusikan ke berbagai platform media sosial.

```
YouTube URL → Download → Transcribe → AI Clip Selection → Cut + Caption → Distribute
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

## Running

### Development

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


## License

MIT

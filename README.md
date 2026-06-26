# BrandSight

Brand visibility analysis for **Coca-Cola** vs **Pepsi** using custom YOLO11 detection, Supabase PostgreSQL + Storage, and AI-generated marketing reports.

## Quick start

### 1. Clone and install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Supabase

Step-by-step: **[docs/SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md)** (ISSUE-03)

1. Create a project at [supabase.com](https://supabase.com/)
2. Run `sql/schema.sql` in the SQL Editor
3. Run `sql/storage.sql` to create the `brandsight-crops` bucket
4. Copy the **Session pooler** connection string into `.env` as `DATABASE_URL`
5. Add `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` (Project Settings → API)

### 3. Verify database

```bash
python -m scripts.check_db
python -m scripts.check_storage
python -m scripts.test_db_insert   # round-trip insert into videos (ISSUE-04)
```

### 4. Add model weights

Place your fine-tuned `best.pt` in `models/` (Colab trains from the `yolo11l.pt` base checkpoint).

### 5. Run web app

```bash
streamlit run app/streamlit_app.py
```

## Project structure

```
app/                  Streamlit UI
src/
  config.py           Settings from .env
  db/                 Supabase connection + ORM models
  detect_image.py     Single-image inference CLI
  detect_video.py     Video inference CLI
  metrics.py          Visibility calculations
  metrics_export.py   Metrics JSON/text export CLI (#9)
  crops.py            Bbox crop extraction + Supabase Storage upload (#10)
  supabase_storage.py Supabase Storage client for crop uploads
  pipeline.py         End-to-end analysis orchestrator
  report/             AI marketing report generator
data/
  demo/               Demo videos
  crops/              Local crop cache (also uploaded to Supabase Storage)
  uploads/            Uploaded videos (runtime)
models/               best.pt (fine-tuned weights; training base: yolo11l.pt)
sql/schema.sql        Supabase schema (5 tables)
sql/storage.sql       Storage bucket `brandsight-crops` for crops
notebooks/            Colab training (to add)
docs/                 Project plans + Kanban
```

## CLI examples

```bash
# Image detection
python -m src.detect_image --image path/to/image.jpg

# Video detection (persists to Supabase when DATABASE_URL is set)
python -m src.detect_video --video data/demo/sample.mp4

# Skip database write
python -m src.detect_video --video data/demo/sample.mp4 --no-db

# Visibility metrics for a processed video (reads from Supabase)
python -m src.metrics_export --video-id 1
python -m src.metrics_export --video-id 1 --export

# Verify bbox crops on disk match detections.crop_path (#10)
python -m scripts.verify_crops --video-id 1

# Full pipeline (video → DB → metrics → report)
python -c "from pathlib import Path; from src.pipeline import analyze_video; print(analyze_video(Path('data/demo/sample.mp4')))"
```

## Visibility metrics (#9)

Detection runs every **`SAMPLE_STRIDE`** frames (default `3`, set in `.env`).
Per-brand **visible seconds** = unique sampled frames with a detection × `(stride / fps)`.
**Visibility %** = `visible_seconds / video_duration × 100`.
**Balance label:** `balanced` if gap &lt; 5% of duration; else `coca_cola_dominant` or `pepsi_dominant`.

`detect_video` writes `brand_summary` and `competitive_analysis` when persisting to Supabase.
Exported files: `data/outputs/metrics_{video_id}.json` and `.txt`.

## Bbox crops (#10)

Each detection bbox is cropped from the source video, cached under `data/crops/{video_id}/`, and uploaded to Supabase Storage (`brandsight-crops`). The `storage:…` URI is stored in `detections.crop_path`. Streamlit shows signed URLs for crop thumbnails.

```bash
python -m scripts.check_storage
python -m src.detect_video --video data/demo/demo1.mp4
python -m scripts.verify_crops --video-id <id>
```

## Docker

```bash
docker build -t brandsight .
docker run -p 8501:8501 --env-file .env brandsight
```

## Deploy (Streamlit Cloud) — #13

**Runbook:** **[docs/DEPLOY.md](docs/DEPLOY.md)**

```bash
python -m scripts.smoke_deploy   # pre-flight before deploy
```

1. Push repo to GitHub (`models/best.pt` must be on the branch)
2. [share.streamlit.io](https://share.streamlit.io) → New app → `app/streamlit_app.py`
3. Paste secrets (see `.streamlit/secrets.toml.example`) — `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `GEMINI_API_KEY`, etc.
4. Deploy → verify sidebar **Supabase connected** → upload a short MP4 and run analysis

**Live demo:** _add URL after deploy, e.g. `https://brandsight-equipo1.streamlit.app`_

## Team docs

- [Project plan](docs/PROJECT_PLAN.md)
- [Plan (ES)](docs/PLAN_PROYECTO.md)
- [Kanban](docs/KANBAN.md)
- [Supabase setup](docs/SUPABASE_SETUP.md)
- [Cloud deploy (#13)](docs/DEPLOY.md)
- [Roboflow dataset](docs/ROBOFLOW_DATASET.md)
- [Briefing](docs/BRIEFING_README.md)

## Brands (YOLO classes)

| Class ID | Name |
|----------|------|
| 0 | `coca_cola` |
| 1 | `pepsi` |

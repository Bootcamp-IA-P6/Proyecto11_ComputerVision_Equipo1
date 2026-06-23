# BrandSight

Brand visibility analysis for **Coca-Cola** vs **Pepsi** using custom YOLO detection, Supabase PostgreSQL, and AI-generated marketing reports.

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
3. Copy the **Session pooler** connection string into `.env` as `DATABASE_URL`

### 3. Verify database

```bash
python -m scripts.check_db
python -m scripts.test_db_insert   # round-trip insert into videos (ISSUE-04)
```

### 4. Add model weights

Place your fine-tuned `best.pt` in `models/` (from Google Colab training).

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
  pipeline.py         End-to-end analysis orchestrator
  report/             AI marketing report generator
data/
  demo/               Demo videos
  crops/              Saved logo crops
  uploads/            Uploaded videos (runtime)
models/               best.pt (not in Git)
sql/schema.sql        Supabase schema (5 tables)
sql/storage.sql       Optional Storage bucket for crops
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

# Full pipeline (video → DB → report)
python -c "from src.pipeline import analyze_video; analyze_video(__import__('pathlib').Path('data/demo/sample.mp4'))"
```

## Docker

```bash
docker build -t brandsight .
docker run -p 8501:8501 --env-file .env brandsight
```

## Deploy (Streamlit Cloud)

1. Push repo to GitHub
2. [share.streamlit.io](https://share.streamlit.io) → New app → `app/streamlit_app.py`
3. Add secrets: `DATABASE_URL`, `GEMINI_API_KEY`, `MODEL_PATH=models/best.pt`
4. Include `best.pt` in repo or download at startup (document your approach)

## Team docs

- [Project plan](docs/PROJECT_PLAN.md)
- [Plan (ES)](docs/PLAN_PROYECTO.md)
- [Kanban](docs/KANBAN.md)
- [Supabase setup](docs/SUPABASE_SETUP.md)
- [Roboflow dataset](docs/ROBOFLOW_DATASET.md)
- [Briefing](docs/BRIEFING_README.md)

## Brands (YOLO classes)

| Class ID | Name |
|----------|------|
| 0 | `coca_cola` |
| 1 | `pepsi` |

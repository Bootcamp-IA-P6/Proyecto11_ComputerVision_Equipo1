# Project Plan — BrandSight (Coca-Cola vs Pepsi)

Brand visibility analysis web application: detect logos in video, compare screen time, persist results in a **cloud database**, and generate an AI marketing report for the Coca-Cola client.

**Constraints:** 6 days · 3 teammates · Linux / Mac / Windows · training on **Google Colab** · **deployed** web app

Related docs: [BRIEFING_README.md](./BRIEFING_README.md) · [PLAN_PROYECTO.md](./PLAN_PROYECTO.md) (Spanish) · [KANBAN.md](./KANBAN.md)

---

## Project Summary

| Item | Detail |
|------|--------|
| **Product name** | BrandSight (working title) |
| **Client** | Coca-Cola |
| **Competitor** | Pepsi |
| **Goal** | Measure and compare brand visibility in video content |
| **Core stack** | YOLOv8 · OpenCV · **Supabase** (PostgreSQL) · Streamlit · LLM API · Cloud deploy |

### Pipeline

```
Upload video → YOLO detects Coca-Cola & Pepsi (frame by frame)
    → Calculate visibility metrics → Save to Supabase (+ crop files)
    → LLM generates Coca-Cola marketing report → Display in web app
```

---

## Main Objective

Build a proof-of-concept **brand visibility analyzer** that:

1. Detects **Coca-Cola** and **Pepsi** logos in uploaded videos using a custom fine-tuned YOLO model
2. Calculates per-brand screen time, percentages, detection counts, and competitive dominance
3. Persists all analysis data in **Supabase** (managed PostgreSQL in the cloud)
4. Generates an **AI marketing report** from stored metrics (Coca-Cola analyst perspective)
5. Delivers everything through a **deployed Streamlit web application**

**Demo success criteria:** upload a 30–60s video → annotated output → metrics dashboard → competitive comparison → AI report — all running on the **live deployed URL**.

---

## Alignment with Briefing

| Briefing requirement | BrandSight |
|---------------------|------------|
| Custom logo detection in video | ✅ YOLO — Coca-Cola + Pepsi |
| Time on screen + percentage | ✅ Per-brand seconds and % |
| Save detections in database | ✅ Supabase (PostgreSQL) |
| Multi-brand model (Advanced) | ✅ 2 classes |
| Confidence % (Advanced) | ✅ On overlay + in DB |
| Bbox crops (Advanced) | ✅ Saved to cloud/local storage, path in DB |
| Web front (Expert) | ✅ Streamlit — deployed |
| Cloud / API (Expert) | ✅ Deployed app + optional FastAPI endpoint |

---

## Realistic 6-Day Target

| Level | Verdict |
|-------|---------|
| Essential | **Must ship** (Day 1–2) |
| Medium | **Must ship** (Day 2–3) |
| Advanced | **Must ship** (Day 3–4) |
| Expert | **Target** — deployed web app; skip separate microservice API unless spare time |

**Do not chase:** perfect model accuracy, 10+ brands, custom React frontend, Celery job queues.

---

## Team Roles (3 people, dual hats)

Everyone codes. PO and SM are **part-time hats**.

| Person | Primary | Secondary | Deliverables |
|--------|---------|-----------|--------------|
| **A — Product Owner** | Scope, demo script, presentation, AI report prompt | Frontend / deploy | Streamlit UI, marketing prompt, slides, acceptance criteria |
| **B — Scrum Master** | Daily, Kanban, Git/PR, deployment & env | Backend / pipeline | `detect_video.py`, `report.py`, DB layer, Docker, deploy config |
| **C — ML Engineer** | Dataset, Colab training, model quality | Inference | Roboflow, `train_colab.ipynb`, `detect_image.py`, `models/best.pt` |

**Rotate SM** when B is blocked on ML.

**Ceremonies:** 15-min daily · PO guards scope · SM merges PRs same day

**Workload note:** ML Engineer is the critical path (labeling + training). PO and SM must help label from Day 1.

---

## Cross-OS Strategy

| Problem | Solution |
|---------|----------|
| GPU / CUDA differences | Train **only in Google Colab** |
| Python deps | Single `requirements.txt`, Python 3.10–3.11 |
| Paths | `pathlib.Path` everywhere |
| Line endings | `.gitattributes` → `* text=auto` |
| Model weights | Team Google Drive — not in Git (use Git LFS only if needed) |
| DB differences local vs cloud | **Same Supabase project** via `DATABASE_URL`; `.env` locally, secrets in deploy platform |

**Shared artifacts (outside Git):**
```
Team Drive/
├── datasets/           # Roboflow YOLO export
├── models/best.pt
└── demo_videos/        # 2–3 clips (both brands visible)
```

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Streamlit Web App (deployed — Streamlit Cloud / Railway)   │
│  Upload · Metrics · Charts · AI Report                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  Analysis Pipeline (Python)                                 │
│  OpenCV → YOLO (coca_cola, pepsi) → Metrics → Crop saver    │
└──────────────┬─────────────────────────┬────────────────────┘
               │                         │
┌──────────────▼──────────┐   ┌──────────▼────────────────────┐
│  Supabase PostgreSQL    │   │  Supabase Storage (optional)  │
│  videos · detections    │   │  bucket: brandsight-crops     │
│  summaries · reports    │   │  videos · crops · reports     │
└─────────────────────────┘   └─────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│  LLM API (Gemini / OpenAI) — marketing report generation    │
└─────────────────────────────────────────────────────────────┘

Training (offline): Roboflow → Google Colab → best.pt → Drive → deploy bundle
```

### Tech Stack

| Layer | Choice |
|-------|--------|
| Detection | Ultralytics YOLOv8 (`yolov8n` or `yolov8s`) |
| Training | Google Colab + Roboflow |
| Video | OpenCV |
| Database | **Supabase** (PostgreSQL — free tier) |
| ORM | SQLAlchemy |
| Migrations | Alembic (optional) or SQL init script |
| Web UI | Streamlit |
| AI report | Gemini API or OpenAI (single prompt call) |
| Deploy | **Streamlit Community Cloud** or **Railway** |
| Secrets | Platform env vars + `.env` locally (never commit) |
| Container | Dockerfile (Railway / reproducibility) |

---

## Supabase Setup (Day 1 — SM)

1. Create a project at [supabase.com](https://supabase.com/) (free tier)
2. **SQL Editor** → run `sql/schema.sql` from this repo
3. **Project Settings → Database** → copy the **Connection string** (URI mode)
4. Use the **Session pooler** string for Streamlit / server apps
5. Share `DATABASE_URL` with the team via secure channel (not Git)
6. *(Optional)* **Storage** → create bucket `brandsight-crops` (public or signed URLs)

**Connection string format:**
```
postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres
```

**SQLAlchemy** (if needed):
```
postgresql+psycopg2://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres
```

**Verify:** Table Editor should show `videos`, `detections`, `brand_summary`, `competitive_analysis`, `marketing_reports`.

---

## Database Schema (Supabase / PostgreSQL)

Schema file: [`sql/schema.sql`](../sql/schema.sql)

```sql
CREATE TABLE videos (
    id              SERIAL PRIMARY KEY,
    filename        VARCHAR(255) NOT NULL,
    storage_path    TEXT NOT NULL,
    duration_sec    DOUBLE PRECISION NOT NULL,
    fps             DOUBLE PRECISION,
    total_frames    INTEGER,
    annotated_path  TEXT,
    status          VARCHAR(20) DEFAULT 'pending',
    processed_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE detections (
    id              SERIAL PRIMARY KEY,
    video_id        INTEGER NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    brand           VARCHAR(50) NOT NULL,       -- 'coca_cola' | 'pepsi'
    confidence      DOUBLE PRECISION NOT NULL,
    frame_number    INTEGER NOT NULL,
    timestamp_sec   DOUBLE PRECISION NOT NULL,
    bbox_x          DOUBLE PRECISION NOT NULL,
    bbox_y          DOUBLE PRECISION NOT NULL,
    bbox_w          DOUBLE PRECISION NOT NULL,
    bbox_h          DOUBLE PRECISION NOT NULL,
    crop_path       TEXT
);

CREATE TABLE brand_summary (
    id              SERIAL PRIMARY KEY,
    video_id        INTEGER NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    brand           VARCHAR(50) NOT NULL,
    visible_seconds DOUBLE PRECISION NOT NULL,
    visibility_pct  DOUBLE PRECISION NOT NULL,
    detection_count INTEGER NOT NULL,
    avg_confidence  DOUBLE PRECISION,
    UNIQUE (video_id, brand)
);

CREATE TABLE competitive_analysis (
    id                  SERIAL PRIMARY KEY,
    video_id            INTEGER NOT NULL REFERENCES videos(id) ON DELETE CASCADE UNIQUE,
    dominant_brand      VARCHAR(50) NOT NULL,
    coca_cola_seconds   DOUBLE PRECISION NOT NULL,
    pepsi_seconds       DOUBLE PRECISION NOT NULL,
    coca_cola_pct       DOUBLE PRECISION NOT NULL,
    pepsi_pct           DOUBLE PRECISION NOT NULL,
    visibility_gap_sec  DOUBLE PRECISION NOT NULL,
    balance_label       VARCHAR(30) NOT NULL
);

CREATE TABLE marketing_reports (
    id              SERIAL PRIMARY KEY,
    video_id        INTEGER NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    model_name      VARCHAR(100),
    prompt_version  VARCHAR(20),
    report_text     TEXT NOT NULL,
    report_path     TEXT,
    generated_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_detections_video_id ON detections(video_id);
CREATE INDEX idx_detections_brand ON detections(brand);
```

### Visibility calculation

```
frame_interval = 1 / fps   (× sample_stride if skipping frames)

Per sampled frame:
  if coca_cola detected (conf ≥ 0.5) → coca_frames += 1
  if pepsi detected     (conf ≥ 0.5) → pepsi_frames += 1

visible_seconds = frames × frame_interval × sample_stride
visibility_pct  = (visible_seconds / duration_sec) × 100

dominant_brand  = higher visible_seconds
balance_label   = 'balanced' if gap < 5% of duration, else '{winner}_dominant'
```

---

## AI Report Generation

**Input:** JSON from `brand_summary` + `competitive_analysis` (not raw video).

**System prompt:**
> You are a brand visibility analyst working for Coca-Cola. Write a concise marketing report using only the provided metrics. Be professional and data-driven. Do not invent numbers.

**Report sections:**
1. Executive Summary
2. Coca-Cola Visibility
3. Pepsi Competitive Visibility
4. Competitive Comparison
5. Marketing Insights (2–3 bullets)
6. Recommendation for Coca-Cola

**Fallback:** Jinja2 template if LLM API unavailable at demo time.

**Module:** `src/report/generate_marketing_report.py` → saves to `marketing_reports` table.

---

## Web App Features (Streamlit)

| Section | Features |
|---------|----------|
| Upload | MP4 uploader + demo video selector |
| Processing | Progress bar, status from DB |
| Video results | Annotated output player |
| Metrics | Duration, seconds/%, detection count per brand |
| Comparison | Bar chart, dominant brand badge |
| Detections | Table + crop thumbnails |
| AI Report | Rendered markdown + copy/download |
| History | Past analyses from Supabase |

---

## Scope Decisions

| Decision | Choice |
|----------|--------|
| Brands | Coca-Cola + Pepsi only |
| Images per brand | 80–120 annotated |
| Demo video | 30–60 seconds |
| Frame sampling | Every 3rd–5th frame (document in README) |
| Database | **Supabase** (PostgreSQL) |
| File storage | Supabase Storage bucket or app temp dir + DB paths |
| Frontend | Streamlit only |
| Deploy | Streamlit Cloud or Railway |
| LLM | Gemini free tier or OpenAI |

---

## 6-Day Sprint Plan

### Day 1 — Setup, data, cloud infra, first train

| Who | Tasks |
|-----|--------|
| PO | Finalize Coca-Cola/Pepsi scope, user stories, GitHub Project board |
| SM | Repo skeleton, branches, `requirements.txt`, `.gitignore`, `.env.example` |
| SM | **Create Supabase project**, run `sql/schema.sql`, share `DATABASE_URL` with team |
| ML | Roboflow project, ~50 images/brand, start labeling |
| All | 30-min planning: definition of done |

**End of day:** Supabase live · 50+ labeled images · Colab smoke train (10 epochs)

---

### Day 2 — Essential DONE

| Who | Tasks |
|-----|--------|
| ML | Finish labeling, full Colab train, `best.pt` → Drive |
| Backend | `detect_image.py`, DB connection module, test insert on all OS |
| PO | README: setup, env vars, how to run |

**End of day:** Single-image detection with bbox + brand label · DB connection works locally

---

### Day 3 — Medium DONE

| Who | Tasks |
|-----|--------|
| Backend | `detect_video.py` — annotated MP4, labels + confidence on overlay |
| ML | Retrain if needed; add hard frames from demo videos |
| PO/SM | Record 2 demo videos (both brands); update Kanban |

**End of day:** 30s annotated video demo · data written to Supabase

---

### Day 4 — Advanced DONE

| Who | Tasks |
|-----|--------|
| Backend | `report.py` — visibility metrics, `brand_summary`, `competitive_analysis` |
| Backend | Save bbox crops, store paths in `detections` |
| ML | Final 2-class Colab train if metrics weak |
| Backend | `generate_marketing_report.py` — LLM call + DB insert |

**End of day:** Full metrics + competitive analysis + AI report in DB

---

### Day 5 — Web app + deployment

| Who | Tasks |
|-----|--------|
| PO | Streamlit UI: upload → pipeline → metrics + chart + AI report |
| SM | `Dockerfile`, deploy to **Streamlit Cloud or Railway** |
| SM | Configure deploy secrets: `DATABASE_URL`, `GEMINI_API_KEY` / `OPENAI_API_KEY` |
| ML | Final model check on deployed app |
| All | Dry-run on **live URL** (15 min) |

**End of day:** Public/deployed URL working end-to-end

---

### Day 6 — Buffer + delivery

| Who | Tasks |
|-----|--------|
| All | Fix deploy bugs, cross-OS issues, video codec on Windows |
| PO | Presentation: problem → architecture → demo on live URL → limitations |
| SM | Kanban closed, tag `v1.0-demo`, README deploy section |
| All | Final rehearsal |

**End of day:** Live demo + presentation ready

---

## Kanban Cards

Full board with issues, descriptions, and assignees: **[KANBAN.md](./KANBAN.md)**

```
Backlog → To Do → In Progress → In Review → Done
```

1. Roboflow dataset (Coca-Cola + Pepsi) — **C**
2. Supabase schema + connection layer — **B**
3. Colab training notebook — **C**
4. Image detection — **C**
5. Video detection + labels + confidence — **B**
6. Visibility metrics + competitive analysis — **B**
7. Bbox crops + DB persistence — **B**
8. AI marketing report generator — **A**
9. Streamlit web app — **A**
10. **Cloud deployment** — **B**
11. README + presentation — **A**

---

## Risk Register

| Risk | Mitigation |
|------|------------|
| Labeling too slow | All 3 label; 2 brands only; Roboflow auto-label + fix |
| Colab disconnect | Checkpoints to Drive every 10 epochs |
| DB connection fails on deploy | Test `DATABASE_URL` from deploy platform Day 1 |
| Supabase free tier limits | Short demo videos; sample frames |
| LLM API down at demo | Jinja2 template fallback |
| Model weak on video | Fine-tune on demo video frames |
| Windows codec issues | H.264 MP4; test Day 3 |
| Deploy breaks on Day 5 | Start deploy config Day 1 (empty app + DB ping) |

---

## Repo Layout

```
ai-computer-vision-objects/
├── app/
│   └── streamlit_app.py
├── data/
│   └── demo/                 # small sample videos (gitignored if large)
├── docs/
│   ├── BRIEFING_README.md
│   ├── PROJECT_PLAN.md
│   └── PLAN_PROYECTO.md
├── models/                   # best.pt (gitignored — bundled at deploy)
├── notebooks/
│   └── train_colab.ipynb
├── src/
│   ├── db/
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── repository.py
│   ├── detect_image.py
│   ├── detect_video.py
│   ├── metrics.py
│   └── report/
│       └── generate_marketing_report.py
├── sql/
│   └── schema.sql
├── .env.example
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Environment Variables

```bash
# .env.example — never commit real values
# Supabase → Project Settings → Database → Connection string (URI)
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres

# Optional — Supabase Storage for crops/videos
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

GEMINI_API_KEY=your_key_here          # or OPENAI_API_KEY
MODEL_PATH=models/best.pt
CONFIDENCE_THRESHOLD=0.5
SAMPLE_STRIDE=3
```

---

## Presentation Description (copy-ready)

**Short pitch:**

> **BrandSight** analyzes video content to measure brand visibility for **Coca-Cola** against competitor **Pepsi**. A custom YOLO model detects both logos frame by frame, calculates screen time and competitive dominance, stores every result in **Supabase**, and generates an AI marketing report — all through a **deployed web application**.

**Slide structure:**
1. Problem — clients need visibility metrics vs competitors
2. Solution — BrandSight pipeline
3. Architecture — YOLO + Supabase + Streamlit + LLM
4. Demo — live URL walkthrough
5. Tech stack & training (Colab, augmentations)
6. Limitations & future work (more brands, API, real-time)

---

## References

- [Bootcamp roadmap](https://roadmap-mad-ai-p4.coderf5.es/)
- [Ultralytics YOLO docs](https://docs.ultralytics.com/)
- [Supabase](https://supabase.com/) · [Supabase SQL Editor](https://supabase.com/docs/guides/database/overview)
- [Streamlit Cloud deploy](https://docs.streamlit.io/streamlit-community-cloud)

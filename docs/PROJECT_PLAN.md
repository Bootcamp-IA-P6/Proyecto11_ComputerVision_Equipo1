# Project Plan — Computer Vision Logo Detection

Realistic plan for **6 days**, **3 teammates**, **Linux / Mac / Windows** environments, with training on **Google Colab**.

Related docs: [BRIEFING_README.md](./BRIEFING_README.md) · [PLAN_PROYECTO.md](./PLAN_PROYECTO.md) (Spanish version)

---

## Realistic Target (define on Day 1)

With 6 days and 3 people, the achievable goal is **Medium + most of Advanced** — not full Expert (cloud API + production deploy).

| Level | 6-day verdict |
|-------|----------------|
| Essential | **Must ship** (Day 1–2) |
| Medium | **Must ship** (Day 2–3) |
| Advanced | **Target** — 2 brands, confidence %, SQLite, crops, time on screen |
| Expert | **Partial only** — Streamlit upload UI; skip cloud API unless Day 5 has spare time |

**Do not chase:** FastAPI + Celery + cloud deploy + perfect multi-brand accuracy. One working demo beats an unfinished “expert” stack.

---

## Team Roles (3 people, dual hats)

Everyone codes. PO and Scrum Master are **part-time hats**, not full-time non-coders.

| Person | Primary hat | Secondary hat | Main deliverables |
|--------|-------------|---------------|-------------------|
| **A — Product Owner** | Scope, priorities, demo script, presentation story | Frontend | `app/streamlit_app.py`, slides outline, acceptance criteria |
| **B — Scrum Master** | Daily standup, Kanban, blockers, Git/PR flow | Backend / pipeline | `detect_video.py`, `report.py`, SQLite, Docker, README |
| **C — ML Engineer** | Dataset, Colab training, model quality | Inference scripts | Roboflow, `notebooks/train_colab.ipynb`, `detect_image.py`, `models/best.pt` |

**Rotate SM** if B is blocked on ML work — whoever is least busy that day runs the 15-min standup.

**Ceremonies (lightweight):**
- **Daily standup:** 15 min — yesterday / today / blockers
- **PO:** keeps backlog ordered; says “no” to scope creep
- **SM:** moves Kanban cards; ensures PRs merge same day

---

## Cross-OS Strategy (Linux / Mac / Windows)

**Rule:** train in **one place** (Colab), run inference in **one portable way** (Python + shared files).

| Problem | Solution |
|---------|----------|
| Different GPUs / CUDA | **Train only in Google Colab** — no local GPU setup |
| Python deps differ | Single `requirements.txt`, Python **3.10 or 3.11** for everyone |
| Path separators | Use `pathlib.Path` everywhere |
| Line endings | `.gitattributes` with `* text=auto` |
| Model weights too big for Git | **Google Drive shared folder** or Git LFS — never commit `.pt` without LFS |
| “Works on my machine” | Optional **Docker** for inference only (Day 5); not required for training |

**Shared artifacts (outside Git):**
```
Team Drive/
├── datasets/          # Roboflow export zip
├── models/best.pt     # after each Colab run
└── demo_videos/       # 2–3 short test clips
```

**Local setup (all OS, same commands):**
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.detect_video --video data/demo/sample.mp4 --weights models/best.pt
```

---

## Google Colab Workflow (recommended)

Colab is the right call for a 6-day sprint.

```
Roboflow (annotate) → export YOLO zip
        ↓
Colab notebook (train) → best.pt → Team Google Drive
        ↓
Everyone downloads best.pt → models/
        ↓
Local/Streamlit inference (CPU OK for demo clips)
```

**Colab notebook checklist:**
1. Install `ultralytics`
2. Download dataset (Roboflow API key in Colab secrets — not in repo)
3. Train `yolov8n.pt` (fast) or `yolov8s.pt` if logos are small
4. Enable augmentations: flip, mosaic, HSV (built into YOLO — mention in presentation)
5. Save `best.pt` to Drive
6. Quick validation on 2–3 test images in the notebook

**Important:** commit the notebook to Git; **do not** commit datasets or weights.

---

## Scope Decisions (save days)

| Decision | Recommendation |
|----------|----------------|
| Number of brands | **2** (not 4+) — e.g. Nike + Coca-Cola |
| Images per brand | **80–150** annotated (Roboflow + augment → ~300+) |
| Video length for demo | **30–60 seconds** per clip |
| Frame processing | Every **3rd–5th** frame for speed; document assumption |
| Database | **SQLite** (file works on all OS) |
| Frontend | **Streamlit only** (not React) |
| Cloud API | **Skip** or “lite”: deploy Streamlit on **Streamlit Community Cloud** (free) |
| Docker | Simple `Dockerfile` for inference if time on Day 5 |

---

## 6-Day Sprint Plan

### Day 1 — Setup + data + first train
**Goal:** Essential path started; Kanban live; repo skeleton.

| Who | Tasks |
|-----|--------|
| PO | Pick 2 brands, write user stories, create GitHub Project / Trello |
| SM | Repo structure, branches (`main`, `develop`), `requirements.txt`, `.gitignore`, `.gitattributes` |
| ML | Roboflow project, collect ~50 imgs/brand, start labeling |
| All | 30-min planning: definition of done per level |

**End of day:** 50+ labeled images, Colab notebook runs 10-epoch smoke train.

---

### Day 2 — Essential DONE
**Goal:** One image → bounding box + brand name.

| Who | Tasks |
|-----|--------|
| ML | Finish labeling, full Colab train, export `best.pt` to Drive |
| Backend | `detect_image.py`, download weights, test on 3 OS |
| PO | README: setup, how to run, dataset description |

**End of day:** Demo on **single image** from any teammate’s laptop.

---

### Day 3 — Medium DONE
**Goal:** Video in → annotated video out + label under each box.

| Who | Tasks |
|-----|--------|
| Backend | `detect_video.py` (OpenCV + Ultralytics), save output MP4 |
| ML | Retrain if Day 2 mAP poor; add hard examples from video frames |
| PO/SM | Record 2 demo videos; update Kanban |

**End of day:** 30s video with boxes + class names visible.

---

### Day 4 — Advanced (core)
**Goal:** Time on screen + confidence + DB.

| Who | Tasks |
|-----|--------|
| Backend | `report.py`: seconds + % per brand; SQLite schema + insert |
| ML | Multi-class dataset (2 brands), retrain in Colab |
| Backend | Save bbox crops to `data/crops/` + paths in DB |
| All | Show confidence % on video overlay (`conf` in Ultralytics plot) |

**End of day:** JSON/text report + SQLite file + crops folder.

---

### Day 5 — Advanced polish + Expert-lite
**Goal:** Streamlit + presentation draft.

| Who | Tasks |
|-----|--------|
| PO/Frontend | Streamlit: upload video → run pipeline → show report + table |
| SM | Dockerfile (optional), clean README, branch merge to `main` |
| ML | Final model pass; prepare 3 slides on training/augmentation |
| All | Dry-run demo (15 min) |

**End of day:** Streamlit works locally; optional deploy to Streamlit Cloud.

---

### Day 6 — Buffer + delivery
**Goal:** Nothing new — fix, rehearse, document.

- Fix OS-specific bugs (paths, video codec)
- Presentation: problem → dataset → YOLO fine-tune → pipeline → demo → limitations
- Kanban: all cards Done or Won’t Do with reason
- Tag release `v1.0-demo`

---

## Kanban Columns (keep it simple)

```
Backlog → To Do → In Progress → In Review → Done
```

**Minimum cards:**
1. Dataset + Roboflow
2. Colab training notebook
3. Image detection
4. Video detection + labels
5. Time / % report
6. SQLite + crops
7. Streamlit UI
8. README + presentation

---

## Risk Register

| Risk | Mitigation |
|------|------------|
| Labeling too slow | Start with 2 brands; Roboflow auto-label + manual fix |
| Colab disconnect | Save checkpoints to Drive every 10 epochs |
| Model bad on video | Fine-tune on frames extracted from your demo videos |
| Windows video codec issues | Use `.mp4` H.264; test Day 3 on Windows machine |
| Someone blocked on setup | SM pairs 30 min; Colab removes GPU pain |
| Scope creep to Expert | PO freezes backlog after Day 3 lunch |

---

## Presentation Talking Points (evaluation criteria)

Explicitly mention:
- **Preprocessing:** YOLO resize/normalize (640px), your frame sampling
- **Custom dataset:** Roboflow, YOLO format, train/val split
- **Pretrained + fine-tune:** `yolov8n.pt` → your logos
- **Augmentations:** flip, mosaic, HSV in training config
- **“Real-time”:** optional — show FPS on laptop or say “batch analysis, not live stream”
- **DB:** SQLite schema + crops

---

## Tech Stack

Recommended technologies for the brand logo detection project, mapped to delivery levels and evaluation criteria.

### Core Principle

Use **one detection framework end-to-end** (train → infer on images/video → export metrics) instead of mixing TensorFlow + PyTorch + Detectron2. That keeps the demo, database schema, and deployment simpler.

---

### 1. Detection Model — YOLO via Ultralytics (PyTorch)

| Option | Verdict |
|--------|---------|
| **YOLOv8 / YOLO11 (Ultralytics)** | **Best default** — fast to train, good docs, multi-class, confidence scores, video inference built-in |
| Faster R-CNN / Detectron2 | Strong accuracy, heavier setup; overkill for logo PoC |
| SSD | Middle ground; less ecosystem support than YOLO today |
| TensorFlow/Keras | Fine if the team already knows it; otherwise adds friction |

**Why YOLO fits this brief:**

- **Essential:** single-image detection with bounding boxes
- **Medium:** video frame-by-frame processing
- **Advanced:** confidence %, multi-brand (multi-class), crops from boxes
- **Evaluation:** pretrained backbone + fine-tune, augmentation in training config, real-time optional at inference

```
Pretrained: yolov8n.pt (fast demo) or yolov8s.pt (better accuracy)
Fine-tune on your logo dataset (YOLO format)
```

---

### 2. Language & CV Libraries

| Layer | Choice | Role |
|-------|--------|------|
| **Python 3.10+** | Main language | Training, pipeline, API, UI |
| **Ultralytics** | Training + inference | Model lifecycle |
| **OpenCV** | Video I/O, frame extraction, optional overlay | Required for video pipeline |
| **Pillow** | Image crops for DB | Save bounding-box crops |
| **Albumentations** (optional) | Custom augmentations beyond YOLO defaults | flip, color jitter, crop — hits evaluation criteria explicitly |
| **pandas** | Aggregations | Per-brand time on screen, % of video |

**Skip for v1 unless needed:** scikit-image (OpenCV + Pillow cover most cases).

---

### 3. Dataset & Annotation

| Tool | Use |
|------|-----|
| **Roboflow** (free tier) | Annotate boxes, export YOLO format, built-in augmentations |
| **Label Studio** / **CVAT** | Self-hosted alternative |
| **Manual collection** | Screenshots from ads, sports broadcasts, YouTube frames (watch licensing) |

**Brands for PoC:** pick 2–4 visually distinct logos (e.g. Nike, Coca-Cola, McDonald's) — easier to demo multi-class than 10 similar marks.

**Format:** YOLO txt labels (`class x_center y_center width height` normalized).

---

### 4. Video Analysis Pipeline

```
Video → OpenCV read frames → YOLO predict (conf threshold) →
track presence per frame → aggregate time per brand → report + DB insert
```

| Component | Recommendation |
|-----------|----------------|
| Frame sampling | Every frame for accuracy; every Nth frame for speed in demo |
| Temporal logic | Simple: brand "on screen" if detected in frame; optional IoU tracking (ByteTrack in Ultralytics) for stability |
| Output report | JSON + human-readable summary: seconds, % of duration, frame count |
| Annotated video | Optional `result.save()` from Ultralytics for demo |

---

### 5. Database — SQLite → PostgreSQL

For Advanced level, a minimal schema:

| Table | Fields (example) |
|-------|------------------|
| `videos` | id, filename, duration_sec, processed_at |
| `detections` | id, video_id, brand, confidence, timestamp_sec, bbox, crop_path |
| `video_summary` | video_id, brand, total_seconds, percentage |

| Tier | DB |
|------|-----|
| PoC / local | **SQLite** + SQLAlchemy |
| Expert / cloud | **PostgreSQL** (same ORM, easy migration) |

Store crop images on disk (`data/crops/{video_id}/`) and paths in DB — not blobs in SQLite unless required.

---

### 6. Frontend — Streamlit (Expert Level)

| Option | When |
|--------|------|
| **Streamlit** | Fastest upload UI, charts, tables — ideal for live demo |
| **Gradio** | Good if you want minimal code around the model only |
| **React + FastAPI** | Only if you have front-end bandwidth |

Streamlit + FastAPI is a common split: Streamlit for demo, FastAPI for API clients.

---

### 7. API & Cloud (Expert Level)

| Layer | Choice |
|-------|--------|
| API | **FastAPI** — upload video, async job, poll status, get report |
| Task queue (optional) | Background thread or **Celery + Redis** if videos are long |
| Container | **Docker** (CUDA optional; CPU fine for demo) |
| Cloud (pick one) | **Railway / Render** (simple), **GCP Cloud Run**, **Hugging Face Spaces** (GPU for demo) |

```
Client → POST /analyze → worker runs pipeline → DB + storage → GET /results/{id}
```

---

### 8. DevOps & Project Management

| Area | Tool |
|------|------|
| Version control | Git + GitHub (`main`, `develop`, feature branches) |
| Kanban | GitHub Projects or Trello (required deliverable) |
| Env | `uv` or `poetry` + `requirements.txt` |
| Config | `.env` for paths, model weights, DB URL |
| CI (nice) | GitHub Actions: lint + smoke test on sample image |

---

### Suggested Repo Layout

```
ai-computer-vision-objects/
├── data/
│   ├── raw/              # images + labels
│   ├── datasets/         # YOLO yaml
│   └── crops/            # saved detections
├── models/               # best.pt weights
├── src/
│   ├── train.py
│   ├── detect_image.py
│   ├── detect_video.py
│   ├── report.py         # time / % per brand
│   ├── db/               # models + repository
│   └── api/              # FastAPI (expert)
├── app/                  # Streamlit UI
├── notebooks/            # EDA, augmentation experiments
├── docker/
├── tests/
├── Dockerfile
└── README.md
```

---

### Level → Stack Mapping

| Level | Minimum Stack |
|-------|----------------|
| **Essential** | YOLO + OpenCV + notebook/script + README |
| **Medium** | + `detect_video.py`, labels on output video |
| **Advanced** | + confidence on overlay, SQLite, multi-class, crops |
| **Expert** | + Streamlit, FastAPI, Docker, cloud deploy |

---

### Default Team Stack (Summary)

```
Python 3.11
Ultralytics YOLOv8
OpenCV + Pillow
Roboflow (annotation)
SQLite + SQLAlchemy
Streamlit (UI)
FastAPI (API)
Docker
GitHub Projects (Kanban)
Google Colab (GPU training)
```

This covers every evaluation criterion: preprocessing (resize/normalize in YOLO pipeline), custom dataset, fine-tuned pretrained model, augmentations, optional real-time inference, video analysis, DB persistence, and a web front.

---

### Trade-offs to Decide Early

1. **Accuracy vs demo speed:** `yolov8n` trains fast; `yolov8s/m` if logos are small in frame.
2. **Frame rate:** all frames vs every 5th frame — affects "time on screen" accuracy.
3. **Single repo vs two:** one monorepo is enough for this scope.
4. **GPU:** train on Colab/Kaggle free GPU; inference on CPU is OK for short clips.

---

## References

- [Project roadmap](https://roadmap-mad-ai-p4.coderf5.es/)
- [Ultralytics YOLO docs](https://docs.ultralytics.com/)

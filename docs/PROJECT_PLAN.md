# Tech Stack — Computer Vision Logo Detection

Recommended technologies for the brand logo detection project, mapped to delivery levels and evaluation criteria.

---

## Core Principle

Use **one detection framework end-to-end** (train → infer on images/video → export metrics) instead of mixing TensorFlow + PyTorch + Detectron2. That keeps the demo, database schema, and deployment simpler.

---

## 1. Detection Model — YOLO via Ultralytics (PyTorch)

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

## 2. Language & CV Libraries

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

## 3. Dataset & Annotation

| Tool | Use |
|------|-----|
| **Roboflow** (free tier) | Annotate boxes, export YOLO format, built-in augmentations |
| **Label Studio** / **CVAT** | Self-hosted alternative |
| **Manual collection** | Screenshots from ads, sports broadcasts, YouTube frames (watch licensing) |

**Brands for PoC:** pick 2–4 visually distinct logos (e.g. Nike, Coca-Cola, McDonald's) — easier to demo multi-class than 10 similar marks.

**Format:** YOLO txt labels (`class x_center y_center width height` normalized).

---

## 4. Video Analysis Pipeline

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

## 5. Database — SQLite → PostgreSQL

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

## 6. Frontend — Streamlit (Expert Level)

| Option | When |
|--------|------|
| **Streamlit** | Fastest upload UI, charts, tables — ideal for live demo |
| **Gradio** | Good if you want minimal code around the model only |
| **React + FastAPI** | Only if you have front-end bandwidth |

Streamlit + FastAPI is a common split: Streamlit for demo, FastAPI for API clients.

---

## 7. API & Cloud (Expert Level)

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

## 8. DevOps & Project Management

| Area | Tool |
|------|------|
| Version control | Git + GitHub (`main`, `develop`, feature branches) |
| Kanban | GitHub Projects or Trello (required deliverable) |
| Env | `uv` or `poetry` + `requirements.txt` |
| Config | `.env` for paths, model weights, DB URL |
| CI (nice) | GitHub Actions: lint + smoke test on sample image |

---

## Suggested Repo Layout

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

## Level → Stack Mapping

| Level | Minimum Stack |
|-------|----------------|
| **Essential** | YOLO + OpenCV + notebook/script + README |
| **Medium** | + `detect_video.py`, labels on output video |
| **Advanced** | + confidence on overlay, SQLite, multi-class, crops |
| **Expert** | + Streamlit, FastAPI, Docker, cloud deploy |

---

## Default Team Stack (Summary)

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
```

This covers every evaluation criterion: preprocessing (resize/normalize in YOLO pipeline), custom dataset, fine-tuned pretrained model, augmentations, optional real-time inference, video analysis, DB persistence, and a web front.

---

## Trade-offs to Decide Early

1. **Accuracy vs demo speed:** `yolov8n` trains fast; `yolov8s/m` if logos are small in frame.
2. **Frame rate:** all frames vs every 5th frame — affects "time on screen" accuracy.
3. **Single repo vs two:** one monorepo is enough for this scope.
4. **GPU:** train on Colab/Kaggle free GPU; inference on CPU is OK for short clips.

---

## References

- [Ultralytics YOLO docs](https://docs.ultralytics.com/)

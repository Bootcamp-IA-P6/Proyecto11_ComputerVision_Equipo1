# BrandSight — Scope Freeze / Congelación de alcance

**Status:** Frozen · **Date:** Sprint Day 1  
**Owner:** A (PO) · **Approved by team:** _Pending 30-min planning meeting_

Related: [USER_STORIES.md](./USER_STORIES.md) · [KANBAN.md](./KANBAN.md) · [PLAN_PROYECTO.md](./PLAN_PROYECTO.md)

---

## Sprint goal / Objetivo del sprint

**EN:** Deliver a deployed Streamlit web app that analyzes 30–60 s demo videos, detects **Coca-Cola** and **Pepsi** logos, stores results in Supabase, and generates an AI marketing report for the Coca-Cola client perspective — plus a **local webcam detection** script for live realtime demo during presentation. Demo-ready in 6 days.

**ES:** Entregar una app Streamlit desplegada que analice vídeos demo de 30–60 s, detecte logos de **Coca-Cola** y **Pepsi**, guarde resultados en Supabase y genere un informe de marketing con IA (perspectiva cliente Coca-Cola) — más un script de **detección con webcam local** para demo en tiempo real durante la presentación. Lista para demo en 6 días.

---

## In scope / Dentro del alcance

| Area | Decision |
|------|----------|
| **Brands** | **Exactly 2:** `coca_cola` (class 0) and `pepsi` (class 1). No third brand. |
| **Detection** | YOLO11 fine-tuned — train from `yolo11l.pt` base, deploy `best.pt`; training in Google Colab only |
| **Input** | MP4 video upload (H.264) + optional pre-loaded demo clips |
| **Local webcam** | **`src/detect_webcam.py`** — realtime logo detection from the machine's camera; **local execution only** (not on deployed Streamlit) |
| **Output** | Annotated video, visibility metrics, competitive analysis, AI report, DB persistence; live annotated webcam window locally |
| **Database** | Supabase PostgreSQL — 5 tables per `sql/schema.sql` |
| **Frontend** | Streamlit only (no custom React) |
| **Deploy** | Streamlit Community Cloud or Railway — **public URL required** |
| **LLM** | Gemini or OpenAI — one call per analysis; Jinja2 fallback if API unavailable |
| **Team** | 3 people · Linux / Mac / Windows · 6-day sprint |
| **Delivery levels** | Essential → Medium → Advanced → Expert (all mandatory except optional REST API) |

---

## Out of scope / Fuera del alcance

| Item | Reason |
|------|--------|
| More than 2 brands | Time-boxed sprint; PO scope freeze |
| Webcam on deployed app (Streamlit Cloud / Railway) | Cloud has no GPU; latency poor; local script meets realtime eval criteria |
| Custom React / Next.js frontend | Streamlit meets Expert level |
| Perfect model accuracy | PoC; iterate with demo video frames if needed |
| Celery / job queues | Streamlit synchronous pipeline is enough |
| Microservice REST API | Optional stretch; deploy Streamlit first |
| Model weights in Git | `best.pt` (fine-tuned) lives in Team Drive + deploy bundle |
| Secrets in repository | `.env` local only; platform secrets for deploy |

---

## Brand constraint (hard rule)

```
MAX_BRANDS = 2

Allowed class names:
  - coca_cola
  - pepsi

Forbidden without PO approval:
  - Any additional YOLO class
  - Generic labels ("cola", "soda", "ex")
  - Rebranding scope mid-sprint
```

If a teammate proposes a third brand, **default answer is no** until Day 6 buffer and only if Essential–Expert are Done.

---

## Demo success criteria

1. Open **deployed URL** (not localhost)
2. Upload or select a 30–60 s demo video with both brands visible
3. See annotated video with bounding boxes, brand names, and confidence %
4. See metrics: seconds, visibility %, detection count per brand
5. See competitive summary (dominant brand, balance label)
6. See AI marketing report rendered in the UI
7. Data persisted in Supabase (verifiable in Table Editor)
8. **Local webcam demo:** presenter runs `python -m src.detect_webcam` on their laptop; live window shows bbox + brand label + confidence % for Coca-Cola or Pepsi

**Demo split:** jury sees the **full pipeline on the deployed URL** (video upload → metrics → report). The **webcam segment runs locally** on the presenter's machine during the presentation (see ISSUE-17).

---

## Shared artifacts (outside Git)

```
Team Drive/
├── datasets/           # Roboflow YOLO export
├── models/best.pt
└── demo_videos/        # 2–3 MP4 clips (H.264)
```

---

## Change control

| Change type | Who decides |
|-------------|-------------|
| New feature in scope | PO (A) + team in daily |
| New brand / class | **Rejected** unless scope doc amended by PO |
| Tech swap (e.g. DB provider) | SM (B) proposes · team agrees same day |
| Cut feature to ship deploy | PO prioritizes: Expert deploy > local webcam (ISSUE-17) > Advanced crops > optional API |

---

## Sign-off / Aprobación del equipo

| Teammate | Role | Scope agreed | Date |
|----------|------|--------------|------|
| _[name]_ | A — PO | ☐ | |
| _[name]_ | B — SM | ☐ | |
| _[name]_ | C — ML | ☐ | |

_Complete during the 30-min Day 1 planning meeting._

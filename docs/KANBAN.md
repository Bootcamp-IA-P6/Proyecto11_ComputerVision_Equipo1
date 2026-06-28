# BrandSight — Kanban Board / Tablero Kanban

**Project:** BrandSight — Coca-Cola vs Pepsi brand visibility analysis  
**Sprint:** 6 days · 3 teammates  
**Columns / Columnas:** `Backlog` → `To Do` → `In Progress` → `In Review` → `Done`

Related: [PROJECT_PLAN.md](./PROJECT_PLAN.md) · [PLAN_PROYECTO.md](./PLAN_PROYECTO.md) · [SCOPE.md](./SCOPE.md) · [USER_STORIES.md](./USER_STORIES.md)

**GitHub sync:** `#N` = [GitHub issue #N](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/N) · Project board is source of truth for column status; this file is the spec + acceptance criteria.

> **Note:** Roboflow dataset is documented in [ROBOFLOW_DATASET.md](./ROBOFLOW_DATASET.md) (658 Coca-Cola + 637 Pepsi annotated images). Primary training notebook: `notebooks/Pepsi_Cocacola_Yolo_version_2.ipynb` (YOLO11 `yolo11l.pt` base → `best.pt`).

---

## Team / Equipo

| ID | Role / Rol | GitHub | Name / Nombre | Focus / Enfoque |
|----|------------|--------|---------------|-----------------|
| **A** | Product Owner | `Marizqdo` | Mar Izquierdo | Scope, UI, presentation, AI prompt |
| **B** | Scrum Master + Backend | `KangMirae` | Mirae Kang | Kanban, Git, pipeline, Supabase, deploy |
| **C** | ML Engineer | `jumair` | Juan Manuel Iriondo | Dataset, Colab, model, inference |

**Legend / Leyenda:** `A` = PO · `B` = SM/Backend · `C` = ML · `All` = whole team / todo el equipo

---

## Board status / Estado del tablero

| To Do | In Progress | In Review | Done |
|-------|-------------|-----------|------|
| 1 | 0 | 4 | 11 |

_Last sync: repo state — `#5`–`#12` implemented in code; live deploy + final QA pending on **#9**, **#13**, **#14**, **#17**._

---

## Issues / Incidencias

_Order matches GitHub issue numbers #1 → #17._

---

### #1 · Project setup & repository / Configuración del proyecto y repositorio

| Field | Value |
|-------|-------|
| **GitHub** | [#1](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/1) · **Closed** |
| **Status** | Done |
| **Sprint day** | Day 1 |
| **Assignee** | KangMirae (**B**) |
| **Support** | All |
| **Labels** | `infra`, `day-1` |

**Description (EN)**  
Initialize the GitHub repository with branch strategy (`main`, `develop`), folder structure, `requirements.txt`, `.gitignore`, `.gitattributes`, and `.env.example`. Ensure all teammates can clone and run a hello-world check on Linux, Mac, and Windows.

**Descripción (ES)**  
Inicializar el repositorio GitHub con estrategia de ramas (`main`, `develop`), estructura de carpetas, `requirements.txt`, `.gitignore`, `.gitattributes` y `.env.example`. Verificar que los tres compañeros puedan clonar y ejecutar una prueba básica en Linux, Mac y Windows.

**Acceptance criteria / Criterios de aceptación**
- [x] Repo created with `main` and `develop` branches
- [x] Folder structure matches project plan
- [x] `.env.example` committed; `.env` in `.gitignore`
- [x] All 3 OS: `pip install -r requirements.txt` succeeds

---

### #2 · Sprint planning & user stories / Planning del sprint y user stories

| Field | Value |
|-------|-------|
| **GitHub** | [#2](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/2) · **Closed** |
| **Status** | Done |
| **Sprint day** | Day 1 |
| **Assignee** | KangMirae (**A** PO hat) |
| **Support** | B, C |
| **Labels** | `planning`, `day-1` |

**Description (EN)**  
Define sprint goal, user stories, and definition of done for each delivery level (Essential → Expert). Create the GitHub Project board and link this Kanban file. Freeze scope: Coca-Cola + Pepsi only, 2 brands, deployed Streamlit app.

**Descripción (ES)**  
Definir objetivo del sprint, user stories y definición de hecho por nivel de entrega (Esencial → Experto). Crear el tablero en GitHub Projects y enlazar este Kanban. Congelar alcance: solo Coca-Cola + Pepsi, 2 marcas, app Streamlit desplegada.

**Deliverables / Entregables**
- [SCOPE.md](./SCOPE.md) — frozen scope (2 brands max)
- [USER_STORIES.md](./USER_STORIES.md) — 18 user stories + DoD per level

**Acceptance criteria / Criterios de aceptación**
- [x] User stories written for upload, detect, metrics, report, deploy
- [x] Kanban board created and shared (GitHub Project)
- [x] Scope document: no more than 2 brands
- [ ] Definition of done sign-off in `USER_STORIES.md` (optional follow-up)

---

### #3 · Supabase project & database schema / Proyecto Supabase y esquema de BD

| Field | Value |
|-------|-------|
| **GitHub** | [#3](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/3) · **Closed** |
| **Status** | Done |
| **Sprint day** | Day 1 |
| **Assignee** | KangMirae (**B**) |
| **Support** | — |
| **Labels** | `database`, `supabase`, `day-1` |

**Runbook:** [SUPABASE_SETUP.md](./SUPABASE_SETUP.md)

**Description (EN)**  
Create a Supabase project (free tier). Run `sql/schema.sql` in the SQL Editor. Verify all 5 tables exist. Share `DATABASE_URL` (Session pooler) via secure channel — never commit to Git.

**Descripción (ES)**  
Crear proyecto en Supabase (tier gratis). Ejecutar `sql/schema.sql` en el SQL Editor. Verificar las 5 tablas. Compartir `DATABASE_URL` (Session pooler) por canal seguro — nunca en Git.

**Acceptance criteria / Criterios de aceptación**
- [x] Supabase project live
- [x] All tables visible in Table Editor
- [x] `python -m scripts.check_db` passes
- [x] `DATABASE_URL` shared with team
- [x] Storage bucket `brandsight-crops` created (`sql/storage.sql`)

**Verify Storage / Verificar almacenamiento**
```bash
python -m scripts.check_storage
```

---

### #4 · Supabase connection layer / Capa de conexión a Supabase

| Field | Value |
|-------|-------|
| **GitHub** | [#4](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/4) · **Closed** |
| **Status** | Done |
| **Sprint day** | Day 2 |
| **Assignee** | KangMirae (**B**) |
| **Support** | — |
| **Labels** | `database`, `backend`, `day-2` |

**Verify / Verificar**
```bash
python -m scripts.check_db
python -m scripts.test_db_insert
```

**Acceptance criteria / Criterios de aceptación**
- [x] DB connection works with Supabase pooler string
- [x] Test insert into `videos` succeeds (run `test_db_insert` on each OS)
- [x] Repository functions documented in `src/db/repository.py`
- [x] Uses `pathlib` for file paths

---

### #5 · Google Colab training notebook / Notebook de entrenamiento en Colab

| Field | Value |
|-------|-------|
| **GitHub** | [#5](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/5) · **Open** |
| **Status** | Done |
| **Sprint day** | Day 1–2 |
| **Assignee** | jumair (**C**) |
| **Support** | A, B (labeling) |
| **Labels** | `ml`, `training`, `colab`, `day-1`, `day-2` |

**Dataset:** [ROBOFLOW_DATASET.md](./ROBOFLOW_DATASET.md) — Roboflow `Coca-Pepsi-5`, YOLO11 export, 658 + 637 annotated images per brand.

**Notebooks**
- `notebooks/Pepsi_Cocacola_Yolo_version_2.ipynb` — full Colab training run (team notebook)
- `notebooks/train_colab.ipynb` — minimal reproducible template for bootcamp handoff

**Description (EN)**  
Fine-tune from Ultralytics `yolo11l.pt` base on Roboflow dataset; export fine-tuned **`best.pt`** (not the base checkpoint) for inference in `models/best.pt`.

**Descripción (ES)**  
Fine-tune desde base `yolo11l.pt` con dataset Roboflow; exportar **`best.pt`** fine-tuned (no el checkpoint base) para inferencia en `models/best.pt`.

**Acceptance criteria / Criterios de aceptación**
- [x] Roboflow dataset ready (≥80 annotated images per brand — see ROBOFLOW_DATASET.md)
- [x] Notebook runs end-to-end on Colab GPU (`Pepsi_Cocacola_Yolo_version_2.ipynb`)
- [x] `best.pt` in `models/` (fine-tuned weights)
- [x] Training metrics logged (mAP, loss in Colab output)
- [x] Notebook(s) committed to repo (no secrets, no dataset blobs)

### #6 · Image detection script / Script de detección en imagen

| Field | Value |
|-------|-------|
| **GitHub** | [#6](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/6) · **Open** |
| **Status** | Done |
| **Sprint day** | Day 2 |
| **Assignee** | jumair (**C**) |
| **Support** | B |
| **Labels** | `inference`, `essential`, `day-2` |

**CLI**
```bash
python -m src.detect_image --image data/demo/pepsi_cocacola1.jpg
python -m src.detect_image --image path/to.jpg --weights models/best.pt
```

**Acceptance criteria / Criterios de aceptación**
- [x] `src/detect_image.py` — loads `best.pt`, draws bbox + label
- [x] Annotated output saved under `data/outputs/`
- [x] CLI with `--image`, `--weights`, `--output`
- [x] **Essential level complete**

### #7 · Demo videos collection / Recopilación de vídeos demo

| Field | Value |
|-------|-------|
| **GitHub** | [#7](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/7) · **Open** |
| **Status** | Done |
| **Sprint day** | Day 3 |
| **Assignee** | Marizqdo (**A**) |
| **Support** | B |
| **Labels** | `content`, `day-3` |

**Assets:** `data/demo/demo1.mp4` … `demo4.mp4` (gitignored — local + Team Drive). Sources: [data/demo/SOURCES.md](../data/demo/SOURCES.md). Download: `python scripts/download_demo_videos.py`.

**Acceptance criteria / Criterios de aceptación**
- [x] ≥2 demo videos available (4 clips: 29–62 s)
- [x] Both brands visible in clips
- [x] MP4 H.264 format
- [x] Videos shared with team (SOURCES.md + download script)

### #8 · Video detection + labels + confidence / Detección en vídeo + etiquetas + confianza

| Field | Value |
|-------|-------|
| **GitHub** | [#8](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/8) · **Open** |
| **Status** | Done |
| **Sprint day** | Day 3 |
| **Assignee** | KangMirae (**B**) |
| **Support** | C |
| **Labels** | `inference`, `video`, `medium`, `day-3` |

**CLI**
```bash
python -m src.detect_video --video data/demo/demo1.mp4
python -m src.detect_video --video path/to.mp4 --no-db
```

**Acceptance criteria / Criterios de aceptación**
- [x] `src/detect_video.py` — stride sampling, bbox + brand + confidence % overlay
- [x] Annotated MP4 saved (`data/outputs/annotated_*.mp4`)
- [x] Detections inserted into Supabase when `DATABASE_URL` set
- [x] E2E run on demo video (`annotated_demo2.mp4` produced)
- [x] **Medium level complete**

### #9 · Visibility metrics & competitive analysis / Métricas de visibilidad y análisis competitivo

| Field | Value |
|-------|-------|
| **GitHub** | [#9](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/9) · **Open** |
| **Status** | In Review |
| **Sprint day** | Day 4 |
| **Assignee** | KangMirae (**B**) |
| **Support** | C |
| **Labels** | `metrics`, `backend`, `advanced`, `day-4` |

**CLI**
```bash
python -m src.detect_video --video data/demo/demo1.mp4   # detections + metrics → DB
python -m src.metrics_export --video-id <id> --export
```

**Acceptance criteria / Criterios de aceptación**
- [x] Coca-Cola and Pepsi seconds + % calculated correctly
- [x] Dominant brand and gap stored in DB (`brand_summary`, `competitive_analysis`)
- [x] JSON/text summary exported to `data/outputs/metrics_{id}.*`
- [x] Frame sampling documented in README + `src/metrics.py` module docstring
- [ ] Metrics match manual spot-check on demo video — _run on `demo1.mp4`_

---

### #10 · Bbox crops & Supabase Storage / Recortes bbox y almacenamiento en la nube

| Field | Value |
|-------|-------|
| **GitHub** | [#10](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/10) · **Open** |
| **Status** | Done |
| **Sprint day** | Day 4 |
| **Assignee** | KangMirae (**B**) |
| **Support** | C |
| **Labels** | `database`, `storage`, `advanced`, `day-4` |

**Implementation**
- `src/crops.py` — extract bbox JPEGs, upload when Storage configured
- `src/supabase_storage.py` — upload to `brandsight-crops`, signed URLs for UI
- `detections.crop_path` — `storage:brandsight-crops/{video_id}/{brand}_{index}.jpg`

**Verify**
```bash
python -m scripts.check_storage
python -m scripts.verify_crops --video-id <id>
```

**Acceptance criteria / Criterios de aceptación**
- [x] Crops uploaded to Supabase Storage bucket `brandsight-crops`
- [x] `crop_path` stores `storage:…` URI in PostgreSQL
- [x] Streamlit thumbnails via signed URLs; sidebar shows **Storage ready**
- [x] Local cache under `data/crops/{video_id}/` for dev
- [x] **Advanced DB + Storage requirement met**

### #11 · AI marketing report generator / Generador de informe de marketing con IA

| Field | Value |
|-------|-------|
| **GitHub** | [#11](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/11) · **Open** |
| **Status** | Done |
| **Sprint day** | Day 4–5 |
| **Assignee** | Marizqdo (**A**) |
| **Support** | B |
| **Labels** | `ai`, `report`, `day-4`, `day-5` |

**Implementation:** `src/report/generate_marketing_report.py` — Gemini (`gemini-2.0-flash`) with Jinja2 fallback; wired in `src/pipeline.py`; saved to `marketing_reports` + `data/outputs/report_{id}.md`.

**Acceptance criteria / Criterios de aceptación**
- [x] Report generated from DB metrics only (no invented numbers)
- [x] Report saved to `marketing_reports` table
- [x] Coca-Cola client perspective in tone
- [x] Fallback template works without `GEMINI_API_KEY`

### #12 · Streamlit web application / Aplicación web Streamlit

| Field | Value |
|-------|-------|
| **GitHub** | [#12](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/12) · **Open** |
| **Status** | Done |
| **Sprint day** | Day 5 |
| **Assignee** | Marizqdo (**A**) |
| **Support** | B |
| **Labels** | `frontend`, `streamlit`, `expert`, `day-5` |

**App:** `app/streamlit_app.py` — upload or demo video → `analyze_video` pipeline → metrics table + bar chart + annotated video + crop thumbnails + AI report + History tab.

**Acceptance criteria / Criterios de aceptación**
- [x] Upload → analyze → results flow works
- [x] Metrics and chart displayed from Supabase
- [x] AI report rendered in UI
- [x] Sidebar: DB + Storage status
- [x] **Expert frontend requirement met**

### #13 · Cloud deployment / Despliegue en la nube

| Field | Value |
|-------|-------|
| **GitHub** | [#13](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/13) · **Open** |
| **Status** | In Review |
| **Sprint day** | Day 5 |
| **Assignee** | KangMirae (**B**) |
| **Support** | A |
| **Labels** | `deploy`, `expert`, `day-5` |

**Acceptance criteria / Criterios de aceptación**
- [ ] Public URL accessible — _deploy via [docs/DEPLOY.md](./DEPLOY.md)_
- [x] Deploy config: `.streamlit/config.toml`, `runtime.txt`, `Dockerfile`, secrets bootstrap
- [x] `scripts/smoke_deploy.py` — checks DB, schema, Storage bucket, `best.pt`
- [ ] Deployed app connects to Supabase + Storage — _verify on live URL_
- [ ] Full demo on live URL (upload → metrics → crops from bucket → report)
- [x] Secrets not exposed in repo or logs (`.streamlit/secrets.toml` gitignored, UI redaction)

---

### #14 · README & technical documentation / README y documentación técnica

| Field | Value |
|-------|-------|
| **GitHub** | [#14](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/14) · **Open** |
| **Status** | In Review |
| **Sprint day** | Day 2–6 |
| **Assignee** | KangMirae (**B**), Marizqdo (**A**) |
| **Support** | — |
| **Labels** | `docs`, `day-2`, `day-6` |

**Docs in repo:** `README.md`, `docs/PROJECT_PLAN.md`, `docs/SUPABASE_SETUP.md`, `docs/DEPLOY.md`, `docs/ROBOFLOW_DATASET.md`, `PRESENTATION_MIRAE.md`

**Acceptance criteria / Criterios de aceptación**
- [x] README complete in repo root (setup, CLI, crops, deploy)
- [x] Supabase + Storage setup documented (`SUPABASE_SETUP.md`)
- [ ] Live demo URL linked in README
- [ ] Evaluation criteria addressed in docs (preprocessing, dataset, YOLO11 fine-tune, augmentations)

### #15 · Presentation & live demo rehearsal / Presentación y ensayo de demo en vivo

| Field | Value |
|-------|-------|
| **GitHub** | [#15](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/15) · **Open** |
| **Status** | To Do |
| **Sprint day** | Day 5–6 |
| **Assignee** | Marizqdo (**A**) |
| **Support** | All |
| **Labels** | `presentation`, `day-5`, `day-6` |

**Description (EN)**  
Presentation: problem → solution → architecture → live demo on deployed URL → **local webcam segment (#17)** → stack → limitations → future work.

**Deliverables:** `PRESENTATION_MIRAE.md` (backend script) + team slide deck

**Acceptance criteria / Criterios de aceptación**
- [ ] Slide deck ready (6–10 slides)
- [x] Backend presentation script written (`PRESENTATION_MIRAE.md`)
- [ ] Live demo script written and rehearsed
- [ ] Each teammate has a speaking section
- [ ] Kanban synced with repo · release tagged `v1.0-demo`

### #17 · Local webcam detection / Detección con webcam local

| Field | Value |
|-------|-------|
| **GitHub** | [#17](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/17) · **Open** |
| **Status** | In Review |
| **Sprint day** | Day 2–3 |
| **Assignee** | jumair (**C**) |
| **Support** | B |
| **Labels** | `inference`, `webcam`, `realtime`, `medium`, `day-2`, `day-3` |

**Implementation:** `src/detect_webcam.py` — OpenCV camera + `best.pt` + bbox overlay; records to `data/outputs/`. Also `scripts/check_web_cam_record.py`.

**Acceptance criteria / Criterios de aceptación**
- [x] Live webcam window with bbox + brand label + confidence %
- [ ] Polished CLI (`python -m src.detect_webcam`) documented in README
- [ ] Works on Linux, Mac, Windows — _team QA_
- [ ] **Medium — realtime eval criteria met**

## Sprint day map / Mapa por día

| Day | GitHub issues |
|-----|----------------|
| **Day 1** | #1, #2, #3, #5 (start + Roboflow dataset) |
| **Day 2** | #4, #5 (finish), #6, #17 (start), #14 (start) |
| **Day 3** | #7, #8, #17 (finish) |
| **Day 4** | #9, #10, #11 (start) |
| **Day 5** | #11 (finish), #12, #13, #15 (dry-run) |
| **Day 6** | #14 (finish), #15 (final), bug fixes |

---

## Delivery level checklist / Checklist por nivel de entrega

| Level / Nivel | GitHub issue(s) | Status |
|---------------|-----------------|--------|
| 🟢 Essential | #6 | **Done** |
| 🟡 Medium | #8, #17 | **#8 Done** · #17 In Review |
| 🟠 Advanced | #9, #10, #11 | **#10, #11 Done** · #9 In Review |
| 🔴 Expert | #12, #13 | **#12 Done** · #13 In Review |

---

## Daily standup template / Plantilla daily

```
Yesterday / Ayer:     [what I did]
Today / Hoy:          [#N — short title]
Blockers / Bloqueos:  [none / describe]
```

---

## GitHub Project sync / Sincronización

**Repo:** [Proyecto11_ComputerVision_Equipo1](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1)  
**Issues:** [#1 … #15, #17](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues) _(no #16 on GitHub)_

| GitHub # | Title |
|----------|-------|
| [#1](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/1) | Project setup & repository |
| [#2](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/2) | Sprint planning & user stories |
| [#3](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/3) | Supabase project & database schema |
| [#4](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/4) | Supabase connection layer |
| [#5](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/5) | Google Colab training notebook |
| [#6](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/6) | Image detection script |
| [#7](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/7) | Demo videos collection |
| [#8](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/8) | Video detection + labels + confidence |
| [#9](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/9) | Visibility metrics & competitive analysis |
| [#10](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/10) | Bbox crops & database persistence |
| [#11](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/11) | AI marketing report generator |
| [#12](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/12) | Streamlit web application |
| [#13](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/13) | Cloud deployment |
| [#14](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/14) | README & technical documentation |
| [#15](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/15) | Presentation & live demo rehearsal |
| [#17](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/17) | Local webcam detection |

_When closing an issue on GitHub, update **Status → Done** and check acceptance criteria here._

---

_Last updated: synced with repo state — YOLO11 (`yolo11l.pt` base → `best.pt`), Supabase PostgreSQL + Storage `brandsight-crops`, pipeline + Streamlit complete; live deploy QA pending._

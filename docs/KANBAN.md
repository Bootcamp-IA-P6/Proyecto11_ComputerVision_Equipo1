# BrandSight — Kanban Board / Tablero Kanban

**Project:** BrandSight — Coca-Cola vs Pepsi brand visibility analysis  
**Sprint:** 6 days · 3 teammates  
**Columns / Columnas:** `Backlog` → `To Do` → `In Progress` → `In Review` → `Done`

Related: [PROJECT_PLAN.md](./PROJECT_PLAN.md) · [PLAN_PROYECTO.md](./PLAN_PROYECTO.md) · [SCOPE.md](./SCOPE.md) · [USER_STORIES.md](./USER_STORIES.md)

**GitHub sync:** `#N` = [GitHub issue #N](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/N) · Project board is source of truth for column status; this file is the spec + acceptance criteria.

> **Gap:** Roboflow dataset (80+ images/brand) is not a separate GitHub issue — track as prerequisite under **#5** or open **#16** on GitHub if you want a dedicated card.

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
| 7 | 1 | 3 | 5 |

_Sync with GitHub Project columns. / Sincronizar con columnas del Project._

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
- [ ] Optional: Storage bucket `brandsight-crops` (`sql/storage.sql`)

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
| **Status** | In Review |
| **Sprint day** | Day 1–2 |
| **Assignee** | jumair (**C**) |
| **Support** | A, B (labeling) |
| **Labels** | `ml`, `training`, `colab`, `day-1`, `day-2` |

**Prerequisite (no GitHub issue yet):** Roboflow dataset — 2 classes (`coca_cola`, `pepsi`), ≥80 images/brand, YOLO export.

**Description (EN)**  
Create `notebooks/train_colab.ipynb`: install Ultralytics, load Roboflow dataset (API key in Colab secrets), fine-tune from `yolov8n.pt` or `yolov8s.pt`, enable augmentations (flip, mosaic, HSV), save checkpoints to Google Drive, export `best.pt`. Include validation plots on 2–3 test images.

**Descripción (ES)**  
Crear `notebooks/train_colab.ipynb`: instalar Ultralytics, cargar dataset Roboflow (API key en secretos Colab), fine-tune desde `yolov8n.pt` o `yolov8s.pt`, activar augmentations (flip, mosaic, HSV), guardar checkpoints en Google Drive, exportar `best.pt`. Incluir gráficos de validación en 2–3 imágenes de test.

**Acceptance criteria / Criterios de aceptación**
- [ ] Roboflow dataset ready (≥80 annotated images per brand)
- [ ] Notebook runs end-to-end on Colab GPU
- [ ] `best.pt` saved to Team Drive
- [ ] Training metrics logged (mAP, loss)
- [ ] Notebook committed to repo (no secrets, no dataset)

---

### #6 · Image detection script / Script de detección en imagen

| Field | Value |
|-------|-------|
| **GitHub** | [#6](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/6) · **Open** |
| **Status** | To Do |
| **Sprint day** | Day 2 |
| **Assignee** | jumair (**C**) |
| **Support** | B |
| **Labels** | `inference`, `essential`, `day-2` |

**Description (EN)**  
Implement `src/detect_image.py`: load `best.pt`, run inference on a single image, draw bounding boxes with brand label (`coca_cola` / `pepsi`) under each detection. Save annotated output image. CLI: `python -m src.detect_image --image path --weights models/best.pt`.

**Descripción (ES)**  
Implementar `src/detect_image.py`: cargar `best.pt`, inferencia en imagen única, dibujar bounding boxes con etiqueta de marca bajo cada detección. Guardar imagen anotada.

**Acceptance criteria / Criterios de aceptación**
- [ ] Detects at least one brand in test image
- [ ] Bounding box + label visible on output
- [ ] Works on Linux, Mac, Windows
- [ ] **Essential level complete**

---

### #7 · Demo videos collection / Recopilación de vídeos demo

| Field | Value |
|-------|-------|
| **GitHub** | [#7](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/7) · **Open** |
| **Status** | To Do |
| **Sprint day** | Day 3 |
| **Assignee** | Marizqdo (**A**) |
| **Support** | B |
| **Labels** | `content`, `day-3` |

**Description (EN)**  
Record or source 2–3 demo videos (30–60 s) where both Coca-Cola and Pepsi logos appear. Store in Team Drive `demo_videos/`. H.264 MP4 for Windows compatibility.

**Acceptance criteria / Criterios de aceptación**
- [ ] ≥2 demo videos available
- [ ] Both brands visible in at least one clip
- [ ] MP4 H.264 format
- [ ] Videos shared with team

---

### #8 · Video detection + labels + confidence / Detección en vídeo + etiquetas + confianza

| Field | Value |
|-------|-------|
| **GitHub** | [#8](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/8) · **Open** |
| **Status** | In Review |
| **Sprint day** | Day 3 |
| **Assignee** | KangMirae (**B**) |
| **Support** | C |
| **Labels** | `inference`, `video`, `medium`, `day-3` |

**Description (EN)**  
Implement `src/detect_video.py`: process video frame by frame (or every Nth frame), run YOLO inference, overlay bounding boxes with brand name and confidence %. Save annotated MP4. Write detection rows to Supabase `detections` table.

**CLI**
```bash
python -m src.detect_video --video data/demo/sample.mp4
python -m src.detect_video --video path/to.mp4 --no-db
```

**Acceptance criteria / Criterios de aceptación**
- [x] Annotated video saved with labels + confidence %
- [x] Detections inserted into Supabase (default when `DATABASE_URL` set)
- [ ] 30s demo video processes successfully — _needs `best.pt` + demo clip_
- [ ] **Medium level complete** — _after E2E demo run_

---

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

### #10 · Bbox crops & database persistence / Recortes bbox y persistencia en BD

| Field | Value |
|-------|-------|
| **GitHub** | [#10](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/10) · **Open** |
| **Status** | In Review |
| **Sprint day** | Day 4 |
| **Assignee** | KangMirae (**B**) |
| **Support** | C |
| **Labels** | `database`, `advanced`, `day-4` |

**Acceptance criteria / Criterios de aceptación**
- [x] Crop images saved for sample detections (`src/crops.py` → `data/crops/{video_id}/`)
- [x] `crop_path` populated in Supabase (`detect_video` + `pipeline`)
- [x] Crops viewable from path/URL (Streamlit thumbnails + `scripts/verify_crops.py`)
- [x] **Advanced DB requirement met**

---

### #11 · AI marketing report generator / Generador de informe de marketing con IA

| Field | Value |
|-------|-------|
| **GitHub** | [#11](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/11) · **Open** |
| **Status** | To Do |
| **Sprint day** | Day 4–5 |
| **Assignee** | Marizqdo (**A**) |
| **Support** | B |
| **Labels** | `ai`, `report`, `day-4`, `day-5` |

**Acceptance criteria / Criterios de aceptación**
- [ ] Report generated from DB metrics only (no invented numbers)
- [ ] Report saved to `marketing_reports` table
- [ ] Coca-Cola client perspective in tone
- [ ] Fallback template works without API key

---

### #12 · Streamlit web application / Aplicación web Streamlit

| Field | Value |
|-------|-------|
| **GitHub** | [#12](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/12) · **Open** |
| **Status** | To Do |
| **Sprint day** | Day 5 |
| **Assignee** | Marizqdo (**A**) |
| **Support** | B |
| **Labels** | `frontend`, `streamlit`, `expert`, `day-5` |

**Acceptance criteria / Criterios de aceptación**
- [ ] Upload → analyze → results flow works
- [ ] Metrics and chart displayed correctly
- [ ] AI report rendered in UI
- [ ] **Expert frontend requirement met**

---

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
- [x] Deploy config: `.streamlit/config.toml`, `packages.txt`, `runtime.txt`, secrets bootstrap
- [x] `scripts/smoke_deploy.py` pre-flight check (no secrets logged)
- [ ] Deployed app connects to Supabase — _verify on live URL_
- [ ] Full demo works on live URL (upload → metrics → report) — _use 30–60 s MP4_
- [x] Secrets not exposed in repo or logs (`.streamlit/secrets.toml` gitignored, UI redaction)

---

### #14 · README & technical documentation / README y documentación técnica

| Field | Value |
|-------|-------|
| **GitHub** | [#14](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/14) · **Open** |
| **Status** | To Do |
| **Sprint day** | Day 2–6 |
| **Assignee** | KangMirae (**B**), Marizqdo (**A**) |
| **Support** | — |
| **Labels** | `docs`, `day-2`, `day-6` |

**Acceptance criteria / Criterios de aceptación**
- [ ] README complete in repo root
- [ ] Setup works for new teammate from README alone
- [ ] Live demo URL linked
- [ ] Evaluation criteria addressed (preprocessing, dataset, fine-tune, augmentations)

---

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

**Acceptance criteria / Criterios de aceptación**
- [ ] Slide deck ready (6–10 slides)
- [ ] Live demo script written and rehearsed
- [ ] Each teammate has a speaking section
- [ ] Kanban 100% Done or Won't Do · release tagged `v1.0-demo`

---

### #17 · Local webcam detection / Detección con webcam local

| Field | Value |
|-------|-------|
| **GitHub** | [#17](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1/issues/17) · **Open** |
| **Status** | To Do |
| **Sprint day** | Day 2–3 |
| **Assignee** | jumair (**C**) |
| **Support** | B |
| **Labels** | `inference`, `webcam`, `realtime`, `medium`, `day-2`, `day-3` |

**Description (EN)**  
Implement `src/detect_webcam.py`: local OpenCV camera + YOLO, bbox + brand + confidence %. **Local only** — not on deployed Streamlit. CLI: `python -m src.detect_webcam --weights models/best.pt`.

**Acceptance criteria / Criterios de aceptación**
- [ ] Live webcam window with bbox + brand label + confidence %
- [ ] Works on Linux, Mac, Windows
- [ ] Documented in README (presentation demo segment)
- [ ] **Medium — realtime eval criteria met**

---

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

| Level / Nivel | GitHub issue(s) | Owner |
|---------------|-----------------|-------|
| 🟢 Essential | #6 | jumair + KangMirae |
| 🟡 Medium | #8, #17 | KangMirae + jumair |
| 🟠 Advanced | #9, #10, #11 | KangMirae + Marizqdo |
| 🔴 Expert | #12, #13 | Marizqdo + KangMirae |

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

_Last updated: synced with GitHub issues #1–#17 (assignees + closed state)_

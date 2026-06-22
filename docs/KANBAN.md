# BrandSight — Kanban Board / Tablero Kanban

**Project:** BrandSight — Coca-Cola vs Pepsi brand visibility analysis  
**Sprint:** 6 days · 3 teammates  
**Columns / Columnas:** `Backlog` → `To Do` → `In Progress` → `In Review` → `Done`

Related: [PROJECT_PLAN.md](./PROJECT_PLAN.md) · [PLAN_PROYECTO.md](./PLAN_PROYECTO.md) · [SCOPE.md](./SCOPE.md) · [USER_STORIES.md](./USER_STORIES.md)

---

## Team / Equipo

| ID | Role / Rol | Name / Nombre | Focus / Enfoque |
|----|------------|---------------|-----------------|
| **A** | Product Owner | _[fill in]_ | Scope, UI, presentation, AI prompt |
| **B** | Scrum Master + Backend | _[fill in]_ | Kanban, Git, pipeline, Supabase, deploy |
| **C** | ML Engineer | _[fill in]_ | Dataset, Colab, model, inference |

**Legend / Leyenda:** `A` = PO · `B` = SM/Backend · `C` = ML · `All` = whole team / todo el equipo

---

## Board status / Estado del tablero

| To Do | In Progress | In Review | Done |
|-------|-------------|-----------|------|
| 16 | 0 | 0 | 0 |

_Update counts as cards move. / Actualizar contadores al mover tarjetas._

---

## Issues / Incidencias

---

### ISSUE-01 · Project setup & repository / Configuración del proyecto y repositorio

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 1 |
| **Responsible** | **B** (SM) |
| **Support** | All |
| **Labels** | `infra`, `day-1` |

**Description (EN)**  
Initialize the GitHub repository with branch strategy (`main`, `develop`), folder structure, `requirements.txt`, `.gitignore`, `.gitattributes`, and `.env.example`. Ensure all teammates can clone and run a hello-world check on Linux, Mac, and Windows.

**Descripción (ES)**  
Inicializar el repositorio GitHub con estrategia de ramas (`main`, `develop`), estructura de carpetas, `requirements.txt`, `.gitignore`, `.gitattributes` y `.env.example`. Verificar que los tres compañeros puedan clonar y ejecutar una prueba básica en Linux, Mac y Windows.

**Acceptance criteria / Criterios de aceptación**
- [ ] Repo created with `main` and `develop` branches
- [ ] Folder structure matches project plan
- [ ] `.env.example` committed; `.env` in `.gitignore`
- [ ] All 3 OS: `pip install -r requirements.txt` succeeds

---

### ISSUE-02 · Sprint planning & user stories / Planning del sprint y user stories

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 1 |
| **Responsible** | **A** (PO) |
| **Support** | B, C |
| **Labels** | `planning`, `day-1` |

**Description (EN)**  
Define sprint goal, user stories, and definition of done for each delivery level (Essential → Expert). Create the GitHub Project board (or Trello) and link this Kanban file. Freeze scope: Coca-Cola + Pepsi only, 2 brands, deployed Streamlit app.

**Descripción (ES)**  
Definir objetivo del sprint, user stories y definición de hecho por nivel de entrega (Esencial → Experto). Crear el tablero en GitHub Projects (o Trello) y enlazar este archivo Kanban. Congelar alcance: solo Coca-Cola + Pepsi, 2 marcas, app Streamlit desplegada.

**Deliverables / Entregables**
- [SCOPE.md](./SCOPE.md) — frozen scope (2 brands max)
- [USER_STORIES.md](./USER_STORIES.md) — 18 user stories + DoD per level
- GitHub Project board — _paste URL after creation (see below)_

**Acceptance criteria / Criterios de aceptación**
- [x] User stories written for upload, detect, metrics, report, deploy
- [ ] Definition of done agreed by team (30-min meeting) — _draft in USER_STORIES.md; sign-off table pending_
- [ ] Kanban board created and shared — _this file is source of truth; import to GitHub Projects pending_
- [x] Scope document: no more than 2 brands

**Note:** Does not block on ISSUE-01 approval. Repo setup and planning can run in parallel.

---

### ISSUE-03 · Supabase project & database schema / Proyecto Supabase y esquema de BD

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 1 |
| **Responsible** | **B** (SM) |
| **Support** | — |
| **Labels** | `database`, `supabase`, `day-1` |

**Description (EN)**  
Create a Supabase project (free tier). Run `sql/schema.sql` in the SQL Editor. Verify all 5 tables exist: `videos`, `detections`, `brand_summary`, `competitive_analysis`, `marketing_reports`. Share `DATABASE_URL` (Session pooler) with the team via a secure channel — never commit to Git.

**Descripción (ES)**  
Crear proyecto en Supabase (tier gratis). Ejecutar `sql/schema.sql` en el SQL Editor. Verificar las 5 tablas: `videos`, `detections`, `brand_summary`, `competitive_analysis`, `marketing_reports`. Compartir `DATABASE_URL` (Session pooler) por canal seguro — nunca en Git.

**Acceptance criteria / Criterios de aceptación**
- [ ] Supabase project live
- [ ] All tables visible in Table Editor
- [ ] `DATABASE_URL` shared with team
- [ ] Optional: Storage bucket `brandsight-crops` created

---

### ISSUE-04 · Supabase connection layer / Capa de conexión a Supabase

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 2 |
| **Responsible** | **B** (SM) |
| **Support** | — |
| **Labels** | `database`, `backend`, `day-2` |

**Description (EN)**  
Implement `src/db/connection.py`, `models.py`, and `repository.py` using SQLAlchemy. Read `DATABASE_URL` from environment. Provide functions to insert/query videos, detections, summaries, and reports. Test connection from all 3 OS.

**Descripción (ES)**  
Implementar `src/db/connection.py`, `models.py` y `repository.py` con SQLAlchemy. Leer `DATABASE_URL` del entorno. Funciones para insertar/consultar videos, detecciones, resúmenes e informes. Probar conexión desde los 3 sistemas operativos.

**Verify / Verificar**
```bash
python -m scripts.check_db
python -m scripts.test_db_insert
```

**Acceptance criteria / Criterios de aceptación**
- [x] DB connection works with Supabase pooler string
- [x] Test insert into `videos` succeeds from Linux, Mac, Windows — _run `test_db_insert` on each OS_
- [x] Repository functions documented in code
- [x] Uses `pathlib` for any file paths

---

### ISSUE-05 · Roboflow dataset — Coca-Cola & Pepsi / Dataset Roboflow — Coca-Cola y Pepsi

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 1–2 |
| **Responsible** | **C** (ML) |
| **Support** | **A, B** (labeling help) |
| **Labels** | `dataset`, `ml`, `day-1`, `day-2` |

**Description (EN)**  
Create a Roboflow project with 2 classes: `coca_cola` (class 0) and `pepsi` (class 1). Collect 80–120 images per brand from ads, sports, packaging, billboards. Annotate bounding boxes. Export in YOLO format. Enable augmentations (flip, brightness, crop) in Roboflow or document YOLO training augmentations.

**Descripción (ES)**  
Crear proyecto Roboflow con 2 clases: `coca_cola` (clase 0) y `pepsi` (clase 1). Recopilar 80–120 imágenes por marca de anuncios, deportes, envases, vallas. Anotar bounding boxes. Exportar en formato YOLO. Activar augmentations (flip, brillo, crop) o documentarlas en entrenamiento YOLO.

**Acceptance criteria / Criterios de aceptación**
- [ ] ≥80 annotated images per brand
- [ ] Train/val split configured
- [ ] YOLO export zip available in Team Drive
- [ ] Class names consistent: `coca_cola`, `pepsi`

---

### ISSUE-06 · Google Colab training notebook / Notebook de entrenamiento en Colab

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 1–2 |
| **Responsible** | **C** (ML) |
| **Support** | B |
| **Labels** | `ml`, `training`, `colab`, `day-1`, `day-2` |

**Description (EN)**  
Create `notebooks/train_colab.ipynb`: install Ultralytics, load Roboflow dataset (API key in Colab secrets), fine-tune from `yolov8n.pt` or `yolov8s.pt`, enable augmentations (flip, mosaic, HSV), save checkpoints to Google Drive, export `best.pt`. Include validation plots on 2–3 test images.

**Descripción (ES)**  
Crear `notebooks/train_colab.ipynb`: instalar Ultralytics, cargar dataset Roboflow (API key en secretos Colab), fine-tune desde `yolov8n.pt` o `yolov8s.pt`, activar augmentations (flip, mosaic, HSV), guardar checkpoints en Google Drive, exportar `best.pt`. Incluir gráficos de validación en 2–3 imágenes de test.

**Acceptance criteria / Criterios de aceptación**
- [ ] Notebook runs end-to-end on Colab GPU
- [ ] `best.pt` saved to Team Drive
- [ ] Training metrics logged (mAP, loss)
- [ ] Notebook committed to repo (no secrets, no dataset)

---

### ISSUE-07 · Image detection script / Script de detección en imagen

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 2 |
| **Responsible** | **C** (ML) |
| **Support** | B |
| **Labels** | `inference`, `essential`, `day-2` |

**Description (EN)**  
Implement `src/detect_image.py`: load `best.pt`, run inference on a single image, draw bounding boxes with brand label (`coca_cola` / `pepsi`) under each detection. Save annotated output image. CLI: `python -m src.detect_image --image path --weights models/best.pt`.

**Descripción (ES)**  
Implementar `src/detect_image.py`: cargar `best.pt`, inferencia en imagen única, dibujar bounding boxes con etiqueta de marca (`coca_cola` / `pepsi`) bajo cada detección. Guardar imagen anotada. CLI: `python -m src.detect_image --image path --weights models/best.pt`.

**Acceptance criteria / Criterios de aceptación**
- [ ] Detects at least one brand in test image
- [ ] Bounding box + label visible on output
- [ ] Works on Linux, Mac, Windows
- [ ] **Essential level complete**

---

### ISSUE-17 · Local webcam detection / Detección con webcam local

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 2–3 |
| **Responsible** | **C** (ML) |
| **Support** | B |
| **Labels** | `inference`, `webcam`, `realtime`, `medium`, `day-2`, `day-3` |

**Description (EN)**  
Implement `src/detect_webcam.py`: open the local camera with OpenCV, run YOLO inference frame-by-frame, overlay bounding boxes with brand name (`coca_cola` / `pepsi`) and confidence % below each detection. Display in a live window; press `q` to quit. **Local execution only** — not deployed to Streamlit Cloud. Reuse inference logic from `detect_image.py` / `detect_video.py`. CLI: `python -m src.detect_webcam --weights models/best.pt` (optional `--camera 0`).

**Descripción (ES)**  
Implementar `src/detect_webcam.py`: abrir cámara local con OpenCV, inferencia YOLO frame a frame, overlay con nombre de marca (`coca_cola` / `pepsi`) y % de confianza bajo cada detección. Ventana en vivo; `q` para salir. **Solo ejecución local** — no desplegar en Streamlit Cloud. Reutilizar lógica de `detect_image.py` / `detect_video.py`. CLI: `python -m src.detect_webcam --weights models/best.pt` (opcional `--camera 0`).

**Acceptance criteria / Criterios de aceptación**
- [ ] Live webcam window shows detections with bbox + brand label + confidence %
- [ ] Detects at least one brand when pointing camera at Coca-Cola or Pepsi product/logo
- [ ] Works on Linux, Mac, Windows
- [ ] Documented in README (local run only; used in presentation demo segment)
- [ ] **Medium level — realtime requirement met**

---

### ISSUE-08 · Demo videos collection / Recopilación de vídeos demo

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 3 |
| **Responsible** | **A** (PO) |
| **Support** | B |
| **Labels** | `content`, `day-3` |

**Description (EN)**  
Record or source 2–3 demo videos (30–60 seconds each) where both Coca-Cola and Pepsi logos appear. Store in Team Drive `demo_videos/`. At least one video must work reliably for the live demo. H.264 MP4 format for Windows compatibility.

**Descripción (ES)**  
Grabar u obtener 2–3 vídeos demo (30–60 segundos) donde aparezcan logos de Coca-Cola y Pepsi. Guardar en Team Drive `demo_videos/`. Al menos un vídeo debe funcionar de forma fiable en la demo en vivo. Formato MP4 H.264 para compatibilidad Windows.

**Acceptance criteria / Criterios de aceptación**
- [ ] ≥2 demo videos available
- [ ] Both brands visible in at least one clip
- [ ] MP4 H.264 format
- [ ] Videos shared with team

---

### ISSUE-09 · Video detection + labels + confidence / Detección en vídeo + etiquetas + confianza

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 3 |
| **Responsible** | **B** (SM) |
| **Support** | C |
| **Labels** | `inference`, `video`, `medium`, `day-3` |

**Description (EN)**  
Implement `src/detect_video.py`: process video frame by frame (or every Nth frame), run YOLO inference, overlay bounding boxes with brand name and confidence % below each detection. Save annotated MP4. Write detection rows to Supabase `detections` table. CLI support for video path and weights.

**Descripción (ES)**  
Implementar `src/detect_video.py`: procesar vídeo frame a frame (o cada N frames), inferencia YOLO, overlay con nombre de marca y % de confianza bajo cada detección. Guardar MP4 anotado. Escribir filas en tabla `detections` de Supabase. Soporte CLI para ruta de vídeo y pesos.

**Acceptance criteria / Criterios de aceptación**
- [ ] Annotated video saved with labels + confidence %
- [ ] Detections inserted into Supabase
- [ ] 30s demo video processes successfully
- [ ] **Medium level complete**

---

### ISSUE-10 · Visibility metrics & competitive analysis / Métricas de visibilidad y análisis competitivo

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 4 |
| **Responsible** | **B** (SM) |
| **Support** | C |
| **Labels** | `metrics`, `backend`, `advanced`, `day-4` |

**Description (EN)**  
Implement `src/metrics.py` and `src/report.py`: calculate per-brand visible seconds, visibility %, detection count, avg confidence. Determine dominant brand and `balance_label` (`coca_cola_dominant`, `pepsi_dominant`, `balanced`). Write to `brand_summary` and `competitive_analysis` tables. Export JSON/text summary.

**Descripción (ES)**  
Implementar `src/metrics.py` y `src/report.py`: calcular segundos visibles, % de visibilidad, número de detecciones y confianza media por marca. Determinar marca dominante y `balance_label` (`coca_cola_dominant`, `pepsi_dominant`, `balanced`). Escribir en tablas `brand_summary` y `competitive_analysis`. Exportar resumen JSON/texto.

**Acceptance criteria / Criterios de aceptación**
- [ ] Coca-Cola and Pepsi seconds + % calculated correctly
- [ ] Dominant brand and gap stored in DB
- [ ] Metrics match manual spot-check on demo video
- [ ] Document frame sampling assumption in code/README

---

### ISSUE-11 · Bbox crops & database persistence / Recortes bbox y persistencia en BD

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 4 |
| **Responsible** | **B** (SM) |
| **Support** | C |
| **Labels** | `database`, `advanced`, `day-4` |

**Description (EN)**  
Save cropped logo images from each detection to `data/crops/{video_id}/` or Supabase Storage bucket `brandsight-crops`. Store `crop_path` in `detections` table. Ensure paths work in deployed environment (prefer Supabase Storage URLs for production).

**Descripción (ES)**  
Guardar recortes de logos de cada detección en `data/crops/{video_id}/` o bucket Supabase Storage `brandsight-crops`. Guardar `crop_path` en tabla `detections`. Asegurar que las rutas funcionen en el entorno desplegado (preferir URLs de Supabase Storage en producción).

**Acceptance criteria / Criterios de aceptación**
- [ ] Crop images saved for sample detections
- [ ] `crop_path` populated in Supabase
- [ ] Crops viewable from path/URL
- [ ] **Advanced DB requirement met**

---

### ISSUE-12 · AI marketing report generator / Generador de informe de marketing con IA

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 4–5 |
| **Responsible** | **A** (PO) |
| **Support** | B |
| **Labels** | `ai`, `report`, `day-4`, `day-5` |

**Description (EN)**  
Implement `src/report/generate_marketing_report.py`: read metrics from Supabase, build prompt (Coca-Cola analyst perspective), call Gemini or OpenAI API, save result to `marketing_reports` table. Report sections: Executive Summary, Coca-Cola Visibility, Pepsi Visibility, Competitive Comparison, Marketing Insights, Recommendation. Include Jinja2 template fallback if API unavailable.

**Descripción (ES)**  
Implementar `src/report/generate_marketing_report.py`: leer métricas de Supabase, construir prompt (perspectiva analista Coca-Cola), llamar API Gemini u OpenAI, guardar en tabla `marketing_reports`. Secciones: Resumen ejecutivo, Visibilidad Coca-Cola, Visibilidad Pepsi, Comparativa, Insights, Recomendación. Incluir plantilla Jinja2 como respaldo si la API falla.

**Acceptance criteria / Criterios de aceptación**
- [ ] Report generated from DB metrics only (no invented numbers)
- [ ] Report saved to `marketing_reports` table
- [ ] Coca-Cola client perspective in tone
- [ ] Fallback template works without API key

---

### ISSUE-13 · Streamlit web application / Aplicación web Streamlit

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 5 |
| **Responsible** | **A** (PO) |
| **Support** | B |
| **Labels** | `frontend`, `streamlit`, `expert`, `day-5` |

**Description (EN)**  
Build `app/streamlit_app.py`: video upload (or demo selector), run full pipeline, show progress, display annotated video, metrics cards (seconds, %, detection count), competitive bar chart, detection table with crop thumbnails, AI report markdown, optional analysis history from Supabase.

**Descripción (ES)**  
Construir `app/streamlit_app.py`: subida de vídeo (o selector demo), ejecutar pipeline completo, mostrar progreso, vídeo anotado, tarjetas de métricas (segundos, %, detecciones), gráfico de barras competitivo, tabla de detecciones con miniaturas, informe IA en markdown, historial opcional desde Supabase.

**Acceptance criteria / Criterios de aceptación**
- [ ] Upload → analyze → results flow works
- [ ] Metrics and chart displayed correctly
- [ ] AI report rendered in UI
- [ ] **Expert frontend requirement met**

---

### ISSUE-14 · Cloud deployment / Despliegue en la nube

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 5 |
| **Responsible** | **B** (SM) |
| **Support** | A |
| **Labels** | `deploy`, `expert`, `day-5` |

**Description (EN)**  
Deploy Streamlit app to Streamlit Community Cloud or Railway. Configure secrets: `DATABASE_URL`, `GEMINI_API_KEY` / `OPENAI_API_KEY`, `MODEL_PATH`. Optional `Dockerfile` for Railway. Bundle or download `best.pt` at deploy time. Verify end-to-end flow on live URL. Document deploy steps in README.

**Descripción (ES)**  
Desplegar app Streamlit en Streamlit Community Cloud o Railway. Configurar secrets: `DATABASE_URL`, `GEMINI_API_KEY` / `OPENAI_API_KEY`, `MODEL_PATH`. `Dockerfile` opcional para Railway. Incluir o descargar `best.pt` en deploy. Verificar flujo completo en URL en vivo. Documentar pasos en README.

**Acceptance criteria / Criterios de aceptación**
- [ ] Public URL accessible
- [ ] Deployed app connects to Supabase
- [ ] Full demo works on live URL (not just local)
- [ ] Secrets not exposed in repo or logs

---

### ISSUE-15 · README & technical documentation / README y documentación técnica

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 2–6 |
| **Responsible** | **A** (PO) |
| **Support** | B |
| **Labels** | `docs`, `day-2`, `day-6` |

**Description (EN)**  
Write project README: problem statement, setup instructions, env vars, how to train (Colab), how to run locally, how to deploy, architecture diagram, team roles, link to live demo URL. Document preprocessing, augmentations, and frame sampling assumptions.

**Descripción (ES)**  
Escribir README del proyecto: planteamiento, instrucciones de setup, variables de entorno, cómo entrenar (Colab), cómo ejecutar en local, cómo desplegar, diagrama de arquitectura, roles del equipo, enlace a demo en vivo. Documentar preprocesado, augmentations y suposiciones de muestreo de frames.

**Acceptance criteria / Criterios de aceptación**
- [ ] README complete in repo root
- [ ] Setup works for new teammate from README alone
- [ ] Live demo URL linked
- [ ] Evaluation criteria addressed (preprocessing, dataset, fine-tune, augmentations)

---

### ISSUE-16 · Presentation & live demo rehearsal / Presentación y ensayo de demo en vivo

| Field | Value |
|-------|-------|
| **Status** | To Do |
| **Sprint day** | Day 5–6 |
| **Responsible** | **A** (PO) |
| **Support** | All |
| **Labels** | `presentation`, `day-5`, `day-6` |

**Description (EN)**  
Prepare technical presentation: problem → solution → architecture → live demo on deployed URL → **local webcam segment** → tech stack → limitations → future work. Assign speaking parts to A, B, C. Run 15-min dry-run on Day 5 and final rehearsal on Day 6. SM closes Kanban, tags release `v1.0-demo`.

**Descripción (ES)**  
Preparar presentación técnica: problema → solución → arquitectura → demo en URL desplegada → **segmento webcam local** → stack → limitaciones → trabajo futuro. Asignar partes a A, B, C. Ensayo de 15 min el Día 5 y ensayo final el Día 6. SM cierra Kanban y tag `v1.0-demo`.

**Acceptance criteria / Criterios de aceptación**
- [ ] Slide deck ready (6–10 slides)
- [ ] Live demo script written and rehearsed
- [ ] Each teammate has a speaking section
- [ ] Kanban 100% Done or Won't Do · release tagged

---

## Sprint day map / Mapa por día

| Day | Issues to target / Incidencias objetivo |
|-----|----------------------------------------|
| **Day 1** | ISSUE-01, 02, 03, 05 (start), 06 (smoke) |
| **Day 2** | ISSUE-04, 05 (finish), 06, 07, 17 (start), 15 (start) |
| **Day 3** | ISSUE-08, 09, 17 (finish) |
| **Day 4** | ISSUE-10, 11, 12 (start) |
| **Day 5** | ISSUE-12 (finish), 13, 14, 16 (dry-run) |
| **Day 6** | ISSUE-15 (finish), 16 (final), bug fixes |

---

## Delivery level checklist / Checklist por nivel de entrega

| Level / Nivel | Issue(s) / Incidencia(s) | Owner |
|---------------|--------------------------|-------|
| 🟢 Essential | ISSUE-07 | C + B |
| 🟡 Medium | ISSUE-09, 17 | B + C |
| 🟠 Advanced | ISSUE-10, 11, 12 | B + A |
| 🔴 Expert | ISSUE-13, 14 | A + B |

---

## Daily standup template / Plantilla daily

```
Yesterday / Ayer:     [what I did]
Today / Hoy:          [ISSUE-XX]
Blockers / Bloqueos:  [none / describe]
```

---

## Import to GitHub Projects / Importar a GitHub Projects

**Repo:** [Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1](https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1)  
**GitHub Project URL:** _← SM (B) paste link here after board is created_

### Setup steps (SM — ~15 min)

1. GitHub repo → **Projects** → **New project** → **Board** template  
2. Columns: `Backlog` · `To Do` · `In Progress` · `In Review` · `Done`  
3. Project description → link this file and planning docs:
   - `docs/KANBAN.md`
   - `docs/SCOPE.md`
   - `docs/USER_STORIES.md`
4. Create **17 issues** (one per `ISSUE-01` … `ISSUE-17`): copy title + description + acceptance criteria from [KANBAN.md](./KANBAN.md)  
5. Add labels: `day-1` … `day-6`, `planning`, `ml`, `backend`, `frontend`, `deploy`, `infra`, etc.  
6. Assign owner: A, B, or C per issue table  
7. Set ISSUE-02 → **Done** after team signs off DoD in the 30-min meeting  

### Bulk issue titles (copy-paste)

```
ISSUE-01 · Project setup & repository
ISSUE-02 · Sprint planning & user stories
ISSUE-03 · Supabase project & database schema
ISSUE-04 · Supabase connection layer
ISSUE-05 · Roboflow dataset — Coca-Cola & Pepsi
ISSUE-06 · Google Colab training notebook
ISSUE-07 · Image detection script
ISSUE-17 · Local webcam detection
ISSUE-08 · Demo videos collection
ISSUE-09 · Video detection + labels + confidence
ISSUE-10 · Visibility metrics & competitive analysis
ISSUE-11 · Bbox crops & database persistence
ISSUE-12 · AI marketing report generator
ISSUE-13 · Streamlit web application
ISSUE-14 · Cloud deployment
ISSUE-15 · README & technical documentation
ISSUE-16 · Presentation & live demo rehearsal
```

---

_Last updated: ISSUE-17 local webcam added to scope (Day 1)_

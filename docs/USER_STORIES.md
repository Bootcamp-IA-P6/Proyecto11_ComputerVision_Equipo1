# BrandSight — User Stories & Definition of Done

**Sprint:** 6 days · **Issue:** ISSUE-02  
**Owner:** A (PO) · **Support:** B, C

Related: [SCOPE.md](./SCOPE.md) · [KANBAN.md](./KANBAN.md) · [PLAN_PROYECTO.md](./PLAN_PROYECTO.md)

---

## Persona

**Marketing analyst at Coca-Cola** — uploads sponsorship or ad videos and needs objective visibility metrics vs Pepsi, stored for reporting and summarized by AI.

---

## User stories by theme

Stories use format: **As a… I want… So that…**  
Priority maps to delivery level. GitHub issues: `ISSUE-XX` in [KANBAN.md](./KANBAN.md).

### Upload / Subida

| ID | Story (EN) | Story (ES) | Priority | Issue |
|----|------------|------------|----------|-------|
| US-01 | As a **marketing analyst**, I want to **upload an MP4 video** (or pick a demo clip) so that **I can analyze brand visibility without using the command line**. | Como **analista de marketing**, quiero **subir un vídeo MP4** (o elegir un demo) para **analizar visibilidad de marca sin usar la terminal**. | Expert | ISSUE-13 |
| US-02 | As a **marketing analyst**, I want to **see upload progress and processing status** so that **I know the analysis is running and when it finishes**. | Como **analista**, quiero **ver progreso y estado del procesado** para **saber que el análisis está en curso y cuándo termina**. | Expert | ISSUE-13 |
| US-03 | As a **PO**, I want **2–3 reliable demo videos** (30–60 s, both brands) so that **the live presentation never depends on a random upload**. | Como **PO**, quiero **2–3 vídeos demo fiables** (30–60 s, ambas marcas) para **que la demo en vivo no dependa de un upload aleatorio**. | Medium | ISSUE-08 |

**Acceptance hints:** H.264 MP4; max practical size for free-tier Supabase; demo selector works on deployed URL.

---

### Detect / Detección

| ID | Story (EN) | Story (ES) | Priority | Issue |
|----|------------|------------|----------|-------|
| US-04 | As a **data scientist**, I want to **run YOLO on a single image** and see **bounding boxes with brand labels** so that **we prove the model works before video**. | Como **científico de datos**, quiero **ejecutar YOLO en una imagen** y ver **bbox con etiquetas de marca** para **validar el modelo antes del vídeo**. | Essential | ISSUE-07 |
| US-05 | As a **marketing analyst**, I want **frame-by-frame logo detection on video** with **brand name under each box** so that **I can see where each brand appears**. | Como **analista**, quiero **detección frame a frame en vídeo** con **nombre de marca bajo cada caja** para **ver dónde aparece cada marca**. | Medium | ISSUE-09 |
| US-06 | As a **marketing analyst**, I want **confidence % shown on each detection** so that **I can judge how reliable each logo match is**. | Como **analista**, quiero **ver el % de confianza en cada detección** para **valorar la fiabilidad de cada match**. | Advanced | ISSUE-09 |
| US-07 | As an **ML engineer**, I want a **Roboflow dataset with ≥80 images per brand** and a **Colab training notebook** so that **the team can reproduce `best.pt`**. | Como **ML engineer**, quiero un **dataset Roboflow con ≥80 imágenes por marca** y un **notebook Colab** para **reproducir `best.pt`**. | Essential | ISSUE-05, ISSUE-06 |
| US-18 | As a **presenter**, I want **realtime webcam detection on my laptop** with **brand labels and confidence %** so that **I can demo live logo recognition during the presentation without relying on cloud CPU**. | Como **presentador**, quiero **detección en tiempo real con webcam en mi portátil** con **etiquetas de marca y % de confianza** para **demostrar reconocimiento de logos en vivo durante la presentación sin depender de CPU en cloud**. | Medium | ISSUE-17 |

**Acceptance hints:** Classes locked to `coca_cola`, `pepsi`; `CONFIDENCE_THRESHOLD=0.5`; works on Linux, Mac, Windows. Webcam runs **locally only** — not part of deployed Streamlit app.

---

### Metrics / Métricas

| ID | Story (EN) | Story (ES) | Priority | Issue |
|----|------------|------------|----------|-------|
| US-08 | As a **marketing analyst**, I want **visible seconds and visibility % per brand** so that **I can compare Coca-Cola vs Pepsi screen time**. | Como **analista**, quiero **segundos visibles y % de visibilidad por marca** para **comparar tiempo en pantalla Coca-Cola vs Pepsi**. | Advanced | ISSUE-10 |
| US-09 | As a **marketing analyst**, I want a **dominant brand and balance label** (`coca_cola_dominant`, `pepsi_dominant`, `balanced`) so that **I get a clear competitive verdict**. | Como **analista**, quiero **marca dominante y etiqueta de balance** para **obtener un veredicto competitivo claro**. | Advanced | ISSUE-10 |
| US-10 | As a **marketing analyst**, I want **detection rows and bbox crops stored in Supabase** so that **results are auditable after the demo**. | Como **analista**, quiero **filas de detección y recortes bbox en Supabase** para **auditar resultados después de la demo**. | Advanced | ISSUE-09, ISSUE-11 |
| US-11 | As a **marketing analyst**, I want **metrics shown as cards and a bar chart** in the web app so that **stakeholders understand results at a glance**. | Como **analista**, quiero **métricas en tarjetas y gráfico de barras** en la web para **que stakeholders entiendan el resultado de un vistazo**. | Expert | ISSUE-13 |

**Acceptance hints:** Metrics match manual spot-check on demo video; `SAMPLE_STRIDE` documented in README.

---

### Report / Informe

| ID | Story (EN) | Story (ES) | Priority | Issue |
|----|------------|------------|----------|-------|
| US-12 | As a **Coca-Cola client**, I want an **AI-generated marketing report** from stored metrics only so that **I receive actionable insights without invented numbers**. | Como **cliente Coca-Cola**, quiero un **informe de marketing generado por IA** solo con métricas almacenadas para **recibir insights accionables sin cifras inventadas**. | Advanced | ISSUE-12 |
| US-13 | As a **PO**, I want a **Jinja2 fallback report** when the LLM API is down so that **the demo never blocks on an external service**. | Como **PO**, quiero un **informe plantilla Jinja2** si falla la API LLM para **que la demo no se bloquee**. | Advanced | ISSUE-12 |
| US-14 | As a **marketing analyst**, I want the **report rendered as Markdown in Streamlit** with copy/download so that **I can share it after the meeting**. | Como **analista**, quiero el **informe en Markdown en Streamlit** con copiar/descargar para **compartirlo tras la reunión**. | Expert | ISSUE-13 |

**Report sections:** Executive Summary · Coca-Cola Visibility · Pepsi Visibility · Competitive Comparison · Marketing Insights · Recommendation.

---

### Deploy / Despliegue

| ID | Story (EN) | Story (ES) | Priority | Issue |
|----|------------|------------|----------|-------|
| US-15 | As a **presenter**, I want a **public HTTPS URL** for the Streamlit app so that **the jury sees a live cloud demo, not localhost**. | Como **presentador**, quiero una **URL pública HTTPS** de la app Streamlit para **que el jurado vea demo en cloud, no localhost**. | Expert | ISSUE-14 |
| US-16 | As an **SM**, I want **secrets configured on the host** (`DATABASE_URL`, LLM key, model path) so that **credentials never appear in Git or logs**. | Como **SM**, quiero **secretos configurados en el host** para **que credenciales no aparezcan en Git ni logs**. | Expert | ISSUE-14 |
| US-17 | As a **teammate**, I want **documented deploy steps in README** so that **anyone can redeploy after the sprint**. | Como **compañero**, quiero **pasos de deploy documentados en README** para **cualquiera pueda redesplegar tras el sprint**. | Expert | ISSUE-14, ISSUE-15 |

---

## Definition of Done by delivery level

Team agrees in the **30-min Day 1 meeting**. Check boxes when level is truly shippable.

### 🟢 Essential / Esencial (Day 1–2)

**Maps to:** ISSUE-05, ISSUE-06, ISSUE-07 · briefing Essential + repo hygiene

- [ ] YOLO model detects **at least one brand** (`coca_cola` or `pepsi`) in a **single test image**
- [ ] Output image shows **visible bounding box** and **brand label**
- [ ] CLI works: `python -m src.detect_image --image <path> --weights models/best.pt`
- [ ] Runs on **Linux, Mac, and Windows** (same `requirements.txt`)
- [ ] Roboflow project exists with **2 classes**; **≥80 annotated images per brand** (or documented progress if Day 2 morning)
- [ ] Colab notebook committed (**no secrets, no dataset blobs**)
- [ ] Git: feature branches → PR → `develop`; commits are descriptive
- [ ] README section: how to install and run image detection

**Not required yet:** video, database, web UI, deploy.

---

### 🟡 Medium / Medio (Day 2–3)

**Maps to:** ISSUE-08, ISSUE-09, ISSUE-17 · briefing Medium + realtime detection (eval criteria)

- [ ] `detect_video.py` processes a **30 s demo MP4** end-to-end
- [ ] Annotated output video saved; **brand name under each detection**
- [ ] Detections **inserted into Supabase** `detections` table linked to `videos`
- [ ] **Both brands** (`coca_cola`, `pepsi`) detectable in model (2-class multibrand)
- [ ] ≥2 demo videos in Team Drive; at least one clip reliable for live demo
- [ ] MP4 **H.264** for Windows compatibility verified
- [ ] **`detect_webcam.py`** runs locally: live window with bbox + brand label + confidence %; quit with `q`
- [ ] CLI works: `python -m src.detect_webcam --weights models/best.pt` (optional `--camera 0`)
- [ ] Webcam demo tested on **Linux, Mac, and Windows** before presentation

**Not required yet:** confidence overlay on batch video (if not done), visibility seconds/%, AI report, Streamlit deploy.

---

### 🟠 Advanced / Avanzado (Day 3–4)

**Maps to:** ISSUE-10, ISSUE-11, ISSUE-12 · briefing Advanced

- [ ] **Confidence %** visible on video overlay and stored in DB
- [ ] **Visibility metrics** per brand: seconds, %, detection count, avg confidence
- [ ] `brand_summary` and `competitive_analysis` rows written for analyzed video
- [ ] **Bbox crops** saved (`data/crops/` or Supabase Storage); `crop_path` in `detections`
- [ ] **AI marketing report** generated from DB metrics only; saved to `marketing_reports`
- [ ] **Jinja2 fallback** works without LLM API key
- [ ] Frame sampling assumption documented (`SAMPLE_STRIDE`, confidence threshold)

**Not required yet:** Streamlit UI, public deploy URL.

---

### 🔴 Expert / Experto (Day 5–6)

**Maps to:** ISSUE-13, ISSUE-14 · briefing Expert

- [ ] Streamlit app: **upload → analyze → results** (video, metrics, chart, report)
- [ ] App deployed to **Streamlit Cloud or Railway** with **public URL**
- [ ] Deployed app connects to **Supabase**; full demo works on live URL
- [ ] Secrets only in platform env / `.env` (never committed)
- [ ] Optional: analysis history list from Supabase
- [ ] Optional stretch: REST API wrapper — **only if Expert UI + deploy are Done**

**Sprint is "done" when:** jury can run the full flow on the **deployed URL** during presentation.

---

## Story → issue traceability

| Theme | User stories | Primary issues |
|-------|--------------|----------------|
| Upload | US-01, US-02, US-03 | ISSUE-08, ISSUE-13 |
| Detect | US-04–US-07, US-18 | ISSUE-05, ISSUE-06, ISSUE-07, ISSUE-09, ISSUE-17 |
| Metrics | US-08–US-11 | ISSUE-09, ISSUE-10, ISSUE-11, ISSUE-13 |
| Report | US-12–US-14 | ISSUE-12, ISSUE-13 |
| Deploy | US-15–US-17 | ISSUE-14, ISSUE-15 |

---

## Planning meeting agenda (30 min)

1. **5 min** — PO presents [SCOPE.md](./SCOPE.md); team signs off on 2-brand freeze  
2. **10 min** — Walk through user stories above; assign owners A/B/C  
3. **10 min** — Agree Definition of Done checklists per level  
4. **5 min** — SM creates GitHub Project board; link repo docs in project description  

**Blocker note:** ISSUE-01 (repo setup) can proceed in parallel; planning docs do not depend on ISSUE-01 approval.

---

## Team sign-off — Definition of Done

| Teammate | DoD levels agreed | Date |
|----------|-------------------|------|
| _[name]_ — A (PO) | Essential · Medium · Advanced · Expert | |
| _[name]_ — B (SM) | Essential · Medium · Advanced · Expert | |
| _[name]_ — C (ML) | Essential · Medium · Advanced · Expert | |

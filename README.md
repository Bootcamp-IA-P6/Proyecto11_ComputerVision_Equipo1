# BrandSight 🥤

**Coca-Cola vs Pepsi — Brand Visibility Analysis / Análisis de Visibilidad de Marca**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![YOLO11](https://img.shields.io/badge/YOLO11-large-0055FF?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Gemini-API-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**🇬🇧** An AI-powered computer vision application that analyzes video content to measure and compare brand visibility between Coca-Cola and Pepsi. Upload a video, and the system detects logo appearances, calculates visibility metrics, and generates an AI marketing report.

**🇪🇸** Una aplicación de visión artificial impulsada por IA que analiza contenido de vídeo para medir y comparar la visibilidad de marca entre Coca-Cola y Pepsi. Sube un vídeo y el sistema detecta apariciones de logos, calcula métricas de visibilidad y genera un informe de marketing con IA.

🎥 **Demo** [Ver vídeo de demostración](docs/computer-vision-demo.mp4)

📄 **Presentation / Presentación:** [View PDF / Ver PDF](docs/BrandSight_Bold.pdf)

---

## 📋 Table of Contents / Índice

- [Problem Statement / Planteamiento del Problema](#problem-statement--planteamiento-del-problema)
- [Features / Funcionalidades](#features--funcionalidades)
- [Architecture / Arquitectura](#architecture--arquitectura)
- [Project Structure / Estructura del Proyecto](#project-structure--estructura-del-proyecto)
- [Setup Instructions / Instrucciones de Configuración](#setup-instructions--instrucciones-de-configuración)
- [Model Training / Entrenamiento del Modelo](#model-training--entrenamiento-del-modelo)
- [Demo Videos / Vídeos Demo](#demo-videos--vídeos-demo)
- [How to Run Locally / Cómo Ejecutar en Local](#how-to-run-locally--cómo-ejecutar-en-local)
- [How to Deploy / Cómo Desplegar](#how-to-deploy--cómo-desplegar)
- [Verification Scripts / Scripts de Verificación](#verification-scripts--scripts-de-verificación)
- [Evaluation Criteria / Criterios de Evaluación](#evaluation-criteria--criterios-de-evaluación)
- [Team Roles / Roles del Equipo](#team-roles--roles-del-equipo)

---

## Problem Statement / Planteamiento del Problema

### 🇬🇧 English

In competitive marketing, understanding brand visibility in video content (TV commercials, sports events, social media) is crucial for measuring sponsorship ROI and campaign effectiveness. Manual analysis is time-consuming, subjective, and doesn't scale.

**BrandSight** automates this process by:

1. **Detecting** Coca-Cola and Pepsi logos in video frames using a fine-tuned YOLOv8 nano model
2. **Quantifying** visibility metrics (screen time, detection count, confidence scores)
3. **Comparing** competitive presence between the two brands
4. **Generating** AI-powered marketing reports with actionable insights

**Key Questions Answered:**
- What percentage of screen time does each brand occupy?
- Which brand dominates the video?
- What is the visibility gap between competitors?
- Where should marketing efforts be focused?

### 🇪🇸 Español

En marketing competitivo, entender la visibilidad de marca en contenido de vídeo (anuncios de TV, eventos deportivos, redes sociales) es crucial para medir el ROI de patrocinios y la efectividad de campañas. El análisis manual es lento, subjetivo y no escala.

**BrandSight** automatiza este proceso mediante:

1. **Detección** de logos de Coca-Cola y Pepsi en fotogramas de vídeo usando un modelo YOLOv8 nano fine-tuned
2. **Cuantificación** de métricas de visibilidad (tiempo en pantalla, número de detecciones, puntuaciones de confianza)
3. **Comparación** de presencia competitiva entre las dos marcas
4. **Generación** de informes de marketing con IA e insights accionables

**Preguntas clave que responde:**
- ¿Qué porcentaje de tiempo en pantalla ocupa cada marca?
- ¿Qué marca domina el vídeo?
- ¿Cuál es la brecha de visibilidad entre competidores?
- ¿Dónde deberían enfocarse los esfuerzos de marketing?

---

## Features / Funcionalidades

| 🇬🇧 English | 🇪🇸 Español |
|------------|------------|
| 🎥 **Video Upload & Processing** — MP4 up to 200MB | 🎥 **Subida y procesado de vídeo** — MP4 hasta 200MB |
| 🔍 **Logo Detection** — YOLOv11 large fine-tuned | 🔍 **Detección de logos** — YOLOv11 large ajustado |
| 📊 **Visibility Metrics** — Screen time, detections, confidence | 📊 **Métricas de visibilidad** — Tiempo, detecciones, confianza |
| 📈 **Competitive Analysis** — Dominant brand, visibility gap | 📈 **Análisis competitivo** — Marca dominante, brecha |
| 🤖 **AI Marketing Report** — Gemini + Jinja2 fallback | 🤖 **Informe IA** — Gemini + plantilla de respaldo |
| 🖼️ **Detection Gallery** — Bounding box crops | 🖼️ **Galería de detecciones** — Recortes de logos |
| 🎬 **Annotated Video** — Output with drawn detections | 🎬 **Vídeo anotado** — Salida con detecciones dibujadas |
| 💾 **Supabase Persistence** — All results in PostgreSQL | 💾 **Persistencia Supabase** — Resultados en PostgreSQL |
| 🌐 **Bilingual UI** — English / Spanish | 🌐 **Interfaz bilingüe** — Inglés / Español |

---

## Architecture / Arquitectura

```
┌──────────────────────────────────────────────────────────────┐
│             USER INTERFACE / INTERFAZ DE USUARIO             │
│              Streamlit (app/streamlit_app.py)                 │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ Video Upload │  │ Brand Metrics│  │ Detection Gallery  │   │
│  │ Demo Select  │  │ Bar Chart    │  │ AI Report (MD)     │   │
│  └─────────────┘  └──────────────┘  └────────────────────┘   │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│              ORCHESTRATOR / ORQUESTADOR                       │
│                    src/pipeline.py                            │
│        analyze_video() — coordinates entire analysis flow     │
└──────────────────────────┬───────────────────────────────────┘
                           │
     ┌─────────────────────┼─────────────────────┐
     ▼                     ▼                     ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────────┐
│  DETECTION  │    │   METRICS    │    │   AI REPORT      │
│  DETECCIÓN  │    │   MÉTRICAS   │    │   INFORME IA     │
│             │    │              │    │                  │
│ YOLOv11 large │    │ Visibility   │    │ Gemini +  │
│ detect_video│    │ Competitive  │    │ Jinja2 fallback  │
│ crops.py    │    │ metrics.py   │    │ marketing_report │
└──────┬──────┘    └──────┬───────┘    └────────┬─────────┘
       │                  │                     │
       └──────────────────┼─────────────────────┘
                          │
              ┌───────────▼───────────┐
              │      DATABASE         │
              │   Supabase PostgreSQL │
              │  • videos             │
              │  • detections         │
              │  • brand_summary      │
              │  • competitive_analysis│
              │  • marketing_reports  │
              └───────────────────────┘
```

**Data Flow / Flujo de datos:**
1. User uploads video → saved to `data/uploads/` / El usuario sube un vídeo → guardado en `data/uploads/`
2. `pipeline.py` orchestrates / orquesta:
   - `detect_video.py` — runs YOLO on every Nth frame / ejecuta YOLO cada N fotogramas
   - `crops.py` — extracts bounding box regions / extrae regiones de bounding box
   - `metrics.py` — calculates visibility percentages / calcula porcentajes de visibilidad
   - `generate_marketing_report.py` — generates AI insights / genera insights con IA
3. Results persisted to Supabase PostgreSQL / Resultados persistidos en Supabase PostgreSQL
4. UI displays metrics, charts, crops, and report / La UI muestra métricas, gráficos, recortes e informe

---

## Project Structure / Estructura del Proyecto

```
brandsight/
├── .streamlit/
│   ├── config.toml                # Theme, server settings / Tema, configuración servidor
│   └── secrets.toml.example       # Credentials template / Plantilla de credenciales
├── app/
│   ├── streamlit_app.py           # UI — tabs, widgets, visualizations
│   └── bootstrap_secrets.py       # Injects secrets into os.environ
├── src/
│   ├── config.py                  # Pydantic settings (env vars → typed config)
│   ├── pipeline.py                # Main orchestrator / Orquestador principal
│   ├── detect_video.py            # YOLO video processing / Procesado de vídeo
│   ├── detect_image.py            # YOLO single image inference / Inferencia en imagen
│   ├── crops.py                   # Bbox crop extraction / Extracción de recortes
│   ├── metrics.py                 # Visibility & competitive analysis / Métricas
│   ├── metrics_export.py          # JSON/TXT export + CLI viewer
│   ├── db/
│   │   ├── connection.py          # SQLAlchemy engine, sessions, schema checks
│   │   ├── models.py              # ORM models — 5 tables / 5 tablas
│   │   └── repository.py          # CRUD operations
│   └── report/
│       └── generate_marketing_report.py  # AI report generation / Generación informe IA
├── scripts/
│   ├── check_db.py                # Verify DB connection & schema
│   ├── check_detect_image.py      # Quick model test on image
│   ├── download_demo_videos.py    # Auto-download demo videos with yt-dlp
│   ├── smoke_deploy.py            # Pre-deploy verification
│   ├── test_db_insert.py          # DB round-trip test
│   └── verify_crops.py            # Verify crop files exist
├── notebooks/
│   └── train_colab.ipynb          # YOLO training notebook / Notebook entrenamiento
├── sql/
│   ├── schema.sql                 # Database schema DDL / Esquema de BD
│   └── storage.sql                # Supabase Storage bucket setup
├── data/                          # gitignored
│   ├── crops/                     # Extracted detection crops / Recortes de detecciones
│   ├── uploads/                   # Uploaded videos / Vídeos subidos
│   ├── outputs/                   # Annotated videos, metrics / Vídeos anotados, métricas
│   └── demo/                      # Demo videos — see Demo Videos section
├── models/
│   └── best.pt                    # YOLOv8 nano weights — gitignored / pesos — no en Git
├── docs/
│   └── presentation.pdf           # Project presentation / Presentación del proyecto
├── Dockerfile
├── .env.example
├── requirements.txt
├── packages.txt                   # System deps for Streamlit Cloud / Deps del sistema
└── runtime.txt                    # Python version for Streamlit Cloud
```

---

## Setup Instructions / Instrucciones de Configuración

### Prerequisites / Prerrequisitos

- **Python 3.11**
- **Git**
- **Supabase account** (free tier / plan gratuito)
- **Google Gemini API key** 
- **Streamlit Cloud account** *(for deploy / para despliegue)*

### Local Development / Desarrollo Local

```bash
# 1. Clone / Clonar
git clone https://github.com/Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1.git
cd Proyecto11_ComputerVision_Equipo1

# 2. Virtual environment / Entorno virtual
python -m venv .venv
source .venv/bin/activate       # Linux/Mac
# .venv\Scripts\activate        # Windows

# 3. Install / Instalar
pip install -r requirements.txt

# 4. Environment variables / Variables de entorno
cp .env.example .env
# Edit .env with your values / Edita .env con tus valores (ask SM for DATABASE_URL)

# 5. Streamlit secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Same values as .env / Mismos valores que .env

# 6. Supabase — run in SQL Editor / ejecutar en SQL Editor
# sql/schema.sql   → creates 5 tables / crea 5 tablas
# sql/storage.sql  → optional crops bucket / bucket opcional

# 7. Demo videos / Vídeos demo
python scripts/download_demo_videos.py

# 8. Verify / Verificar
python scripts/smoke_deploy.py
```

### Environment Variables / Variables de Entorno

| Variable | Required / Requerida | Description / Descripción | Where / Dónde |
|----------|----------------------|---------------------------|---------------|
| `DATABASE_URL` | ✅ | Supabase PostgreSQL connection string | Supabase → Settings → Database → URI |
| `SUPABASE_URL` | ❌ | Supabase project URL | Supabase → Settings → API |
| `SUPABASE_SERVICE_ROLE_KEY` | ❌ | Service role key | Supabase → Settings → API |
| `GEMINI_API_KEY` | ❌ | Google Gemini API key | Google AI Studio |
| `MODEL_PATH` | ❌ | Path to YOLO weights | Default: `models/best.pt` |
| `CONFIDENCE_THRESHOLD` | ❌ | Min detection confidence / Confianza mínima | Default: `0.5` |
| `SAMPLE_STRIDE` | ❌ | Process every Nth frame / Procesar cada N frames | Default: `3` |

---

## Model Training / Entrenamiento del Modelo

### Dataset

**🇬🇧** Custom dataset of Coca-Cola and Pepsi logos, managed with **Roboflow**.
**🇪🇸** Dataset personalizado de logos de Coca-Cola y Pepsi, gestionado con **Roboflow**.

- **Classes / Clases:** `coca_cola` · `pepsi`
- **Source / Fuente:** TV commercials, sports events, product placement / Anuncios, eventos deportivos, product placement
- **Format / Formato:** YOLOv11 bounding boxes
- **Split / División:** Train / Validation / Test (Roboflow standard)

### Preprocessing & Augmentations / Preprocesado y Augmentaciones

| Step / Paso | Detail / Detalle |
|-------------|------------------|
| Resize / Redimensionar | 640×640 px (YOLOv11 standard) |
| Normalization / Normalización | [0, 1] — automatic via ultralytics |
| Format / Formato | RGB conversion if needed / Conversión a RGB si necesario |

| Augmentation / Augmentación | Parameter | Purpose / Propósito |
|-----------------------------|-----------|---------------------|
| Horizontal, Vertical Flip / Volteo horizontal, vertical | p=0.5 | Left & right logo orientations |
| Rotation / Rotación | ±180° | Robustness to tilt / Robustez ante inclinación |
| Brightness / Brillo | ±25% | Lighting variations / Variaciones de luz |
| Contrast / Contraste | ±25% | Environment variation / Variación de entorno |
| Scale / Escala | ±50% | Different distances / Distintas distancias |
| Mosaic / Mosaico | p=1.0 | Better context learning / Mejor aprendizaje contextual |

### Training Configuration / Configuración de Entrenamiento

| Parameter | Value | Rationale / Justificación |
|-----------|-------|---------------------------|
| Model / Modelo | YOLOv8 nano (`yolo11l.pt`) | ~6MB, fast inference, fits Streamlit Cloud |
| Epochs / Épocas | 50 | Sufficient for 2-class transfer learning |
| Image size / Tamaño | 640 | YOLOv8 standard |
| Batch size / Lote | 16 | Fits Colab T4 GPU |
| Optimizer | AdamW | YOLOv11 default |
| Learning rate | 0.001 | Fine-tuning from COCO weights |

**To retrain / Para re-entrenar:**
1. Open `notebooks/train_colab.ipynb` in Google Colab
2. Set Roboflow API key / Configura la API key de Roboflow
3. Run all cells / Ejecuta todas las celdas
4. Download `best.pt` → place in `models/` / Descarga y coloca en `models/`

### Frame Sampling / Muestreo de Fotogramas

```
frame_interval  = sample_stride / fps
visible_seconds = unique_detected_frames × frame_interval
visibility_pct  = (visible_seconds / total_duration) × 100
```

| Parameter | Default | Meaning / Significado |
|-----------|---------|----------------------|
| `SAMPLE_STRIDE` | 3 | Every 3rd frame / Cada 3 fotogramas |
| `CONFIDENCE_THRESHOLD` | 0.5 | Min 50% confidence / Confianza mínima 50% |

**Stride tradeoff / Compromiso:**
- `stride=1` → most accurate / más preciso, 3× slower / más lento
- `stride=3` → good balance / buen equilibrio *(default)*
- `stride=5` → faster / más rápido, may miss brief appearances / puede perder apariciones breves

---

## Demo Videos / Vídeos Demo

**🇬🇧** Demo videos are not stored in Git. Download automatically with:
**🇪🇸** Los vídeos demo no están en Git. Descárgalos automáticamente con:

```bash
python scripts/download_demo_videos.py
```

Alternatively, copy from team Google Drive `Team Drive/demo_videos/` /
Alternativamente, cópialos del Google Drive del equipo `Team Drive/demo_videos/`.

| File / Archivo | Duration / Duración | Source / Fuente |
|----------------|---------------------|-----------------|
| `demo1.mp4` | 45s | YouTube |
| `demo2.mp4` | 29s | YouTube |
| `demo3.mp4` | 36s | YouTube |
| `demo4.mp4` | 62s | YouTube |

---

## How to Run Locally / Cómo Ejecutar en Local

```bash
source .venv/bin/activate

# Web app / Aplicación web
streamlit run app/streamlit_app.py
# → http://localhost:8501

# CLI tools / Herramientas CLI
python scripts/check_db.py                       # DB check / Verificar BD
python scripts/check_detect_image.py             # Model test / Probar modelo
python scripts/smoke_deploy.py                   # Pre-deploy checks
python scripts/test_db_insert.py                 # DB round-trip test
python scripts/verify_crops.py --video-id 1      # Verify crops / Verificar recortes
python scripts/download_demo_videos.py           # Download demo videos
```

---

## How to Deploy / Cómo Desplegar

### Streamlit Cloud

```bash
# 1. Push to GitHub / Sube a GitHub
git push origin main

# 2. Go to / Ve a: https://streamlit.io/cloud
# 3. New app → select repo → main file: app/streamlit_app.py
# 4. Add secrets / Añade secrets (App → Settings → Secrets):
```

```toml
DATABASE_URL          = "postgresql://..."
GEMINI_API_KEY        = "your_key"
MODEL_PATH            = "models/best.pt"
CONFIDENCE_THRESHOLD  = "0.5"
SAMPLE_STRIDE         = "3"
```

> Streamlit Cloud reads `runtime.txt`, `packages.txt`, and `requirements.txt` automatically /
> Streamlit Cloud lee `runtime.txt`, `packages.txt` y `requirements.txt` automáticamente.

### Docker

```bash
docker build -t brandsight .
docker run -p 8501:8501 --env-file .env brandsight
```

---

## Verification Scripts / Scripts de Verificación

| Script | Purpose / Propósito | Usage / Uso |
|--------|---------------------|-------------|
| `check_db.py` | Verify Supabase connection & schema / Verificar conexión y esquema | `python scripts/check_db.py` |
| `check_detect_image.py` | Quick YOLO test / Prueba rápida del modelo | `python scripts/check_detect_image.py` |
| `download_demo_videos.py` | Auto-download demo videos / Descarga automática | `python scripts/download_demo_videos.py` |
| `smoke_deploy.py` | Full pre-deploy verification / Verificación completa | `python scripts/smoke_deploy.py` |
| `test_db_insert.py` | DB round-trip test / Prueba CRUD completa | `python -m scripts.test_db_insert` |
| `verify_crops.py` | Check crop files / Verificar recortes en disco | `python scripts/verify_crops.py --video-id 1` |

```bash
# Run all before deploying / Ejecutar todo antes de desplegar
python scripts/smoke_deploy.py && python -m scripts.test_db_insert
```

---

## Evaluation Criteria / Criterios de Evaluación

| Criterion / Criterio | Implementation / Implementación |
|----------------------|--------------------------------|
| **Dataset** | Custom Roboflow dataset — 2 classes (`coca_cola`, `pepsi`) — bounding box annotations |
| **Preprocessing** | 640×640 resize · automatic normalization via ultralytics |
| **Fine-tuning** | YOLOv11 large pretrained on COCO → 50 epochs → 2-class specialization |
| **Augmentations** | Flip · Rotation · Brightness · Contrast · Scale · Mosaic |
| **Real-time detection** | `detect_webcam.py` — local live demo during presentation / demo en vivo durante presentación |
| **Frame sampling** | Stride-based (default 3) · configurable via `SAMPLE_STRIDE` |

---

## Team Roles / Roles del Equipo

| Role / Rol | Responsibilities / Responsabilidades |
|------------|--------------------------------------|
| **Product Owner (Mar Izquierdo Vaquer)** | Scope · user stories · README · demo videos · AI report · Streamlit UI · presentation / Alcance · historias de usuario · README · vídeos demo · informe IA · UI Streamlit · presentación |
| **Scrum Master + Backend (Mirae Kang)** | Kanban · Git/PRs · pipeline · Supabase · metrics · crops · deployment / Kanban · Git/PRs · pipeline · Supabase · métricas · recortes · despliegue |
| **ML Engineer (Juan Miguel Iriondo Ortega)** | Dataset (Roboflow) · training (Colab) · `best.pt` · `detect_image` · `detect_webcam` |

---

---

*Desarrollado como proyecto educativo para el bootcamp de desarrollo AI de [Factoría F5](https://factoriaf5.org) · 2026*

*Developed as an educational project for the AI development bootcamp at [Factoría F5](https://factoriaf5.org) · 2026*
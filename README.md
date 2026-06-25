```markdown
# BrandSight 🥤

**Coca-Cola vs Pepsi — Brand Visibility Analysis / Análisis de Visibilidad de Marca**

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](runtime.txt)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32%2B-FF4B4B.svg)](requirements.txt)
[![YOLOv8](https://img.shields.io/badge/YOLO-v8n-00FF00.svg)](models/best.pt)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**🇬🇧** An AI-powered computer vision application that analyzes video content to measure and compare brand visibility between Coca-Cola and Pepsi. Upload a video, and the system detects logo appearances, calculates visibility metrics, and generates an AI marketing report.

**🇪🇸** Una aplicación de visión artificial impulsada por IA que analiza contenido de video para medir y comparar la visibilidad de marca entre Coca-Cola y Pepsi. Sube un video y el sistema detecta apariciones de logotipos, calcula métricas de visibilidad y genera un informe de marketing con IA.

🔗 **Live Demo / Demo en vivo:** [https://brandsight.streamlit.app](https://brandsight.streamlit.app)

---

## 📋 Table of Contents / Índice

- [Problem Statement / Planteamiento del Problema](#problem-statement--planteamiento-del-problema)
- [Features / Funcionalidades](#features--funcionalidades)
- [Architecture / Arquitectura](#architecture--arquitectura)
- [Project Structure / Estructura del Proyecto](#project-structure--estructura-del-proyecto)
- [Setup Instructions / Instrucciones de Configuración](#setup-instructions--instrucciones-de-configuración)
- [Model Training / Entrenamiento del Modelo](#model-training--entrenamiento-del-modelo)
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

En marketing competitivo, entender la visibilidad de marca en contenido de video (anuncios de TV, eventos deportivos, redes sociales) es crucial para medir el ROI de patrocinios y la efectividad de campañas. El análisis manual es lento, subjetivo y no escalable.

**BrandSight** automatiza este proceso mediante:

1. **Detección** de logotipos de Coca-Cola y Pepsi en frames de video usando un modelo YOLOv8 nano fine-tuneado
2. **Cuantificación** de métricas de visibilidad (tiempo en pantalla, número de detecciones, puntuaciones de confianza)
3. **Comparación** de presencia competitiva entre las dos marcas
4. **Generación** de informes de marketing con IA e insights accionables

**Preguntas clave que responde:**
- ¿Qué porcentaje de tiempo en pantalla ocupa cada marca?
- ¿Qué marca domina el video?
- ¿Cuál es la brecha de visibilidad entre competidores?
- ¿Dónde deberían enfocarse los esfuerzos de marketing?

---

## Features / Funcionalidades

### 🇬🇧 English
- 🎥 **Video Upload & Processing** — Upload MP4 videos up to 200MB
- 🔍 **Logo Detection** — YOLOv8 nano fine-tuned on Coca-Cola and Pepsi logos
- 📊 **Visibility Metrics** — Screen time, detection counts, confidence averages
- 📈 **Competitive Analysis** — Dominant brand, visibility gap, balance labels
- 🤖 **AI Marketing Report** — Gemini/OpenAI generated insights with template fallback
- 🖼️ **Detection Gallery** — Bounding box crops of every detected logo
- 🎬 **Annotated Video** — Output video with drawn detections
- 💾 **Supabase Persistence** — All results stored in PostgreSQL
- 🌐 **Bilingual UI** — English / Spanish interface

### 🇪🇸 Español
- 🎥 **Subida y procesamiento de video** — Sube videos MP4 de hasta 200MB
- 🔍 **Detección de logotipos** — YOLOv8 nano fine-tuneado con logotipos de Coca-Cola y Pepsi
- 📊 **Métricas de visibilidad** — Tiempo en pantalla, conteo de detecciones, confianza promedio
- 📈 **Análisis competitivo** — Marca dominante, brecha de visibilidad, etiquetas de balance
- 🤖 **Informe de marketing con IA** — Insights generados por Gemini/OpenAI con plantilla de respaldo
- 🖼️ **Galería de detecciones** — Recortes de cada logotipo detectado
- 🎬 **Video anotado** — Video de salida con detecciones dibujadas
- 💾 **Persistencia en Supabase** — Todos los resultados almacenados en PostgreSQL
- 🌐 **Interfaz bilingüe** — Interfaz en inglés / español

---

## Architecture / Arquitectura

```
┌──────────────────────────────────────────────────────────────┐
│                    USER INTERFACE / INTERFAZ DE USUARIO       │
│              Streamlit (app/streamlit_app.py)                 │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ Video Upload │  │ Brand Metrics│  │ Detection Gallery  │   │
│  │ Demo Select  │  │ Bar Chart    │  │ AI Report (MD)     │   │
│  └─────────────┘  └──────────────┘  └────────────────────┘   │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                    ORCHESTRATOR / ORQUESTADOR                  │
│                src/pipeline.py                                │
│  analyze_video() — coordinates entire analysis flow           │
└──────────────────────────┬───────────────────────────────────┘
                           │
     ┌─────────────────────┼─────────────────────┐
     ▼                     ▼                     ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────────┐
│  DETECTION  │    │   METRICS    │    │   AI REPORT      │
│  DETECCIÓN  │    │   MÉTRICAS   │    │   INFORME IA     │
│             │    │              │    │                  │
│ YOLOv8 nano │    │ Visibility   │    │ Gemini / OpenAI  │
│ detect_video│    │ Competitive  │    │ Jinja2 fallback  │
│ crops.py    │    │ metrics.py   │    │ marketing_report │
└──────┬──────┘    └──────┬───────┘    └────────┬─────────┘
       │                  │                     │
       └──────────────────┼─────────────────────┘
                          │
              ┌───────────▼───────────┐
              │      DATABASE         │
              │   Supabase PostgreSQL │
              │                       │
              │  • videos             │
              │  • detections         │
              │  • brand_summary      │
              │  • competitive_analysis│
              │  • marketing_reports  │
              └───────────────────────┘
```

**Data Flow / Flujo de Datos:**
1. User uploads video → saved to `data/uploads/` / El usuario sube un video → guardado en `data/uploads/`
2. `pipeline.py` orchestrates / orquesta:
   - `detect_video.py` runs YOLO on every Nth frame (stride) / ejecuta YOLO cada N frames
   - `crops.py` extracts bounding box regions / extrae regiones de bounding boxes
   - `metrics.py` calculates visibility percentages / calcula porcentajes de visibilidad
   - `marketing_report.py` generates AI insights / genera insights con IA
3. Results persisted to Supabase PostgreSQL / Resultados guardados en Supabase PostgreSQL
4. UI displays metrics, charts, crops, and report / La UI muestra métricas, gráficos, recortes e informe

---

## Project Structure / Estructura del Proyecto

```
brandsight/
├── .streamlit/                    # Streamlit configuration / Configuración de Streamlit
│   ├── config.toml                # Theme, server settings, upload limits / Tema, servidor, límites
│   └── secrets.toml.example       # Credentials template / Plantilla de credenciales
├── app/                           # Main application / Aplicación principal
│   ├── streamlit_app.py           # UI with tabs, widgets, visualizations / UI con pestañas y widgets
│   └── bootstrap_secrets.py       # Injects secrets into os.environ / Inyecta secretos en os.environ
├── src/                           # Core modules / Módulos principales
│   ├── config.py                  # Pydantic settings (env vars → typed config)
│   ├── pipeline.py                # Main orchestrator / Orquestador principal
│   ├── detect_video.py            # YOLO video processing / Procesamiento de video YOLO
│   ├── detect_image.py            # YOLO single image inference / Inferencia YOLO en imagen
│   ├── crops.py                   # Bbox crop extraction / Extracción de recortes
│   ├── metrics.py                 # Visibility & competitive analysis / Visibilidad y análisis competitivo
│   ├── metrics_export.py          # JSON/TXT export + CLI viewer / Exportación JSON/TXT + visor CLI
│   ├── db/                        # Database layer / Capa de base de datos
│   │   ├── connection.py          # SQLAlchemy engine, sessions, schema checks
│   │   ├── models.py              # ORM models (5 tables) / Modelos ORM (5 tablas)
│   │   └── repository.py          # CRUD operations / Operaciones CRUD
│   └── report/
│       └── generate_marketing_report.py  # AI report generation / Generación de informes IA
├── scripts/                       # Diagnostic & testing tools / Herramientas de diagnóstico
│   ├── check_db.py                # Verify DB connection & schema / Verificar conexión y esquema
│   ├── check_detect_image.py      # Quick model test on image / Prueba rápida del modelo
│   ├── smoke_deploy.py            # Pre-deploy verification / Verificación pre-deploy
│   ├── test_db_insert.py          # DB round-trip test / Prueba de ida y vuelta en BD
│   └── verify_crops.py            # Verify crop files exist / Verificar archivos de recortes
├── notebooks/
│   └── train_colab.ipynb          # YOLO training notebook / Notebook de entrenamiento YOLO
├── sql/
│   ├── schema.sql                 # Database schema (DDL) / Esquema de base de datos
│   └── storage.sql                # Supabase Storage bucket setup / Configuración de bucket
├── data/                          # Generated data (gitignored) / Datos generados (gitignored)
│   ├── crops/                     # Extracted detection crops / Recortes de detecciones
│   ├── uploads/                   # Uploaded videos / Videos subidos
│   ├── outputs/                   # Annotated videos, reports, metrics / Videos anotados, informes
│   └── demo/                      # Demo videos/images / Videos/imágenes de demostración
├── models/
│   └── best.pt                    # Trained YOLOv8 nano weights / Pesos YOLOv8 nano entrenados
├── Dockerfile                     # Docker image definition / Definición de imagen Docker
├── .dockerignore                  # Files excluded from Docker image
├── .gitignore                     # Files excluded from Git
├── .gitattributes                 # Line ending normalization
├── .env.example                   # Environment variables template / Plantilla de variables de entorno
├── requirements.txt               # Python dependencies (pip) / Dependencias Python
├── packages.txt                   # System dependencies (apt-get) / Dependencias del sistema
└── runtime.txt                    # Python version for Streamlit Cloud / Versión de Python
```

---

## Setup Instructions / Instrucciones de Configuración

### Prerequisites / Prerrequisitos

**🇬🇧**
- **Python 3.11** (required)
- **Git**
- **Supabase account** (free tier works)
- **Google Gemini API key** or **OpenAI API key** (optional — for AI reports)
- **Streamlit Cloud account** (for deployment)

**🇪🇸**
- **Python 3.11** (requerido)
- **Git**
- **Cuenta de Supabase** (plan gratuito funciona)
- **API key de Google Gemini** o **API key de OpenAI** (opcional — para informes IA)
- **Cuenta de Streamlit Cloud** (para despliegue)

### Local Development / Desarrollo Local

```bash
# 1. Clone the repository / Clonar el repositorio
git clone https://github.com/your-org/brandsight.git
cd brandsight

# 2. Create virtual environment / Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Install dependencies / Instalar dependencias
pip install -r requirements.txt

# 4. Set up environment variables / Configurar variables de entorno
cp .env.example .env
# Edit .env with your actual values / Editar .env con tus valores reales

# 5. Set up Streamlit secrets / Configurar secretos de Streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit with the same values as .env / Editar con los mismos valores que .env

# 6. Set up Supabase database / Configurar base de datos Supabase
# Go to Supabase SQL Editor / Ir al Editor SQL de Supabase
# Run sql/schema.sql to create tables / Ejecutar sql/schema.sql para crear tablas
# (Optional) Run sql/storage.sql to create storage bucket

# 7. Verify setup / Verificar configuración
python scripts/smoke_deploy.py
```

### Environment Variables / Variables de Entorno

| Variable | Required / Requerida | Description / Descripción | Where to get it / Dónde obtenerla |
|----------|----------------------|---------------------------|-----------------------------------|
| `DATABASE_URL` | ✅ Yes / Sí | Supabase PostgreSQL connection string | Supabase → Settings → Database → URI |
| `SUPABASE_URL` | ❌ No | Supabase project URL | Supabase → Settings → API |
| `SUPABASE_SERVICE_ROLE_KEY` | ❌ No | Service role key for privileged ops | Supabase → Settings → API |
| `GEMINI_API_KEY` | ❌ No | Google Gemini API key | Google AI Studio |
| `OPENAI_API_KEY` | ❌ No | OpenAI API key | OpenAI Platform |
| `MODEL_PATH` | ❌ No | Path to YOLO weights / Ruta a pesos YOLO | Default: `models/best.pt` |
| `CONFIDENCE_THRESHOLD` | ❌ No | Minimum detection confidence / Confianza mínima | Default: `0.5` |
| `SAMPLE_STRIDE` | ❌ No | Process every Nth frame / Procesar cada N frames | Default: `3` |

---

## Model Training / Entrenamiento del Modelo

### Dataset / Conjunto de Datos

**🇬🇧** The model was trained on a custom dataset of Coca-Cola and Pepsi logos using **Roboflow** for dataset management and annotation.

**🇪🇸** El modelo fue entrenado con un dataset personalizado de logotipos de Coca-Cola y Pepsi usando **Roboflow** para la gestión y anotación del dataset.

- **Classes / Clases:** 2 (`coca_cola`, `pepsi`)
- **Source / Fuente:** Brand logos in various contexts / Logotipos de marca en varios contextos (TV commercials, sports events, product placements)
- **Format / Formato:** YOLOv8 (bounding boxes)
- **Split / División:** Train / Validation / Test

### Preprocessing & Augmentations / Preprocesado y Aumentaciones

**🇬🇧** All preprocessing and augmentations were applied during training in the Colab notebook (`notebooks/train_colab.ipynb`).

**🇪🇸** Todo el preprocesado y aumentaciones se aplicaron durante el entrenamiento en el notebook de Colab (`notebooks/train_colab.ipynb`).

**Preprocessing / Preprocesado:**

| Step / Paso | Detail / Detalle |
|-------------|------------------|
| **Resize / Redimensionar** | 640×640 pixels (YOLOv8 standard input size) |
| **Normalization / Normalización** | Pixel values scaled to [0, 1] (automatic via ultralytics) |
| **Format / Formato** | RGB conversion if needed / Conversión a RGB si es necesario |

**Augmentations / Aumentaciones:**

| Augmentation / Aumentación | Parameter / Parámetro | Purpose / Propósito |
|---------------------------|----------------------|---------------------|
| **Horizontal Flip / Volteo horizontal** | p=0.5 | Logos appear both left and right oriented |
| **Rotation / Rotación** | ±10° | Slight rotations for robustness / Rotaciones ligeras |
| **Brightness / Brillo** | ±25% | Different lighting conditions / Diferentes condiciones de luz |
| **Contrast / Contraste** | ±25% | Varying contrast environments / Entornos de contraste variable |
| **Scale / Escala** | ±50% | Logos at different distances / Logos a diferentes distancias |
| **Mosaic / Mosaico** | p=1.0 | Combine 4 images for better context learning |

### Training Process / Proceso de Entrenamiento

**🇬🇧** The model was trained using Google Colab. To retrain:

**🇪🇸** El modelo fue entrenado usando Google Colab. Para re-entrenar:

1. Open `notebooks/train_colab.ipynb` in Google Colab / Abrir en Google Colab
2. Upload your dataset or use Roboflow API key / Subir tu dataset o usar API key de Roboflow
3. Run all cells / Ejecutar todas las celdas
4. Download `best.pt` and place in `models/` folder / Descargar y colocar en `models/`

**Training configuration / Configuración de entrenamiento:**

| Parameter / Parámetro | Value / Valor | Rationale / Justificación |
|----------------------|---------------|--------------------------|
| **Model / Modelo** | YOLOv8 nano (`yolov8n.pt`) | Smallest variant (~6MB), fast inference |
| **Epochs / Épocas** | 50 | Sufficient for transfer learning on 2 classes |
| **Image size / Tamaño imagen** | 640 | Standard YOLOv8 input size |
| **Batch size / Tamaño de lote** | 16 | Fits in Colab T4 GPU memory |
| **Optimizer / Optimizador** | AdamW (default) | Standard for YOLOv8 |

**Why YOLOv8 nano? / ¿Por qué YOLOv8 nano?**

**🇬🇧**
- ~6MB model size fits in Streamlit Cloud memory limits
- Fast inference (~2ms/frame on GPU, ~30ms/frame on CPU)
- Sufficient accuracy for 2-class logo detection (mAP50 > 0.85)
- Transfer learning from COCO provides strong feature extraction

**🇪🇸**
- ~6MB de tamaño cabe en los límites de memoria de Streamlit Cloud
- Inferencia rápida (~2ms/frame en GPU, ~30ms/frame en CPU)
- Precisión suficiente para detección de 2 clases (mAP50 > 0.85)
- Transfer learning desde COCO proporciona extracción de características robusta

### Frame Sampling Assumptions / Suposiciones de Muestreo de Frames

**🇬🇧** Video processing uses **strided sampling** to balance speed and accuracy:

**🇪🇸** El procesamiento de video usa **muestreo por stride** para equilibrar velocidad y precisión:

| Parameter / Parámetro | Default | Meaning / Significado |
|----------------------|---------|----------------------|
| `SAMPLE_STRIDE` | 3 | Process every 3rd frame / Procesar 1 de cada 3 frames |
| `CONFIDENCE_THRESHOLD` | 0.5 | Minimum 50% confidence / Confianza mínima del 50% |

**Frame interval calculation / Cálculo del intervalo de frame:**
```
frame_interval = sample_stride / fps
visible_seconds = unique_frames_with_detection × frame_interval
visibility_pct = (visible_seconds / total_duration) × 100
```

**Assumptions / Suposiciones:**

1. **Linear interpolation / Interpolación lineal:** If a logo is detected at frame N, it's assumed visible for the next `stride - 1` frames. With stride=3 at 30fps, each detection covers 0.1 seconds / Si se detecta un logo en el frame N, se asume visible durante los siguientes `stride - 1` frames. Con stride=3 a 30fps, cada detección cubre 0.1 segundos.

2. **Unique frames / Frames únicos:** Multiple detections in the same frame count as one "visible frame" / Múltiples detecciones en el mismo frame cuentan como un "frame visible".

3. **Detection persistence / Persistencia de detección:** In the annotated video, bounding boxes persist visually between detection frames for smooth visualization / En el video anotado, los bounding boxes persisten visualmente entre frames de detección.

4. **Stride accuracy tradeoff / Compromiso precisión-stride:**
   - `stride=1`: Most accurate / Más preciso, 3× slower / más lento
   - `stride=3`: Good balance / Buen equilibrio, minimal accuracy loss
   - `stride=5`: Faster / Más rápido, may miss brief logo appearances

---

## How to Run Locally / Cómo Ejecutar en Local

```bash
# Activate virtual environment / Activar entorno virtual
source .venv/bin/activate

# Run the Streamlit app / Ejecutar la aplicación Streamlit
streamlit run app/streamlit_app.py

# Or run individual scripts / O ejecutar scripts individuales
python scripts/check_db.py               # Verify database / Verificar base de datos
python scripts/check_detect_image.py      # Test model on image / Probar modelo en imagen
python scripts/smoke_deploy.py            # Pre-deploy checks / Verificación pre-deploy
python scripts/test_db_insert.py          # Test database operations / Probar operaciones BD
python scripts/verify_crops.py --video-id 1  # Verify crop files / Verificar archivos de recortes
```

The app will open at `http://localhost:8501` / La aplicación se abrirá en `http://localhost:8501`.

---

## How to Deploy / Cómo Desplegar

### Streamlit Cloud

**🇬🇧**
1. Push code to GitHub repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app" → Select your repository
4. Configure secrets in App → Settings → Secrets
5. Deploy! Streamlit Cloud reads `runtime.txt`, `packages.txt`, and `requirements.txt` automatically.

**🇪🇸**
1. Sube el código a un repositorio de GitHub
2. Ve a [Streamlit Cloud](https://streamlit.io/cloud)
3. Haz clic en "New app" → Selecciona tu repositorio
4. Configura los secretos en App → Settings → Secrets
5. ¡Desplegar! Streamlit Cloud lee `runtime.txt`, `packages.txt` y `requirements.txt` automáticamente.

**Secrets format / Formato de secretos:**
```toml
DATABASE_URL = "postgresql://..."
GEMINI_API_KEY = "your_key"
MODEL_PATH = "models/best.pt"
CONFIDENCE_THRESHOLD = "0.5"
SAMPLE_STRIDE = "3"
```

### Docker

```bash
# Build image / Construir imagen
docker build -t brandsight .

# Run container / Ejecutar contenedor
docker run -p 8501:8501 \
  -e DATABASE_URL="postgresql://..." \
  -e GEMINI_API_KEY="your_key" \
  brandsight
```

---

## Verification Scripts / Scripts de Verificación

**🇬🇧** The project includes several CLI tools for diagnostics and testing:

**🇪🇸** El proyecto incluye varias herramientas CLI para diagnóstico y testing:

| Script | Purpose / Propósito | Usage / Uso |
|--------|--------------------|-------------|
| `check_db.py` | Verify Supabase connection & schema / Verificar conexión y esquema | `python scripts/check_db.py` |
| `check_detect_image.py` | Quick YOLO test on demo image / Prueba rápida en imagen demo | `python scripts/check_detect_image.py` |
| `smoke_deploy.py` | Full pre-deploy verification / Verificación completa pre-deploy | `python scripts/smoke_deploy.py` |
| `test_db_insert.py` | Round-trip DB insert/read/delete test / Prueba CRUD completa | `python -m scripts.test_db_insert` |
| `verify_crops.py` | Check crop files exist on disk / Verificar recortes en disco | `python scripts/verify_crops.py --video-id 1` |

**Run all checks before deploying / Ejecutar todas las verificaciones antes de desplegar:**
```bash
python scripts/smoke_deploy.py && python -m scripts.test_db_insert
```

---

## Evaluation Criteria / Criterios de Evaluación

### Dataset / Conjunto de Datos

**🇬🇧**
- **Custom dataset** created and managed in Roboflow
- 2 classes: `coca_cola` and `pepsi`
- Images sourced from TV commercials, sports broadcasts, and product placement footage
- Annotated with bounding boxes in YOLOv8 format

**🇪🇸**
- **Dataset personalizado** creado y gestionado en Roboflow
- 2 clases: `coca_cola` y `pepsi`
- Imágenes obtenidas de anuncios de TV, transmisiones deportivas y colocación de producto
- Anotado con bounding boxes en formato YOLOv8

### Preprocessing / Preprocesado

**🇬🇧**
- Images resized to 640×640 pixels
- Automatic normalization by ultralytics framework
- No manual cropping or filtering applied

**🇪🇸**
- Imágenes redimensionadas a 640×640 píxeles
- Normalización automática mediante el framework ultralytics
- Sin recorte ni filtrado manual aplicado

### Fine-tuning

**🇬🇧**
- Transfer learning from YOLOv8 nano pretrained on COCO
- 50 epochs with standard hyperparameters
- Model achieves mAP50 > 0.85 on validation set

**🇪🇸**
- Transfer learning desde YOLOv8 nano pre-entrenado en COCO
- 50 épocas con hiperparámetros estándar
- El modelo alcanza mAP50 > 0.85 en el conjunto de validación

### Augmentations / Aumentaciones

**🇬🇧**
- Horizontal flip (p=0.5)
- Rotation (±10°)
- Brightness & contrast variations (±25%)
- Scale jittering (±50%)
- Mosaic augmentation (p=1.0)

**🇪🇸**
- Volteo horizontal (p=0.5)
- Rotación (±10°)
- Variaciones de brillo y contraste (±25%)
- Jittering de escala (±50%)
- Aumentación de mosaico (p=1.0)

### Frame Sampling / Muestreo de Frames

**🇬🇧**
- Stride-based sampling (default: 3)
- Visibility calculated from unique detected frames
- Configurable via `SAMPLE_STRIDE` environment variable

**🇪🇸**
- Muestreo por stride (por defecto: 3)
- Visibilidad calculada a partir de frames únicos detectados
- Configurable mediante la variable de entorno `SAMPLE_STRIDE`

---

## Team Roles / Roles del Equipo

| Role / Rol | Name / Nombre | Responsibilities / Responsabilidades |
|------------|---------------|--------------------------------------|
| **Scrum Master** | [Mirae Kang] | Sprint planning, daily standups, retrospectives, removing blockers / Planificación de sprints, daily standups, retrospectivas, eliminación de impedimentos |
| **Product Owner (PO)** | [Mar Izquierdo Vaquer] | Requirements, user stories, acceptance criteria, README, documentation, stakeholder communication / Requisitos, historias de usuario, criterios de aceptación, README, documentación, comunicación con stakeholders |
| **ML Engineer** | [Juan Manuel Iriondo Ortega] | YOLO model training, dataset preparation (Roboflow), preprocessing & augmentations, model evaluation, pipeline integration, frame sampling implementation / Entrenamiento del modelo YOLO, preparación del dataset (Roboflow), preprocesado y aumentaciones, evaluación del modelo, integración del pipeline, implementación del muestreo de frames |

---

## Acknowledgements / Agradecimientos

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) — Object detection framework
- [Streamlit](https://streamlit.io) — Web application framework
- [Supabase](https://supabase.com) — Database and storage
- [Roboflow](https://roboflow.com) — Dataset management
- [Google Gemini](https://ai.google.dev) — AI report generation
- [OpenAI](https://openai.com) — Alternative AI provider


*Desarrollado como recurso educativo para la presentación de la Arquitectura RAG — 2026*
```
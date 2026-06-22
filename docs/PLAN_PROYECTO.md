# Plan del Proyecto — BrandSight (Coca-Cola vs Pepsi)

Aplicación web de análisis de visibilidad de marca: detectar logos en vídeo, comparar tiempo en pantalla, persistir resultados en **base de datos en la nube** y generar un informe de marketing con IA para el cliente Coca-Cola.

**Restricciones:** 6 días · 3 compañeros · Linux / Mac / Windows · entrenamiento en **Google Colab** · aplicación **desplegada**

Documentos relacionados: [BRIEFING_README.md](./BRIEFING_README.md) · [PROJECT_PLAN.md](./PROJECT_PLAN.md) (English) · [KANBAN.md](./KANBAN.md)

---

## Resumen del proyecto

| Elemento | Detalle |
|----------|---------|
| **Nombre** | BrandSight (título provisional) |
| **Cliente** | Coca-Cola |
| **Competidor** | Pepsi |
| **Objetivo** | Medir y comparar la visibilidad de marca en contenido de vídeo |
| **Stack principal** | YOLOv8 · OpenCV · **Supabase** (PostgreSQL) · Streamlit · API LLM · Deploy cloud |

### Pipeline

```
Subir vídeo → YOLO detecta Coca-Cola y Pepsi (frame a frame)
    → Calcular métricas de visibilidad → Guardar en Supabase (+ recortes)
    → LLM genera informe de marketing para Coca-Cola → Mostrar en la web app
```

---

## Objetivo principal

Construir un **analizador de visibilidad de marca** (prueba de concepto) que:

1. Detecte los logos de **Coca-Cola** y **Pepsi** en vídeos subidos mediante un modelo YOLO fine-tuned
2. Calcule tiempo en pantalla, porcentajes, número de detecciones y dominancia competitiva por marca
3. Persista todos los datos en **Supabase** (PostgreSQL gestionado en la nube)
4. Genere un **informe de marketing con IA** a partir de las métricas almacenadas (perspectiva analista de Coca-Cola)
5. Entregue todo mediante una **aplicación web Streamlit desplegada**

**Criterio de éxito en demo:** subir un vídeo de 30–60 s → vídeo anotado → dashboard de métricas → comparativa competitiva → informe IA — todo en la **URL desplegada en vivo**; más un **segmento con webcam local** durante la presentación (`detect_webcam.py`).

---

## Alineación con el briefing

| Requisito del briefing | BrandSight |
|------------------------|------------|
| Detección de logos en vídeo | ✅ YOLO — Coca-Cola + Pepsi |
| Detección en tiempo real (evaluación) | ✅ `detect_webcam.py` — **local**, no en deploy |
| Tiempo en pantalla + porcentaje | ✅ Segundos y % por marca |
| Guardar detecciones en BD | ✅ Supabase (PostgreSQL) |
| Modelo multimarca (Avanzado) | ✅ 2 clases |
| % de confianza (Avanzado) | ✅ En overlay + en BD |
| Recortes bbox (Avanzado) | ✅ Guardados; ruta en BD |
| Front web (Experto) | ✅ Streamlit — desplegado |
| Cloud / API (Experto) | ✅ App desplegada; API opcional si sobra tiempo |

---

## Objetivo realista en 6 días

| Nivel | Veredicto |
|-------|-----------|
| Esencial | **Obligatorio** (Día 1–2) |
| Medio | **Obligatorio** (Día 2–3) |
| Avanzado | **Obligatorio** (Día 3–4) |
| Experto | **Objetivo** — web app desplegada; omitir microservicio API salvo tiempo libre |

**No perseguir:** precisión perfecta, 10+ marcas, frontend React custom, colas Celery.

---

## Roles del equipo (3 personas, doble rol)

Todos programan. PO y SM son **roles parciales**.

| Persona | Principal | Secundario | Entregables |
|---------|-----------|------------|-------------|
| **A — Product Owner** | Alcance, guion demo, presentación, prompt del informe IA | Frontend / deploy | UI Streamlit, prompt marketing, slides, criterios de aceptación |
| **B — Scrum Master** | Daily, Kanban, Git/PR, despliegue y entorno | Backend / pipeline | `detect_video.py`, `report.py`, capa BD, Docker, config deploy |
| **C — ML Engineer** | Dataset, entrenamiento Colab, calidad del modelo | Inferencia | Roboflow, `train_colab.ipynb`, `detect_image.py`, `detect_webcam.py`, `models/best.pt` |

**Rotar SM** si B está bloqueado en ML.

**Ceremonias:** daily 15 min · PO protege el alcance · SM mergea PRs el mismo día

**Nota de carga:** el ML Engineer es el camino crítico (etiquetado + entrenamiento). PO y SM deben ayudar a etiquetar desde el Día 1.

---

## Estrategia multi-OS

| Problema | Solución |
|----------|----------|
| GPU / CUDA distintas | Entrenar **solo en Google Colab** |
| Dependencias Python | Un `requirements.txt`, Python 3.10–3.11 |
| Rutas | `pathlib.Path` en todo el código |
| Finales de línea | `.gitattributes` → `* text=auto` |
| Pesos del modelo | Google Drive del equipo — no en Git |
| BD local vs cloud | **Mismo proyecto Supabase** vía `DATABASE_URL`; `.env` local, secrets en plataforma de deploy |

**Artefactos compartidos (fuera de Git):**
```
Team Drive/
├── datasets/           # export YOLO de Roboflow
├── models/best.pt
└── demo_videos/        # 2–3 clips (ambas marcas visibles)
```

---

## Arquitectura técnica

```
┌─────────────────────────────────────────────────────────────┐
│  Web App Streamlit (desplegada — Streamlit Cloud / Railway) │
│  Subida · Métricas · Gráficos · Informe IA                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  Pipeline de análisis (Python)                              │
│  OpenCV → YOLO (coca_cola, pepsi) → Métricas → Recortes     │
└──────────────┬─────────────────────────┬────────────────────┘
               │                         │
┌──────────────▼──────────┐   ┌──────────▼────────────────────┐
│  Supabase PostgreSQL    │   │  Supabase Storage (opcional)  │
│  videos · detections    │   │  bucket: brandsight-crops     │
│  summaries · reports    │   │  vídeos · crops · informes    │
└─────────────────────────┘   └─────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│  API LLM (Gemini / OpenAI) — generación del informe marketing │
└─────────────────────────────────────────────────────────────┘

Entrenamiento (offline): Roboflow → Google Colab → best.pt → Drive → bundle deploy
```

### Stack tecnológico

| Capa | Elección |
|------|----------|
| Detección | Ultralytics YOLOv8 (`yolov8n` o `yolov8s`) |
| Entrenamiento | Google Colab + Roboflow |
| Vídeo | OpenCV |
| Base de datos | **Supabase** (PostgreSQL — tier gratis) |
| ORM | SQLAlchemy |
| Migraciones | Alembic (opcional) o script SQL inicial |
| UI web | Streamlit |
| Informe IA | API Gemini u OpenAI (una llamada por análisis) |
| Deploy | **Streamlit Community Cloud** o **Railway** |
| Secretos | Variables de entorno en plataforma + `.env` local (nunca commitear) |
| Contenedor | Dockerfile (Railway / reproducibilidad) |

---

## Configuración Supabase (Día 1 — SM)

1. Crear proyecto en [supabase.com](https://supabase.com/) (tier gratis)
2. **SQL Editor** → ejecutar `sql/schema.sql` del repo
3. **Project Settings → Database** → copiar **Connection string** (modo URI)
4. Usar el string del **Session pooler** para Streamlit / apps servidor
5. Compartir `DATABASE_URL` con el equipo por canal seguro (no Git)
6. *(Opcional)* **Storage** → crear bucket `brandsight-crops` (público o URLs firmadas)

**Formato connection string:**
```
postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres
```

**SQLAlchemy** (si hace falta):
```
postgresql+psycopg2://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres
```

**Verificar:** Table Editor debe mostrar `videos`, `detections`, `brand_summary`, `competitive_analysis`, `marketing_reports`.

---

## Esquema de base de datos (Supabase / PostgreSQL)

Archivo SQL: [`sql/schema.sql`](../sql/schema.sql)

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

### Cálculo de visibilidad

```
frame_interval = 1 / fps   (× sample_stride si se saltan frames)

Por frame muestreado:
  si coca_cola detectada (conf ≥ 0.5) → coca_frames += 1
  si pepsi detectada     (conf ≥ 0.5) → pepsi_frames += 1

visible_seconds = frames × frame_interval × sample_stride
visibility_pct  = (visible_seconds / duration_sec) × 100

dominant_brand  = marca con más visible_seconds
balance_label   = 'balanced' si gap < 5% duración, si no '{ganador}_dominant'
```

---

## Generación del informe con IA

**Entrada:** JSON de `brand_summary` + `competitive_analysis` (no el vídeo en bruto).

**Prompt de sistema:**
> Eres un analista de visibilidad de marca trabajando para Coca-Cola. Redacta un informe de marketing conciso usando solo las métricas proporcionadas. Sé profesional y basado en datos. No inventes cifras.

**Secciones del informe:**
1. Resumen ejecutivo
2. Visibilidad de Coca-Cola
3. Visibilidad competitiva de Pepsi
4. Comparativa competitiva
5. Insights de marketing (2–3 viñetas)
6. Recomendación para Coca-Cola

**Plan B:** plantilla Jinja2 si la API LLM no está disponible en la demo.

**Módulo:** `src/report/generate_marketing_report.py` → guarda en tabla `marketing_reports`.

---

## Funcionalidades de la web app (Streamlit)

| Sección | Funcionalidades |
|---------|-----------------|
| Subida | Uploader MP4 + selector de vídeo demo |
| Procesado | Barra de progreso, estado desde BD |
| Resultados vídeo | Reproductor del vídeo anotado |
| Métricas | Duración, segundos/%, detecciones por marca |
| Comparativa | Gráfico de barras, badge de marca dominante |
| Detecciones | Tabla + miniaturas de recortes |
| Informe IA | Markdown renderizado + copiar/descargar |
| Historial | Análisis anteriores desde Supabase |

**Nota:** la detección con webcam en tiempo real va en **`src/detect_webcam.py` (local)** — no en la app Streamlit desplegada. Se usa en el segmento en vivo de la presentación.

---

## Decisiones de alcance

| Decisión | Elección |
|----------|----------|
| Marcas | Solo Coca-Cola + Pepsi |
| Imágenes por marca | 80–120 anotadas |
| Vídeo demo | 30–60 segundos |
| Webcam tiempo real | **`detect_webcam.py` — solo local** (OpenCV + YOLO); no en producción |
| Muestreo de frames | Cada 3.er–5.o frame (documentar en README) |
| Base de datos | **Supabase** (PostgreSQL) |
| Archivos | Bucket Supabase Storage o directorio temporal + rutas en BD |
| Frontend | Solo Streamlit |
| Deploy | Streamlit Cloud o Railway |
| LLM | Gemini tier gratis u OpenAI |

---

## Plan de sprint — 6 días

### Día 1 — Setup, datos, infra cloud, primer entrenamiento

| Quién | Tareas |
|-------|--------|
| PO | Cerrar alcance Coca-Cola/Pepsi, user stories, tablero GitHub Project |
| SM | Esqueleto repo, ramas, `requirements.txt`, `.gitignore`, `.env.example` |
| SM | **Crear proyecto Supabase**, ejecutar `sql/schema.sql`, compartir `DATABASE_URL` |
| ML | Proyecto Roboflow, ~50 img/marca, empezar etiquetado |
| Todos | Planning 30 min: definición de hecho |

**Fin de día:** Supabase operativa · 50+ imágenes etiquetadas · smoke train Colab (10 epochs)

---

### Día 2 — Esencial COMPLETADO

| Quién | Tareas |
|-------|--------|
| ML | Terminar etiquetado, entrenamiento Colab completo, `best.pt` → Drive |
| Backend | `detect_image.py`, módulo conexión BD, test insert en los 3 OS |
| ML | Empezar `detect_webcam.py` si `best.pt` disponible |
| PO | README: setup, variables de entorno, cómo ejecutar |

**Fin de día:** Detección en imagen con bbox + marca · conexión BD funciona en local

---

### Día 3 — Medio COMPLETADO

| Quién | Tareas |
|-------|--------|
| Backend | `detect_video.py` — MP4 anotado, etiquetas + confianza en overlay |
| ML | Terminar `detect_webcam.py`; reentrenar si hace falta; añadir frames difíciles de los vídeos demo |
| PO/SM | Grabar 2 vídeos demo (ambas marcas); actualizar Kanban |

**Fin de día:** Demo vídeo 30 s anotado · webcam local funcional · datos escritos en Supabase

---

### Día 4 — Avanzado COMPLETADO

| Quién | Tareas |
|-------|--------|
| Backend | `report.py` — métricas visibilidad, `brand_summary`, `competitive_analysis` |
| Backend | Guardar recortes bbox, rutas en `detections` |
| ML | Entrenamiento final 2 clases en Colab si métricas flojas |
| Backend | `generate_marketing_report.py` — llamada LLM + insert en BD |

**Fin de día:** Métricas completas + análisis competitivo + informe IA en BD

---

### Día 5 — Web app + despliegue

| Quién | Tareas |
|-------|--------|
| PO | UI Streamlit: subir → pipeline → métricas + gráfico + informe IA |
| SM | `Dockerfile`, deploy en **Streamlit Cloud o Railway** |
| SM | Configurar secrets: `DATABASE_URL`, `GEMINI_API_KEY` / `OPENAI_API_KEY` |
| ML | Verificación final del modelo en app desplegada |
| Todos | Ensayo en **URL en vivo** (15 min) |

**Fin de día:** URL pública/desplegada funcionando de punta a punta

---

### Día 6 — Buffer + entrega

| Quién | Tareas |
|-------|--------|
| Todos | Corregir bugs de deploy, cross-OS, codec vídeo en Windows |
| PO | Presentación: problema → arquitectura → demo en URL en vivo → limitaciones |
| SM | Kanban cerrado, tag `v1.0-demo`, sección deploy en README |
| Todos | Ensayo final |

**Fin de día:** Demo en vivo + presentación listas

---

## Tarjetas Kanban

Tablero completo con incidencias, descripciones y responsables: **[KANBAN.md](./KANBAN.md)**

```
Backlog → Por hacer → En progreso → En revisión → Hecho
```

1. Dataset Roboflow (Coca-Cola + Pepsi) — **C**
2. Schema Supabase + capa de conexión — **B**
3. Notebook entrenamiento Colab — **C**
4. Detección en imagen — **C**
5. Detección con webcam local — **C**
6. Detección en vídeo + etiquetas + confianza — **B**
7. Métricas visibilidad + análisis competitivo — **B**
8. Recortes bbox + persistencia BD — **B**
9. Generador informe marketing IA — **A**
10. Web app Streamlit — **A**
11. **Despliegue en cloud** — **B**
12. README + presentación — **A**

---

## Registro de riesgos

| Riesgo | Mitigación |
|--------|------------|
| Etiquetado lento | Los 3 etiquetan; solo 2 marcas; auto-label Roboflow + corrección |
| Colab se desconecta | Checkpoints en Drive cada 10 epochs |
| Fallo conexión BD en deploy | Probar `DATABASE_URL` desde plataforma el Día 1 |
| Límites tier gratis Supabase | Vídeos demo cortos; muestreo de frames |
| API LLM caída en demo | Plantilla Jinja2 de respaldo |
| Modelo flojo en vídeo | Fine-tune con frames de vídeos demo |
| Problemas codec Windows | MP4 H.264; probar Día 3 |
| Deploy falla Día 5 | Empezar config deploy Día 1 (app vacía + ping BD) |

---

## Estructura del repo

```
ai-computer-vision-objects/
├── app/
│   └── streamlit_app.py
├── data/
│   └── demo/
├── docs/
│   ├── BRIEFING_README.md
│   ├── PROJECT_PLAN.md
│   └── PLAN_PROYECTO.md
├── models/                   # best.pt (gitignored)
├── notebooks/
│   └── train_colab.ipynb
├── src/
│   ├── db/
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── repository.py
│   ├── detect_image.py
│   ├── detect_webcam.py      # realtime local webcam — not deployed
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

## Variables de entorno

```bash
# .env.example — nunca commitear valores reales
# Supabase → Project Settings → Database → Connection string (URI)
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres

# Opcional — Supabase Storage para crops/vídeos
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_SERVICE_ROLE_KEY=tu_service_role_key

GEMINI_API_KEY=tu_clave_aqui          # o OPENAI_API_KEY
MODEL_PATH=models/best.pt
CONFIDENCE_THRESHOLD=0.5
SAMPLE_STRIDE=3
```

---

## Descripción para la presentación (lista para copiar)

**Pitch corto:**

> **BrandSight** analiza contenido de vídeo para medir la visibilidad de **Coca-Cola** frente a su competidor **Pepsi**. Un modelo YOLO personalizado detecta ambos logos frame a frame, calcula el tiempo en pantalla y la dominancia competitiva, guarda cada resultado en **Supabase** y genera un informe de marketing con IA — todo desde una **aplicación web desplegada**.

**Estructura de slides:**
1. Problema — el cliente necesita métricas de visibilidad vs competencia
2. Solución — pipeline BrandSight
3. Arquitectura — YOLO + Supabase + Streamlit + LLM
4. Demo — recorrido por URL en vivo
5. Stack y entrenamiento (Colab, augmentations)
6. Limitaciones y trabajo futuro (más marcas, webcam en cloud, API REST)

---

## Referencias

- [Roadmap del bootcamp](https://roadmap-mad-ai-p4.coderf5.es/)
- [Documentación Ultralytics YOLO](https://docs.ultralytics.com/)
- [Supabase](https://supabase.com/) · [SQL Editor Supabase](https://supabase.com/docs/guides/database/overview)
- [Deploy Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)

# Plan del Proyecto — Detección de Logos en Vídeo

Plan realista para **6 días**, **3 compañeros**, entornos **Linux / Mac / Windows**, con entrenamiento en **Google Colab**.

Documentos relacionados: [BRIEFING_README.md](./BRIEFING_README.md) · [PROJECT_PLAN.md](./PROJECT_PLAN.md) (stack en inglés)

---

## Objetivo realista (definir el Día 1)

Con 6 días y 3 personas, el objetivo alcanzable es **Nivel Medio + la mayor parte del Avanzado**, no el Experto completo (API en cloud + despliegue productivo).

| Nivel | Veredicto en 6 días |
|-------|---------------------|
| Esencial | **Obligatorio** (Día 1–2) |
| Medio | **Obligatorio** (Día 2–3) |
| Avanzado | **Objetivo** — 2 marcas, confianza %, SQLite, recortes, tiempo en pantalla |
| Experto | **Parcial** — UI con Streamlit; omitir API cloud salvo que sobre tiempo el Día 5 |

**No perseguir:** FastAPI + Celery + despliegue cloud + precisión perfecta multimarca. Una demo que funcione vale más que un stack “experto” a medias.

---

## Roles del equipo (3 personas, doble rol)

Todos programan. PO y Scrum Master son **roles parciales**, no personas que dejan de codear.

| Persona | Rol principal | Rol secundario | Entregables |
|---------|---------------|----------------|-------------|
| **A — Product Owner** | Alcance, prioridades, guion de demo, historia para la presentación | Frontend | `app/streamlit_app.py`, esquema de slides, criterios de aceptación |
| **B — Scrum Master** | Daily, Kanban, bloqueos, flujo Git/PR | Backend / pipeline | `detect_video.py`, `report.py`, SQLite, Docker, README |
| **C — ML Engineer** | Dataset, entrenamiento Colab, calidad del modelo | Scripts de inferencia | Roboflow, `notebooks/train_colab.ipynb`, `detect_image.py`, `models/best.pt` |

**Rotar el rol de SM** si B está bloqueado en ML — quien tenga menos carga ese día facilita el daily de 15 min.

**Ceremonias (ligeras):**
- **Daily:** 15 min — ayer / hoy / bloqueos
- **PO:** mantiene el backlog ordenado; dice “no” al scope creep
- **SM:** mueve tarjetas en Kanban; PRs mergeados el mismo día

---

## Estrategia multi-OS (Linux / Mac / Windows)

**Regla:** entrenar en **un solo sitio** (Colab), inferencia en **un entorno portable** (Python + archivos compartidos).

| Problema | Solución |
|----------|----------|
| GPUs / CUDA distintas | **Entrenar solo en Google Colab** — sin configurar GPU local |
| Dependencias Python | Un solo `requirements.txt`, Python **3.10 o 3.11** para todos |
| Separadores de ruta | Usar `pathlib.Path` en todo el código |
| Finales de línea | `.gitattributes` con `* text=auto` |
| Pesos del modelo demasiado grandes para Git | **Carpeta compartida en Google Drive** o Git LFS |
| “En mi máquina funciona” | **Docker** opcional para inferencia (Día 5); no necesario para entrenar |

**Artefactos compartidos (fuera de Git):**
```
Team Drive/
├── datasets/          # zip exportado de Roboflow
├── models/best.pt     # tras cada entrenamiento en Colab
└── demo_videos/       # 2–3 clips cortos de prueba
```

**Setup local (mismos comandos en todos los OS):**
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.detect_video --video data/demo/sample.mp4 --weights models/best.pt
```

---

## Flujo con Google Colab (recomendado)

Colab encaja bien en un sprint de 6 días.

```
Roboflow (etiquetar) → exportar zip YOLO
        ↓
Notebook Colab (entrenar) → best.pt → Google Drive del equipo
        ↓
Todos descargan best.pt → models/
        ↓
Inferencia local / Streamlit (CPU vale para clips de demo)
```

**Checklist del notebook Colab:**
1. Instalar `ultralytics`
2. Descargar dataset (API key de Roboflow en secretos de Colab — **no** en el repo)
3. Entrenar desde `yolov8n.pt` (rápido) o `yolov8s.pt` si los logos son pequeños
4. Activar augmentations: flip, mosaic, HSV (incluidas en YOLO — mencionarlas en la presentación)
5. Guardar `best.pt` en Drive
6. Validación rápida con 2–3 imágenes de test en el notebook

**Importante:** subir el notebook a Git; **no** commitear datasets ni pesos.

---

## Decisiones de alcance (ahorran días)

| Decisión | Recomendación |
|----------|---------------|
| Número de marcas | **2** (no 4+) — p. ej. Nike + Coca-Cola |
| Imágenes por marca | **80–150** anotadas (Roboflow + augment → ~300+) |
| Duración vídeo demo | **30–60 segundos** por clip |
| Procesado de frames | Cada **3.er–5.o** frame por velocidad; documentar la suposición |
| Base de datos | **SQLite** (un archivo, funciona en todos los OS) |
| Frontend | **Solo Streamlit** (no React) |
| API cloud | **Omitir** o versión “lite”: Streamlit Community Cloud (gratis) |
| Docker | `Dockerfile` simple para inferencia si hay tiempo el Día 5 |

---

## Plan de 6 días (día a día)

### Día 1 — Setup + datos + primer entrenamiento
**Objetivo:** Esencial iniciado; Kanban activo; esqueleto del repo.

| Quién | Tareas |
|-------|--------|
| PO | Elegir 2 marcas, escribir user stories, crear GitHub Project / Trello |
| SM | Estructura repo, ramas (`main`, `develop`), `requirements.txt`, `.gitignore`, `.gitattributes` |
| ML | Proyecto Roboflow, recopilar ~50 img/marca, empezar etiquetado |
| Todos | Planning 30 min: definición de “hecho” por nivel |

**Fin de día:** 50+ imágenes etiquetadas, notebook Colab con entrenamiento smoke de 10 epochs.

---

### Día 2 — Esencial COMPLETADO
**Objetivo:** Una imagen → bounding box + nombre de marca.

| Quién | Tareas |
|-------|--------|
| ML | Terminar etiquetado, entrenamiento completo en Colab, exportar `best.pt` a Drive |
| Backend | `detect_image.py`, descargar pesos, probar en 3 OS |
| PO | README: setup, cómo ejecutar, descripción del dataset |

**Fin de día:** Demo con **una imagen** desde el portátil de cualquier compañero.

---

### Día 3 — Medio COMPLETADO
**Objetivo:** Vídeo → vídeo anotado + etiqueta bajo cada detección.

| Quién | Tareas |
|-------|--------|
| Backend | `detect_video.py` (OpenCV + Ultralytics), guardar MP4 de salida |
| ML | Reentrenar si el mAP del Día 2 es malo; añadir frames difíciles del vídeo |
| PO/SM | Grabar 2 vídeos demo; actualizar Kanban |

**Fin de día:** Vídeo de 30 s con cajas + nombres de clase visibles.

---

### Día 4 — Avanzado (núcleo)
**Objetivo:** Tiempo en pantalla + confianza + base de datos.

| Quién | Tareas |
|-------|--------|
| Backend | `report.py`: segundos + % por marca; esquema SQLite + inserts |
| ML | Dataset multiclase (2 marcas), reentrenar en Colab |
| Backend | Guardar recortes en `data/crops/` + rutas en BD |
| Todos | Mostrar % de confianza en el overlay del vídeo |

**Fin de día:** Informe JSON/texto + fichero SQLite + carpeta de crops.

---

### Día 5 — Pulido Avanzado + Experto-lite
**Objetivo:** Streamlit + borrador de presentación.

| Quién | Tareas |
|-------|--------|
| PO / Frontend | Streamlit: subir vídeo → ejecutar pipeline → mostrar informe + tabla |
| SM | Dockerfile (opcional), README limpio, merge a `main` |
| ML | Pasada final del modelo; 3 slides sobre entrenamiento / augmentations |
| Todos | Ensayo de demo (15 min) |

**Fin de día:** Streamlit funciona en local; opcional despliegue en Streamlit Cloud.

---

### Día 6 — Buffer + entrega
**Objetivo:** Nada nuevo — corregir, ensayar, documentar.

- Corregir bugs por OS (rutas, codec de vídeo)
- Presentación: problema → dataset → fine-tune YOLO → pipeline → demo → limitaciones
- Kanban: todas las tarjetas en Hecho o No se hará (con motivo)
- Tag de release `v1.0-demo`

---

## Columnas Kanban (simple)

```
Backlog → Por hacer → En progreso → En revisión → Hecho
```

**Tarjetas mínimas:**
1. Dataset + Roboflow
2. Notebook entrenamiento Colab
3. Detección en imagen
4. Detección en vídeo + etiquetas
5. Informe tiempo / %
6. SQLite + recortes
7. UI Streamlit
8. README + presentación

---

## Registro de riesgos

| Riesgo | Mitigación |
|--------|------------|
| Etiquetado lento | 2 marcas; auto-label Roboflow + corrección manual |
| Colab se desconecta | Guardar checkpoints en Drive cada 10 epochs |
| Modelo malo en vídeo | Fine-tune con frames extraídos de los vídeos demo |
| Problemas codec en Windows | Usar `.mp4` H.264; probar en Windows el Día 3 |
| Compañero bloqueado en setup | Pairing 30 min con SM; Colab elimina dolor de GPU |
| Scope creep hacia Experto | PO congela backlog tras el almuerzo del Día 3 |

---

## Qué decir en la presentación (criterios de evaluación)

Mencionar explícitamente:
- **Preprocesado:** resize/normalize YOLO (640px), muestreo de frames
- **Dataset propio:** Roboflow, formato YOLO, split train/val
- **Preentrenado + fine-tune:** `yolov8n.pt` → vuestros logos
- **Augmentations:** flip, mosaic, HSV en config de entrenamiento
- **“Tiempo real”:** opcional — mostrar FPS en portátil o aclarar “análisis por lotes, no streaming en vivo”
- **BD:** esquema SQLite + recortes guardados

---

## Stack tecnológico recomendado

### Principio central

Usar **un solo framework de detección de punta a punta** (entrenar → inferir en imagen/vídeo → exportar métricas) en lugar de mezclar TensorFlow + PyTorch + Detectron2.

### Modelo — YOLO vía Ultralytics (PyTorch)

| Opción | Veredicto |
|--------|-----------|
| **YOLOv8 / YOLO11 (Ultralytics)** | **Mejor opción por defecto** — rápido de entrenar, buena documentación, multiclase, scores de confianza, inferencia en vídeo integrada |
| Faster R-CNN / Detectron2 | Buena precisión, setup pesado; excesivo para PoC de logos |
| SSD | Término medio; menos ecosistema que YOLO hoy |
| TensorFlow/Keras | Vale si el equipo ya lo domina; si no, añade fricción |

```
Preentrenado: yolov8n.pt (demo rápida) o yolov8s.pt (mejor precisión)
Fine-tune sobre dataset de logos (formato YOLO)
```

### Librerías

| Capa | Elección | Rol |
|------|----------|-----|
| **Python 3.10+** | Lenguaje principal | Entrenamiento, pipeline, API, UI |
| **Ultralytics** | Entrenamiento + inferencia | Ciclo de vida del modelo |
| **OpenCV** | I/O vídeo, frames, overlay | Pipeline de vídeo |
| **Pillow** | Recortes para BD | Guardar crops de bounding boxes |
| **Albumentations** (opc.) | Augmentations extra | flip, color jitter, crop |
| **pandas** | Agregaciones | Tiempo por marca, % del vídeo |

### Dataset y anotación

| Herramienta | Uso |
|-------------|-----|
| **Roboflow** (tier gratis) | Anotar cajas, exportar YOLO, augmentations |
| **Label Studio** / **CVAT** | Alternativa self-hosted |
| **Recolección manual** | Capturas de anuncios, deportes, YouTube (cuidado con licencias) |

**Formato:** labels YOLO txt (`class x_center y_center width height` normalizado).

### Pipeline de análisis de vídeo

```
Vídeo → OpenCV lee frames → YOLO predict (umbral conf) →
presencia por frame → agregar tiempo por marca → informe + insert BD
```

### Base de datos — SQLite → PostgreSQL

| Tabla | Campos (ejemplo) |
|-------|------------------|
| `videos` | id, filename, duration_sec, processed_at |
| `detections` | id, video_id, brand, confidence, timestamp_sec, bbox, crop_path |
| `video_summary` | video_id, brand, total_seconds, percentage |

| Nivel | BD |
|-------|-----|
| PoC / local | **SQLite** + SQLAlchemy |
| Experto / cloud | **PostgreSQL** (misma ORM, migración fácil) |

### Frontend y API (nivel Experto)

| Capa | Elección |
|------|----------|
| UI demo | **Streamlit** |
| API (si hay tiempo) | **FastAPI** |
| Contenedor | **Docker** (CUDA opcional; CPU vale para demo) |
| Cloud | Streamlit Cloud, Railway, Render, Hugging Face Spaces |

### Stack resumido del equipo

```
Python 3.11
Ultralytics YOLOv8
OpenCV + Pillow
Roboflow (anotación)
SQLite + SQLAlchemy
Streamlit (UI)
Docker
GitHub Projects (Kanban)
Google Colab (entrenamiento GPU)
```

### Estructura sugerida del repo

```
ai-computer-vision-objects/
├── data/
│   ├── raw/
│   ├── datasets/
│   └── crops/
├── models/
├── src/
│   ├── detect_image.py
│   ├── detect_video.py
│   ├── report.py
│   └── db/
├── app/                  # Streamlit
├── notebooks/            # train_colab.ipynb
├── Dockerfile
└── README.md
```

---

## Trade-offs a decidir pronto

1. **Precisión vs velocidad de demo:** `yolov8n` entrena rápido; `yolov8s/m` si los logos son pequeños en frame.
2. **Frames:** todos vs cada 5.º — afecta la precisión del “tiempo en pantalla”.
3. **Un solo repo** es suficiente para este alcance.
4. **GPU:** entrenar en Colab/Kaggle; inferencia en CPU OK para clips cortos.

---

## Referencias

- [Documentación Ultralytics YOLO](https://docs.ultralytics.com/)

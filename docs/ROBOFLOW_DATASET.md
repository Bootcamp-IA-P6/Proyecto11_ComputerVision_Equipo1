# Roboflow dataset — ISSUE-05

Repository record for the BrandSight Coca-Cola / Pepsi YOLO dataset (ISSUE-05).

Related: [KANBAN.md](./KANBAN.md) · [notebooks/Pepsi_Cocacola_Yolo_version_2.ipynb](../notebooks/Pepsi_Cocacola_Yolo_version_2.ipynb)

---

## Dataset record

a) **Project URL:** https://universe.roboflow.com/thaidd/coca-pepsi-juhuf

b) **Roboflow workspace:** `thaidd`

c) **Project slug:** `coca-pepsi-juhuf`

d) **Project version:** `5` (`Coca-Pepsi-5`)

e) **Export format:** YOLOv11

f) **Task type:** Object detection (bounding boxes)

g) **Class names:**

| Class ID | Name in Roboflow | Name in app (`src/config.py`) |
|----------|------------------|-------------------------------|
| 0 | `CocaCola` | `coca_cola` |
| 1 | `Pepsi` | `pepsi` |

h) **Image counts per brand (source, annotated):**

| Brand | Count |
|-------|-------|
| Coca-Cola | __________ |
| Pepsi | __________ |

i) **Export image counts (from YOLO download):**

| Split | Count |
|-------|-------|
| Train | 1119 |
| Val | 105 |
| Total | 1224 |

j) **Train/validation split:** __________ (e.g. ratio or Roboflow preset name)

k) **Roboflow augmentations (preprocessing on export version):**

| Flip | __________ |
| Brightness | __________ |
| Crop | __________ |
| Other | __________ |

l) **YOLO training augmentations** (if Roboflow aug not used; see notebook):

| Parameter | Value |
|-----------|-------|
| `fliplr` | 0.5 |
| `flipud` | 0.0 |
| `hsv_h` / `hsv_s` / `hsv_v` | 0.015 / 0.7 / 0.4 |
| `mosaic` | 1.0 |
| `auto_augment` | randaugment |

m) **Team Drive dataset zip link:** __________

n) **Team Drive path / filename:** __________

o) **API key env var:** `ROBOFLOW_API_KEY` (see [`.env.example`](../.env.example); not committed)

p) **Notebook reference:** [`notebooks/Pepsi_Cocacola_Yolo_version_2.ipynb`](../notebooks/Pepsi_Cocacola_Yolo_version_2.ipynb)

q) **Notes / known issues:** __________

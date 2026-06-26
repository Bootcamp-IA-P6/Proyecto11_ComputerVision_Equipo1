# BrandSight — Cloud deployment (#13)

Deploy the Streamlit app to **[Streamlit Community Cloud](https://share.streamlit.io)** (free tier). The app shares the same Supabase project as local dev via `DATABASE_URL` and uploads crops to Supabase Storage.

## Prerequisites

- [x] GitHub repo pushed (`Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1`)
- [x] `sql/schema.sql` applied on Supabase
- [x] `sql/storage.sql` applied — bucket `brandsight-crops` exists
- [x] `models/best.pt` in the repo (fine-tuned from `yolo11l.pt` base)
- [ ] Supabase **Session pooler** URI (not direct connection — IPv4 friendly)
- [ ] `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` for crop uploads

## 1. Pre-deploy smoke test (local)

Load secrets the same way Streamlit Cloud will:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml with DATABASE_URL, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, GEMINI_API_KEY

python -m scripts.smoke_deploy
```

Expected output: `OK: smoke_deploy passed — ready for Streamlit Cloud`

## 2. Create the Streamlit Cloud app

1. Sign in at [share.streamlit.io](https://share.streamlit.io) with GitHub.
2. **New app** → select `Bootcamp-IA-P6/Proyecto11_ComputerVision_Equipo1`.
3. **Branch:** `main` or `develop` (whichever you ship from).
4. **Main file path:** `app/streamlit_app.py`
5. **App URL:** e.g. `brandsight-equipo1` → `https://brandsight-equipo1.streamlit.app`

Repo files used automatically:


| File                     | Purpose                              |
| ------------------------ | ------------------------------------ |
| `requirements.txt`       | Python dependencies                  |
| `runtime.txt`            | Python 3.12 (change version to bust stale venv) |
| `.streamlit/config.toml` | Headless server, 200 MB upload limit |


## 3. Configure secrets (never commit these)

In Streamlit Cloud → **App settings → Secrets**, paste:

```toml
DATABASE_URL = "postgresql://postgres.[project-ref]:[PASSWORD]@aws-0-[region].pooler.supabase.com:5432/postgres"
SUPABASE_URL = "https://[project-ref].supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "your_service_role_key"
GEMINI_API_KEY = "your_gemini_key"
MODEL_PATH = "models/best.pt"
CONFIDENCE_THRESHOLD = "0.5"
SAMPLE_STRIDE = "3"
```

`app/bootstrap_secrets.py` copies these into `os.environ` before the app reads settings.

**Security:** Do not log or `st.write()` secret values. Errors are redacted in the UI.

## 4. Deploy and verify

1. Click **Deploy** (or wait for auto-redeploy on push).
2. Open the public URL — sidebar should show **Supabase connected**.
3. **Full demo on live URL:**
  - Upload a short MP4 (30–60 s recommended; long clips may hit Cloud timeouts).
  - Click **Run analysis**.
  - Confirm: metrics table, chart, annotated video, crop thumbnails (from Storage), AI report.
4. In Supabase **Storage** → `brandsight-crops`, confirm new `{video_id}/` folders after analysis.

> **Demo videos:** `data/demo/*.mp4` is gitignored (large files). On Cloud, use **upload** or add a small tracked clip later. Local-only demos stay on your machine.

## 5. Post-deploy checklist (#13)

- [ ] Public URL accessible
- [ ] Sidebar: Supabase connected
- [ ] Upload → analyze → metrics + chart + report on live URL
- [ ] Crop thumbnails visible; objects in `brandsight-crops` bucket
- [ ] No secrets in repo, logs, or UI
- [ ] Add live URL to README: `## Live demo` section

## Troubleshooting


| Symptom                          | Fix                                                                           |
| -------------------------------- | ----------------------------------------------------------------------------- |
| `DATABASE_URL is not set`        | Add secrets in Streamlit Cloud settings; redeploy                             |
| `password authentication failed` | Use **Session pooler** URI; user must be `postgres.[project-ref]`             |
| `Model not found`                | Ensure `models/best.pt` is on the deployed branch                             |
| Storage bucket not found         | Run `sql/storage.sql` in Supabase SQL Editor                                  |
| Crop thumbnails missing          | Set `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY`; use service role key        |
| OpenCV / libGL error             | Use `ultralytics-opencv-headless` + `opencv-python-headless`; no `packages.txt` needed |
| `libgthread-2.0.so.0` missing    | Stale `opencv-python` in cached venv — **Reboot app** (not Rerun); set Python **3.12** in app settings + `runtime.txt` |
| Analysis timeout                 | Use shorter video or increase `SAMPLE_STRIDE` in secrets                      |


## Docker (alternative)

```bash
docker build -t brandsight .
docker run -p 8501:8501 --env-file .env brandsight
```

For Railway/Render, set the same env vars as Streamlit secrets and expose port `8501`.

## Supabase Storage (bbox crops)

Each detection crop is saved locally under `data/crops/{video_id}/` (cache) and uploaded to the `brandsight-crops` bucket. `detections.crop_path` stores a `storage:brandsight-crops/{video_id}/{brand}_{index}.jpg` URI. Streamlit resolves signed URLs at display time, so crops persist across Cloud restarts.

```bash
python -m scripts.check_storage
```

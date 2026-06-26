import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from app.bootstrap_secrets import inject_secrets, redact_secrets

inject_secrets()

from src.config import get_settings
from src.crops import resolve_crop_path
from src.db.connection import check_connection, get_db_session
from src.db import repository

st.set_page_config(page_title="BrandSight", page_icon="🥤", layout="wide")

st.title("BrandSight")
st.caption("Coca-Cola vs Pepsi — brand visibility analysis / análisis de visibilidad de marca")

settings = get_settings()
settings.ensure_dirs()

_is_cloud = os.environ.get("STREAMLIT_RUNTIME_ENVIRONMENT") == "cloud"


def _opencv_packages() -> list[str]:
    import importlib.metadata

    return sorted(
        dist.metadata["Name"]
        for dist in importlib.metadata.distributions()
        if "opencv" in dist.metadata["Name"].lower()
    )


def _safe_error(exc: Exception) -> str:
    return redact_secrets(
        str(exc),
        settings.database_url,
        settings.gemini_api_key,
        settings.openai_api_key,
        settings.supabase_service_role_key,
    )


with st.sidebar:
    st.header("Status / Estado")
    if _is_cloud:
        st.info("Streamlit Cloud")
        opencv_pkgs = _opencv_packages()
        if "opencv-python" in opencv_pkgs:
            st.error(
                "Stale OpenCV detected (`opencv-python`). "
                "Manage app → Reboot app (not Rerun). "
                "If it persists, set Python to 3.12 in app settings and redeploy."
            )
        elif opencv_pkgs:
            st.caption(f"OpenCV: {', '.join(opencv_pkgs)}")
    try:
        check_connection()
        st.success("Supabase connected / Conectado")
    except Exception as exc:
        st.error(f"Database error / Error BD: {_safe_error(exc)}")

    from src.supabase_storage import storage_configured, verify_storage_bucket

    if storage_configured():
        try:
            verify_storage_bucket()
            st.success("Storage ready / Almacenamiento listo")
        except Exception as exc:
            st.warning(f"Storage / Almacenamiento: {_safe_error(exc)}")
    else:
        st.warning("Storage not configured — set SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY")

    st.divider()
    st.markdown("**Settings**")
    st.text(f"Model: {settings.model_path.name}")
    st.text(f"Confidence: {settings.confidence_threshold}")
    st.text(f"Frame stride: {settings.sample_stride}")
    if _is_cloud:
        st.caption("Use upload for demo videos on Cloud.")

tab_upload, tab_history = st.tabs(["Analyze / Analizar", "History / Historial"])

with tab_upload:
    uploaded = st.file_uploader("Upload video (MP4) / Subir vídeo", type=["mp4"])
    demo_dir = settings.uploads_dir.parent / "demo"
    demo_files = sorted(demo_dir.glob("*.mp4")) if demo_dir.exists() else []
    demo_choice = st.selectbox(
        "Or select demo video / O elegir vídeo demo",
        ["—"] + [f.name for f in demo_files],
    )

    if _is_cloud and not demo_files:
        st.caption("No bundled demo on Cloud — upload a 30–60 s MP4.")

    if st.button("Run analysis / Ejecutar análisis", type="primary"):
        video_path: Path | None = None

        if uploaded is not None:
            video_path = settings.uploads_dir / uploaded.name
            video_path.write_bytes(uploaded.getvalue())
        elif demo_choice != "—":
            video_path = demo_dir / demo_choice

        if video_path is None:
            st.warning("Select or upload a video first. / Selecciona o sube un vídeo.")
        elif not settings.model_path.exists():
            st.error(
                f"Model not found at `{settings.model_path}`. "
                "Ensure `models/best.pt` is on the deployed branch."
            )
        else:
            with st.spinner("Analyzing video... / Analizando vídeo..."):
                try:
                    from src.pipeline import analyze_video

                    video_id = analyze_video(video_path)
                    st.session_state["last_video_id"] = video_id
                    st.success(f"Analysis complete / Análisis completo — video_id={video_id}")
                except Exception as exc:
                    st.error(_safe_error(exc))

    video_id = st.session_state.get("last_video_id")
    if video_id:
        with get_db_session() as session:
            video = repository.get_video(session, video_id)
            summaries = repository.get_brand_summaries(session, video_id)
            competitive = repository.get_competitive_analysis(session, video_id)
            report = repository.get_latest_marketing_report(session, video_id)
            detections = repository.get_detections(session, video_id, limit=12)
            video_data = None
            summary_rows = []
            competitive_data = None
            report_data = None
            detection_rows = []
            if video:
                video_data = {
                    "duration_sec": video.duration_sec,
                    "status": video.status,
                    "annotated_path": video.annotated_path,
                }
            for s in summaries:
                summary_rows.append(
                    {
                        "brand": s.brand,
                        "visible_seconds": s.visible_seconds,
                        "visibility_pct": s.visibility_pct,
                        "detections": s.detection_count,
                        "avg_confidence": s.avg_confidence,
                    }
                )
            if competitive:
                competitive_data = competitive.dominant_brand
            if report:
                report_data = report.report_text
            for det in detections:
                detection_rows.append(
                    {
                        "brand": det.brand,
                        "confidence": det.confidence,
                        "frame_number": det.frame_number,
                        "crop_path": det.crop_path,
                    }
                )

        if video_data:
            st.subheader("Results / Resultados")
            col1, col2, col3 = st.columns(3)
            col1.metric("Duration (s)", f"{video_data['duration_sec']:.1f}")
            col2.metric("Status", video_data["status"])
            col3.metric("Dominant brand", competitive_data or "—")

            if summary_rows:
                import pandas as pd

                df = pd.DataFrame(summary_rows)
                st.dataframe(df, use_container_width=True)
                chart_df = df.set_index("brand")[["visible_seconds"]]
                st.bar_chart(chart_df)

            annotated = video_data.get("annotated_path")
            if annotated and Path(annotated).exists():
                st.video(annotated)

            crop_samples = [
                (row, resolve_crop_path(row["crop_path"]))
                for row in detection_rows
                if resolve_crop_path(row["crop_path"]) is not None
            ]
            if crop_samples:
                st.subheader("Detection crops / Recortes de detección")
                cols = st.columns(min(len(crop_samples), 4))
                for idx, (row, crop_path) in enumerate(crop_samples):
                    cols[idx % len(cols)].image(
                        str(crop_path),
                        caption=f"{row['brand']} · {row['confidence']:.0%} · f{row['frame_number']}",
                        use_container_width=True,
                    )

            if report_data:
                st.subheader("AI Marketing Report / Informe de marketing IA")
                st.markdown(report_data)

with tab_history:
    try:
        with get_db_session() as session:
            videos = repository.list_videos(session)
            history = [(v.id, v.filename, v.status, v.duration_sec) for v in videos]
        if not history:
            st.info("No analyses yet. / Aún no hay análisis.")
        else:
            for vid, filename, status, duration in history:
                st.write(f"**#{vid}** — {filename} — {status} — {duration:.1f}s")
    except Exception as exc:
        st.error(_safe_error(exc))

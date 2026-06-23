import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from src.config import BRAND_COCA_COLA, BRAND_PEPSI, get_settings
from src.crops import resolve_crop_path
from src.db.connection import check_connection, get_db_session
from src.db import repository
from src.pipeline import analyze_video

st.set_page_config(page_title="BrandSight", page_icon="🥤", layout="wide")

st.title("BrandSight")
st.caption("Coca-Cola vs Pepsi — brand visibility analysis / análisis de visibilidad de marca")

settings = get_settings()
settings.ensure_dirs()

with st.sidebar:
    st.header("Status / Estado")
    try:
        check_connection()
        st.success("Supabase connected / Conectado")
    except Exception as exc:
        st.error(f"Database error / Error BD: {exc}")

    st.divider()
    st.markdown("**Settings**")
    st.text(f"Model: {settings.model_path}")
    st.text(f"Confidence: {settings.confidence_threshold}")
    st.text(f"Frame stride: {settings.sample_stride}")

tab_upload, tab_history = st.tabs(["Analyze / Analizar", "History / Historial"])

with tab_upload:
    uploaded = st.file_uploader("Upload video (MP4) / Subir vídeo", type=["mp4"])
    demo_dir = settings.uploads_dir.parent / "demo"
    demo_files = sorted(demo_dir.glob("*.mp4")) if demo_dir.exists() else []
    demo_choice = st.selectbox(
        "Or select demo video / O elegir vídeo demo",
        ["—"] + [f.name for f in demo_files],
    )

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
                "Train in Colab and add `best.pt` to `models/`."
            )
        else:
            with st.spinner("Analyzing video... / Analizando vídeo..."):
                try:
                    video_id = analyze_video(video_path)
                    st.session_state["last_video_id"] = video_id
                    st.success(f"Analysis complete / Análisis completo — video_id={video_id}")
                except Exception as exc:
                    st.error(str(exc))

    video_id = st.session_state.get("last_video_id")
    if video_id:
        with get_db_session() as session:
            video = repository.get_video(session, video_id)
            summaries = repository.get_brand_summaries(session, video_id)
            competitive = repository.get_competitive_analysis(session, video_id)
            report = repository.get_latest_marketing_report(session, video_id)
            detections = repository.get_detections(session, video_id, limit=12)

        if video:
            st.subheader("Results / Resultados")
            col1, col2, col3 = st.columns(3)
            col1.metric("Duration (s)", f"{video.duration_sec:.1f}")
            col2.metric("Status", video.status)
            col3.metric("Dominant brand", competitive.dominant_brand if competitive else "—")

            if summaries:
                import pandas as pd

                df = pd.DataFrame(
                    [
                        {
                            "brand": s.brand,
                            "visible_seconds": s.visible_seconds,
                            "visibility_pct": s.visibility_pct,
                            "detections": s.detection_count,
                            "avg_confidence": s.avg_confidence,
                        }
                        for s in summaries
                    ]
                )
                st.dataframe(df, use_container_width=True)
                chart_df = df.set_index("brand")[["visible_seconds"]]
                st.bar_chart(chart_df)

            if video.annotated_path and Path(video.annotated_path).exists():
                st.video(video.annotated_path)

            crop_samples = [
                (det, resolve_crop_path(det.crop_path))
                for det in detections
                if resolve_crop_path(det.crop_path) is not None
            ]
            if crop_samples:
                st.subheader("Detection crops / Recortes de detección")
                cols = st.columns(min(len(crop_samples), 4))
                for idx, (det, crop_path) in enumerate(crop_samples):
                    cols[idx % len(cols)].image(
                        str(crop_path),
                        caption=f"{det.brand} · {det.confidence:.0%} · f{det.frame_number}",
                        use_container_width=True,
                    )

            if report:
                st.subheader("AI Marketing Report / Informe de marketing IA")
                st.markdown(report.report_text)

with tab_history:
    try:
        with get_db_session() as session:
            videos = repository.list_videos(session)
        if not videos:
            st.info("No analyses yet. / Aún no hay análisis.")
        else:
            for video in videos:
                st.write(f"**#{video.id}** — {video.filename} — {video.status} — {video.duration_sec:.1f}s")
    except Exception as exc:
        st.error(str(exc))

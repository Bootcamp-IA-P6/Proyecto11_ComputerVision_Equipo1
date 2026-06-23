from pathlib import Path

from src.crops import save_detection_crops
from src.config import get_settings
from src.db.connection import get_db_session
from src.db import repository
from src.detect_video import detect_video
from src.metrics import persist_visibility_analysis
from src.metrics_export import export_metrics_files
from src.report.generate_marketing_report import PROMPT_VERSION, generate_marketing_report, save_report_to_file


def analyze_video(video_path: Path, *, weights_path: Path | None = None) -> int:
    settings = get_settings()
    settings.ensure_dirs()
    weights = weights_path or settings.model_path

    if not weights.exists():
        raise FileNotFoundError(
            f"Model weights not found at {weights}. Train in Colab and place best.pt in models/."
        )

    annotated_path, detections, duration_sec, fps, total_frames = detect_video(video_path, weights)

    with get_db_session() as session:
        video = repository.create_video(
            session,
            filename=video_path.name,
            storage_path=video_path,
            duration_sec=duration_sec,
            fps=fps,
            total_frames=total_frames,
            status="processing",
        )
        video_id = video.id

        enriched = save_detection_crops(video_path, video_id, detections)
        if enriched:
            repository.bulk_insert_detections(session, enriched)

        payload = persist_visibility_analysis(
            session,
            video_id,
            enriched,
            duration_sec=duration_sec,
            fps=fps,
            sample_stride=settings.sample_stride,
            video_filename=video_path.name,
        )
        export_metrics_files(payload, video_id)

        report_text, model_name = generate_marketing_report(payload)
        report_path = save_report_to_file(video_id, report_text)
        repository.save_marketing_report(
            session,
            video_id,
            {
                "model_name": model_name,
                "prompt_version": PROMPT_VERSION,
                "report_text": report_text,
                "report_path": str(report_path),
            },
        )

        repository.update_video_status(
            session,
            video_id,
            status="done",
            annotated_path=annotated_path,
        )

    return video_id

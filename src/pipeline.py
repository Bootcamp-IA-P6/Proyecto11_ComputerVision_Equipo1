from pathlib import Path

import cv2

from src.config import get_settings
from src.db.connection import get_db_session
from src.db import repository
from src.detect_video import detect_video
from src.metrics import (
    brand_metrics_to_dict,
    build_metrics_payload,
    competitive_result_to_dict,
    compute_brand_metrics,
    compute_competitive_analysis,
)
from src.report.generate_marketing_report import PROMPT_VERSION, generate_marketing_report, save_report_to_file


def _save_crops(video_path: Path, video_id: int, detections: list[dict]) -> list[dict]:
    settings = get_settings()
    crop_dir = settings.crops_dir / str(video_id)
    crop_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return detections

    frames_cache: dict[int, object] = {}
    enriched: list[dict] = []

    for idx, det in enumerate(detections):
        frame_number = det["frame_number"]
        if frame_number not in frames_cache:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ok, frame = cap.read()
            frames_cache[frame_number] = frame if ok else None

        frame = frames_cache[frame_number]
        crop_path = None
        if frame is not None:
            x, y, w, h = int(det["bbox_x"]), int(det["bbox_y"]), int(det["bbox_w"]), int(det["bbox_h"])
            h_img, w_img = frame.shape[:2]
            x2, y2 = min(x + w, w_img), min(y + h, h_img)
            x, y = max(x, 0), max(y, 0)
            if x2 > x and y2 > y:
                crop = frame[y:y2, x:x2]
                crop_file = crop_dir / f"{det['brand']}_{idx}.jpg"
                cv2.imwrite(str(crop_file), crop)
                crop_path = str(crop_file)

        enriched.append({**det, "crop_path": crop_path, "video_id": video_id})

    cap.release()
    return enriched


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

        enriched = _save_crops(video_path, video_id, detections)
        if enriched:
            repository.bulk_insert_detections(session, enriched)

        brand_metrics = compute_brand_metrics(
            enriched,
            duration_sec=duration_sec,
            fps=fps,
            sample_stride=settings.sample_stride,
        )
        competitive = compute_competitive_analysis(brand_metrics, duration_sec=duration_sec)

        repository.save_brand_summaries(
            session,
            video_id,
            [brand_metrics_to_dict(item) for item in brand_metrics],
        )
        repository.save_competitive_analysis(session, video_id, competitive_result_to_dict(competitive))

        payload = build_metrics_payload(video_path.name, duration_sec, brand_metrics, competitive)
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

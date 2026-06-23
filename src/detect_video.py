"""Video logo detection with YOLO — annotated MP4 and optional Supabase persistence (#8)."""

import argparse
from pathlib import Path

import cv2
import numpy as np

from src.config import BRAND_COCA_COLA, BRAND_LABELS, BRAND_PEPSI, get_settings

_FONT = cv2.FONT_HERSHEY_SIMPLEX
_BRAND_COLORS = {
    BRAND_COCA_COLA: (0, 0, 220),
    BRAND_PEPSI: (220, 120, 0),
}


def _brand_name(class_id: int) -> str:
    return BRAND_LABELS.get(class_id, f"class_{class_id}")


def _draw_detection(frame: np.ndarray, brand: str, confidence: float, x1: float, y1: float, x2: float, y2: float) -> None:
    """Draw bbox with brand name and confidence % below the box."""
    ix1, iy1, ix2, iy2 = int(x1), int(y1), int(x2), int(y2)
    color = _BRAND_COLORS.get(brand, (0, 200, 0))
    cv2.rectangle(frame, (ix1, iy1), (ix2, iy2), color, 2)

    brand_text = brand
    conf_text = f"{confidence * 100:.0f}%"
    brand_scale, conf_scale = 0.55, 0.5
    brand_thickness, conf_thickness = 2, 1

    (_, brand_h), _ = cv2.getTextSize(brand_text, _FONT, brand_scale, brand_thickness)
    (_, conf_h), _ = cv2.getTextSize(conf_text, _FONT, conf_scale, conf_thickness)
    gap = 4
    brand_y = iy2 + brand_h + gap
    conf_y = brand_y + conf_h + gap

    h, w = frame.shape[:2]
    if conf_y >= h:
        brand_y = max(iy1 - gap, brand_h)
        conf_y = brand_y - conf_h - gap

    for text, y, scale, thickness in (
        (brand_text, brand_y, brand_scale, brand_thickness),
        (conf_text, conf_y, conf_scale, conf_thickness),
    ):
        (tw, th), _ = cv2.getTextSize(text, _FONT, scale, thickness)
        tx = min(ix1, max(0, w - tw - 2))
        ty = min(max(th, y), h - 2)
        cv2.rectangle(frame, (tx, ty - th - 2), (tx + tw + 2, ty + 2), color, -1)
        cv2.putText(frame, text, (tx, ty), _FONT, scale, (255, 255, 255), thickness, cv2.LINE_AA)


def detect_video(
    video_path: Path,
    weights_path: Path,
    *,
    output_path: Path | None = None,
    sample_stride: int | None = None,
) -> tuple[Path, list[dict], float, float, int]:
    """Run YOLO on video frames; return annotated path, detection rows, duration, fps, frame count."""
    from ultralytics import YOLO

    settings = get_settings()
    settings.ensure_dirs()
    stride = sample_stride or settings.sample_stride

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration_sec = total_frames / fps if fps else 0.0

    out = output_path or settings.outputs_dir / f"annotated_{video_path.name}"
    out.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(out),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    model = YOLO(str(weights_path))
    detections: list[dict] = []
    overlay_boxes: list[tuple[str, float, float, float, float, float]] = []
    frame_idx = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        if frame_idx % stride == 0:
            results = model.predict(frame, conf=settings.confidence_threshold, verbose=False)
            result = results[0]
            timestamp_sec = frame_idx / fps
            overlay_boxes = []

            if result.boxes is not None:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    brand = _brand_name(cls_id)
                    detections.append(
                        {
                            "brand": brand,
                            "confidence": conf,
                            "frame_number": frame_idx,
                            "timestamp_sec": round(timestamp_sec, 3),
                            "bbox_x": x1,
                            "bbox_y": y1,
                            "bbox_w": x2 - x1,
                            "bbox_h": y2 - y1,
                        }
                    )
                    overlay_boxes.append((brand, conf, x1, y1, x2, y2))

        annotated = frame.copy()
        for brand, conf, x1, y1, x2, y2 in overlay_boxes:
            _draw_detection(annotated, brand, conf, x1, y1, x2, y2)

        writer.write(annotated)
        frame_idx += 1

    cap.release()
    writer.release()
    return out, detections, duration_sec, fps, total_frames


def persist_video_detections(
    video_path: Path,
    annotated_path: Path,
    detections: list[dict],
    *,
    duration_sec: float,
    fps: float,
    total_frames: int,
    sample_stride: int | None = None,
) -> tuple[int, dict | None]:
    """Insert video, detections, and visibility metrics into Supabase.

    Returns ``(video_id, metrics_payload)``.
    """
    from src.db.connection import get_db_session
    from src.db import repository
    from src.metrics import persist_visibility_analysis
    from src.metrics_export import export_metrics_files

    settings = get_settings()
    stride = sample_stride or settings.sample_stride
    metrics_payload: dict | None = None

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
        rows = [{**det, "video_id": video_id} for det in detections]
        if rows:
            repository.bulk_insert_detections(session, rows)

        metrics_payload = persist_visibility_analysis(
            session,
            video_id,
            detections,
            duration_sec=duration_sec,
            fps=fps,
            sample_stride=stride,
            video_filename=video_path.name,
        )
        repository.update_video_status(
            session,
            video_id,
            status="done",
            annotated_path=annotated_path,
        )

    if metrics_payload is not None:
        export_metrics_files(metrics_payload, video_id)

    return video_id, metrics_payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect Coca-Cola and Pepsi logos in a video.")
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--weights", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--stride", type=int, default=None)
    parser.add_argument(
        "--no-db",
        action="store_true",
        help="Skip writing detections to Supabase (default: persist when DATABASE_URL is set)",
    )
    args = parser.parse_args()

    settings = get_settings()
    settings.ensure_dirs()
    weights = args.weights or settings.model_path
    if not weights.exists():
        raise FileNotFoundError(
            f"Model weights not found at {weights}. Train in Colab (#5) and place best.pt in models/."
        )

    stride = args.stride or settings.sample_stride
    out, detections, duration, fps, frames = detect_video(
        args.video, weights, output_path=args.output, sample_stride=stride
    )
    print(f"Saved annotated video to {out}")
    print(f"Duration: {duration:.2f}s | FPS: {fps:.2f} | Detections: {len(detections)} | Frames: {frames}")

    if args.no_db:
        return

    if not settings.database_url:
        print("DATABASE_URL not set — skipping Supabase persist (use .env or pass --no-db).")
        return

    video_id, metrics_payload = persist_video_detections(
        args.video,
        out,
        detections,
        duration_sec=duration,
        fps=fps,
        total_frames=frames,
        sample_stride=stride,
    )
    print(f"Supabase: videos.id={video_id} | {len(detections)} rows in detections")
    if metrics_payload:
        from src.metrics_export import format_metrics_text

        print("\n" + format_metrics_text(metrics_payload))
        print(f"\nMetrics files: data/outputs/metrics_{video_id}.json")


if __name__ == "__main__":
    main()

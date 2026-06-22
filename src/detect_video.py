import argparse
from pathlib import Path

import cv2

from src.config import BRAND_LABELS, get_settings


def _brand_name(class_id: int) -> str:
    return BRAND_LABELS.get(class_id, f"class_{class_id}")


def detect_video(
    video_path: Path,
    weights_path: Path,
    *,
    output_path: Path | None = None,
    sample_stride: int | None = None,
) -> tuple[Path, list[dict], float, float, int]:
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
    frame_idx = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        if frame_idx % stride == 0:
            results = model.predict(frame, conf=settings.confidence_threshold, verbose=False)
            result = results[0]
            timestamp_sec = frame_idx / fps

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

            frame = result.plot()

        writer.write(frame)
        frame_idx += 1

    cap.release()
    writer.release()
    return out, detections, duration_sec, fps, total_frames


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect Coca-Cola and Pepsi logos in a video.")
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--weights", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--stride", type=int, default=None)
    args = parser.parse_args()

    settings = get_settings()
    weights = args.weights or settings.model_path
    out, detections, duration, fps, frames = detect_video(
        args.video, weights, output_path=args.output, sample_stride=args.stride
    )
    print(f"Saved annotated video to {out}")
    print(f"Duration: {duration:.2f}s | FPS: {fps:.2f} | Detections: {len(detections)} | Frames: {frames}")


if __name__ == "__main__":
    main()

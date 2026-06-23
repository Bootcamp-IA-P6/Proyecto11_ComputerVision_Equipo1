"""Bbox crop extraction and persistence (#10)."""

from pathlib import Path

import cv2

from src.config import get_settings


def crop_dir_for_video(video_id: int) -> Path:
    """Return ``data/crops/{video_id}/`` (created on save)."""
    settings = get_settings()
    crop_dir = settings.crops_dir / str(video_id)
    crop_dir.mkdir(parents=True, exist_ok=True)
    return crop_dir


def save_detection_crops(
    video_path: Path,
    video_id: int,
    detections: list[dict],
    *,
    max_crops: int | None = None,
) -> list[dict]:
    """Save logo crops to disk and return detection dicts with ``crop_path`` + ``video_id``.

    Crops are stored under ``data/crops/{video_id}/{brand}_{index}.jpg``.
    Paths are absolute so they resolve locally and in Streamlit on the same machine.
    """
    if not detections:
        return []

    settings = get_settings()
    crop_dir = crop_dir_for_video(video_id)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return [{**det, "crop_path": None, "video_id": video_id} for det in detections]

    frames_cache: dict[int, object] = {}
    enriched: list[dict] = []
    rows = detections if max_crops is None else detections[:max_crops]

    for idx, det in enumerate(rows):
        frame_number = det["frame_number"]
        if frame_number not in frames_cache:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ok, frame = cap.read()
            frames_cache[frame_number] = frame if ok else None

        frame = frames_cache[frame_number]
        crop_path: str | None = None
        if frame is not None:
            x = int(det["bbox_x"])
            y = int(det["bbox_y"])
            w = int(det["bbox_w"])
            h = int(det["bbox_h"])
            h_img, w_img = frame.shape[:2]
            x2, y2 = min(x + w, w_img), min(y + h, h_img)
            x, y = max(x, 0), max(y, 0)
            if x2 > x and y2 > y:
                crop = frame[y:y2, x:x2]
                crop_file = crop_dir / f"{det['brand']}_{idx}.jpg"
                cv2.imwrite(str(crop_file), crop)
                crop_path = str(crop_file.resolve())

        enriched.append({**det, "crop_path": crop_path, "video_id": video_id})

    cap.release()

    if max_crops is not None and len(detections) > max_crops:
        for det in detections[max_crops:]:
            enriched.append({**det, "crop_path": None, "video_id": video_id})

    return enriched


def count_saved_crops(detections: list[dict]) -> int:
    return sum(1 for det in detections if det.get("crop_path"))


def resolve_crop_path(crop_path: str | None) -> Path | None:
    """Return a readable path if the crop file exists."""
    if not crop_path:
        return None
    path = Path(crop_path)
    return path if path.is_file() else None

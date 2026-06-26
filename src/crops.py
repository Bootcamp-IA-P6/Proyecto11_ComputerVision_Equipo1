"""Bbox crop extraction and persistence (#10)."""

from pathlib import Path

from src.config import get_settings
from src.supabase_storage import (
    crop_object_key,
    parse_storage_uri,
    storage_configured,
    upload_crop_file,
)


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
    """Save logo crops and return detection dicts with ``crop_path`` + ``video_id``.

    Crops are written under ``data/crops/{video_id}/`` and uploaded to Supabase Storage
    when ``SUPABASE_URL`` and ``SUPABASE_SERVICE_ROLE_KEY`` are set. ``crop_path`` stores
    a ``storage:{bucket}/{video_id}/{brand}_{index}.jpg`` URI, or a local absolute path
    as fallback when Storage is not configured.
    """
    if not detections:
        return []

    import cv2

    settings = get_settings()
    crop_dir = crop_dir_for_video(video_id)
    upload_enabled = storage_configured()
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
                if upload_enabled:
                    object_key = crop_object_key(video_id, det["brand"], idx)
                    crop_path = upload_crop_file(crop_file, object_key)
                else:
                    crop_path = str(crop_file.resolve())

        enriched.append({**det, "crop_path": crop_path, "video_id": video_id})

    cap.release()

    if max_crops is not None and len(detections) > max_crops:
        for det in detections[max_crops:]:
            enriched.append({**det, "crop_path": None, "video_id": video_id})

    return enriched


def count_saved_crops(detections: list[dict]) -> int:
    return sum(1 for det in detections if det.get("crop_path"))


def resolve_crop_path(crop_path: str | None) -> Path | str | None:
    """Return a readable local path or signed URL for display."""
    if not crop_path:
        return None

    parsed = parse_storage_uri(crop_path)
    if parsed is not None:
        if not storage_configured():
            return None
        from src.supabase_storage import create_signed_crop_url

        bucket, object_key = parsed
        return create_signed_crop_url(bucket, object_key)

    path = Path(crop_path)
    return path if path.is_file() else None


def crop_path_is_readable(crop_path: str | None) -> bool:
    return resolve_crop_path(crop_path) is not None

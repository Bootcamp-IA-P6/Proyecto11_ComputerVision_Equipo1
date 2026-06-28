"""Annotated video encoding, Supabase Storage upload, and playback resolution."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from src.supabase_storage import (
    annotated_object_key,
    create_signed_crop_url,
    parse_storage_uri,
    storage_configured,
    upload_storage_file,
)

logger = logging.getLogger(__name__)


def ensure_browser_mp4(source: Path) -> Path:
    """Return an H.264 MP4 that browsers can play in ``<video>`` tags."""
    if not source.is_file():
        return source

    dest = source.with_name(f"{source.stem}_web.mp4")
    if dest.is_file() and dest.stat().st_mtime >= source.stat().st_mtime and dest.stat().st_size > 0:
        return dest

    try:
        import imageio_ffmpeg

        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        result = subprocess.run(
            [
                ffmpeg,
                "-y",
                "-i",
                str(source),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(dest),
            ],
            capture_output=True,
            check=False,
        )
        if result.returncode == 0 and dest.is_file() and dest.stat().st_size > 0:
            return dest
        logger.warning(
            "H.264 transcode failed for %s (exit %s): %s",
            source,
            result.returncode,
            result.stderr.decode(errors="replace")[-500:],
        )
    except Exception as exc:
        logger.warning("Could not transcode annotated video to H.264: %s", exc)

    return source


def persist_annotated_video(local_path: Path, video_id: int) -> str:
    """Upload annotated MP4 to Storage when configured; else return local path."""
    playable = ensure_browser_mp4(local_path)
    if storage_configured():
        object_key = annotated_object_key(video_id)
        return upload_storage_file(playable, object_key, content_type="video/mp4")
    return str(playable.resolve())


def resolve_annotated_path(annotated_path: str | None) -> Path | str | None:
    """Return a local path or signed URL suitable for ``st.video``."""
    if not annotated_path:
        return None

    parsed = parse_storage_uri(annotated_path)
    if parsed is not None:
        if not storage_configured():
            return None
        bucket, object_key = parsed
        return create_signed_crop_url(bucket, object_key)

    path = Path(annotated_path)
    if path.is_file():
        return path

    web_path = path.with_name(f"{path.stem}_web{path.suffix}")
    if web_path.is_file():
        return web_path

    return None

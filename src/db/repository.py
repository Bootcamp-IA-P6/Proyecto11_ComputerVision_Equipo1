"""CRUD helpers for BrandSight tables (videos, detections, summaries, reports).

All write functions expect an active SQLAlchemy ``Session`` (use ``get_db_session``).
File paths accept ``pathlib.Path`` and are stored as strings in the database.
"""

from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.db.models import (
    BrandSummary,
    CompetitiveAnalysis,
    Detection,
    MarketingReport,
    Video,
)


def create_video(
    session: Session,
    *,
    filename: str,
    storage_path: str | Path,
    duration_sec: float,
    fps: float | None = None,
    total_frames: int | None = None,
    status: str = "pending",
) -> Video:
    """Insert a new row in ``videos`` and return the flushed ORM instance."""
    video = Video(
        filename=filename,
        storage_path=str(storage_path),
        duration_sec=duration_sec,
        fps=fps,
        total_frames=total_frames,
        status=status,
    )
    session.add(video)
    session.flush()
    return video


def update_video_status(
    session: Session,
    video_id: int,
    *,
    status: str,
    annotated_path: str | Path | None = None,
) -> Video:
    """Update ``status`` and optional ``annotated_path`` for an existing video."""
    video = session.get(Video, video_id)
    if video is None:
        raise ValueError(f"Video {video_id} not found")
    video.status = status
    if annotated_path is not None:
        video.annotated_path = str(annotated_path)
    session.flush()
    return video


def bulk_insert_detections(session: Session, rows: list[dict]) -> None:
    """Insert detection dicts into ``detections`` (keys must match column names)."""
    session.add_all([Detection(**row) for row in rows])


def save_brand_summaries(session: Session, video_id: int, summaries: list[dict]) -> None:
    """Insert per-brand visibility rows into ``brand_summary``."""
    for item in summaries:
        session.add(BrandSummary(video_id=video_id, **item))


def save_competitive_analysis(session: Session, video_id: int, data: dict) -> CompetitiveAnalysis:
    """Insert one ``competitive_analysis`` row for a video."""
    row = CompetitiveAnalysis(video_id=video_id, **data)
    session.add(row)
    session.flush()
    return row


def save_marketing_report(session: Session, video_id: int, data: dict) -> MarketingReport:
    """Insert a row into ``marketing_reports``."""
    row = MarketingReport(video_id=video_id, **data)
    session.add(row)
    session.flush()
    return row


def get_video(session: Session, video_id: int) -> Video | None:
    """Fetch a single video by primary key."""
    return session.get(Video, video_id)


def list_videos(session: Session, limit: int = 20) -> list[Video]:
    """List recent videos, newest ``processed_at`` first."""
    stmt = select(Video).order_by(Video.processed_at.desc()).limit(limit)
    return list(session.scalars(stmt).all())


def get_detections(
    session: Session,
    video_id: int,
    *,
    brand: str | None = None,
    limit: int | None = None,
) -> list[Detection]:
    """Query detections for a video, optionally filtered by brand."""
    stmt = select(Detection).where(Detection.video_id == video_id).order_by(Detection.frame_number)
    if brand is not None:
        stmt = stmt.where(Detection.brand == brand)
    if limit is not None:
        stmt = stmt.limit(limit)
    return list(session.scalars(stmt).all())


def count_detections(session: Session, video_id: int) -> int:
    """Return total detection count for a video."""
    stmt = select(func.count()).select_from(Detection).where(Detection.video_id == video_id)
    return int(session.scalar(stmt) or 0)


def get_brand_summaries(session: Session, video_id: int) -> list[BrandSummary]:
    """Fetch all brand summary rows for a video."""
    stmt = select(BrandSummary).where(BrandSummary.video_id == video_id)
    return list(session.scalars(stmt).all())


def get_competitive_analysis(session: Session, video_id: int) -> CompetitiveAnalysis | None:
    """Fetch competitive analysis for a video (at most one row)."""
    stmt = select(CompetitiveAnalysis).where(CompetitiveAnalysis.video_id == video_id)
    return session.scalar(stmt)


def get_latest_marketing_report(session: Session, video_id: int) -> MarketingReport | None:
    """Fetch the most recent marketing report for a video."""
    stmt = (
        select(MarketingReport)
        .where(MarketingReport.video_id == video_id)
        .order_by(MarketingReport.generated_at.desc())
        .limit(1)
    )
    return session.scalar(stmt)


def delete_video(session: Session, video_id: int) -> bool:
    """Delete a video and cascade-related rows. Returns False if not found."""
    video = session.get(Video, video_id)
    if video is None:
        return False
    session.delete(video)
    session.flush()
    return True

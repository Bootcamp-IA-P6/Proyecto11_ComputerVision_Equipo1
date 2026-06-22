from pathlib import Path

from sqlalchemy import select
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
    video = session.get(Video, video_id)
    if video is None:
        raise ValueError(f"Video {video_id} not found")
    video.status = status
    if annotated_path is not None:
        video.annotated_path = str(annotated_path)
    session.flush()
    return video


def bulk_insert_detections(session: Session, rows: list[dict]) -> None:
    session.bulk_insert_mappings(Detection, rows)


def save_brand_summaries(session: Session, video_id: int, summaries: list[dict]) -> None:
    for item in summaries:
        session.add(BrandSummary(video_id=video_id, **item))


def save_competitive_analysis(session: Session, video_id: int, data: dict) -> CompetitiveAnalysis:
    row = CompetitiveAnalysis(video_id=video_id, **data)
    session.add(row)
    session.flush()
    return row


def save_marketing_report(session: Session, video_id: int, data: dict) -> MarketingReport:
    row = MarketingReport(video_id=video_id, **data)
    session.add(row)
    session.flush()
    return row


def get_video(session: Session, video_id: int) -> Video | None:
    return session.get(Video, video_id)


def list_videos(session: Session, limit: int = 20) -> list[Video]:
    stmt = select(Video).order_by(Video.processed_at.desc()).limit(limit)
    return list(session.scalars(stmt).all())


def get_brand_summaries(session: Session, video_id: int) -> list[BrandSummary]:
    stmt = select(BrandSummary).where(BrandSummary.video_id == video_id)
    return list(session.scalars(stmt).all())


def get_competitive_analysis(session: Session, video_id: int) -> CompetitiveAnalysis | None:
    stmt = select(CompetitiveAnalysis).where(CompetitiveAnalysis.video_id == video_id)
    return session.scalar(stmt)


def get_latest_marketing_report(session: Session, video_id: int) -> MarketingReport | None:
    stmt = (
        select(MarketingReport)
        .where(MarketingReport.video_id == video_id)
        .order_by(MarketingReport.generated_at.desc())
        .limit(1)
    )
    return session.scalar(stmt)

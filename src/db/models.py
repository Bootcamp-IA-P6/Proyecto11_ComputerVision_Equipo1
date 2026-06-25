"""SQLAlchemy ORM models matching ``sql/schema.sql``."""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(Text, nullable=False)
    duration_sec: Mapped[float] = mapped_column(Float, nullable=False)
    fps: Mapped[float | None] = mapped_column(Float)
    total_frames: Mapped[int | None] = mapped_column(Integer)
    annotated_path: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    detections: Mapped[list["Detection"]] = relationship(
        back_populates="video", cascade="all, delete-orphan"
    )
    brand_summaries: Mapped[list["BrandSummary"]] = relationship(
        back_populates="video", cascade="all, delete-orphan"
    )
    competitive_analysis: Mapped["CompetitiveAnalysis | None"] = relationship(
        back_populates="video", cascade="all, delete-orphan", uselist=False
    )
    marketing_reports: Mapped[list["MarketingReport"]] = relationship(
        back_populates="video", cascade="all, delete-orphan"
    )


class Detection(Base):
    __tablename__ = "detections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    brand: Mapped[str] = mapped_column(String(50), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    frame_number: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp_sec: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_x: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_y: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_w: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_h: Mapped[float] = mapped_column(Float, nullable=False)
    crop_path: Mapped[str | None] = mapped_column(Text)

    video: Mapped["Video"] = relationship(back_populates="detections")


class BrandSummary(Base):
    __tablename__ = "brand_summary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    brand: Mapped[str] = mapped_column(String(50), nullable=False)
    visible_seconds: Mapped[float] = mapped_column(Float, nullable=False)
    visibility_pct: Mapped[float] = mapped_column(Float, nullable=False)
    detection_count: Mapped[int] = mapped_column(Integer, nullable=False)
    avg_confidence: Mapped[float | None] = mapped_column(Float)

    video: Mapped["Video"] = relationship(back_populates="brand_summaries")


class CompetitiveAnalysis(Base):
    __tablename__ = "competitive_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"), nullable=False, unique=True)
    dominant_brand: Mapped[str] = mapped_column(String(50), nullable=False)
    coca_cola_seconds: Mapped[float] = mapped_column(Float, nullable=False)
    pepsi_seconds: Mapped[float] = mapped_column(Float, nullable=False)
    coca_cola_pct: Mapped[float] = mapped_column(Float, nullable=False)
    pepsi_pct: Mapped[float] = mapped_column(Float, nullable=False)
    visibility_gap_sec: Mapped[float] = mapped_column(Float, nullable=False)
    balance_label: Mapped[str] = mapped_column(String(30), nullable=False)

    video: Mapped["Video"] = relationship(back_populates="competitive_analysis")


class MarketingReport(Base):
    __tablename__ = "marketing_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    model_name: Mapped[str | None] = mapped_column(String(100))
    prompt_version: Mapped[str | None] = mapped_column(String(20))
    report_text: Mapped[str] = mapped_column(Text, nullable=False)
    report_path: Mapped[str | None] = mapped_column(Text)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    video: Mapped["Video"] = relationship(back_populates="marketing_reports")

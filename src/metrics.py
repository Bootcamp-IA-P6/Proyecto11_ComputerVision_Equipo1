from dataclasses import dataclass
from pathlib import Path

from src.config import BRAND_COCA_COLA, BRAND_PEPSI, get_settings


@dataclass
class BrandMetrics:
    brand: str
    visible_seconds: float
    visibility_pct: float
    detection_count: int
    avg_confidence: float


@dataclass
class CompetitiveResult:
    dominant_brand: str
    coca_cola_seconds: float
    pepsi_seconds: float
    coca_cola_pct: float
    pepsi_pct: float
    visibility_gap_sec: float
    balance_label: str


def compute_brand_metrics(
    detections: list[dict],
    *,
    duration_sec: float,
    fps: float,
    sample_stride: int,
) -> list[BrandMetrics]:
    if duration_sec <= 0 or fps <= 0:
        return []

    frame_interval = sample_stride / fps
    brands = (BRAND_COCA_COLA, BRAND_PEPSI)
    metrics: list[BrandMetrics] = []

    for brand in brands:
        brand_rows = [row for row in detections if row["brand"] == brand]
        visible_frames = {row["frame_number"] for row in brand_rows}
        visible_seconds = len(visible_frames) * frame_interval
        visibility_pct = (visible_seconds / duration_sec) * 100
        avg_confidence = (
            sum(row["confidence"] for row in brand_rows) / len(brand_rows) if brand_rows else 0.0
        )
        metrics.append(
            BrandMetrics(
                brand=brand,
                visible_seconds=round(visible_seconds, 2),
                visibility_pct=round(visibility_pct, 2),
                detection_count=len(brand_rows),
                avg_confidence=round(avg_confidence, 4),
            )
        )

    return metrics


def compute_competitive_analysis(
    brand_metrics: list[BrandMetrics],
    *,
    duration_sec: float,
    balance_threshold_pct: float = 5.0,
) -> CompetitiveResult:
    by_brand = {item.brand: item for item in brand_metrics}
    coca = by_brand.get(BRAND_COCA_COLA)
    pepsi = by_brand.get(BRAND_PEPSI)

    coca_seconds = coca.visible_seconds if coca else 0.0
    pepsi_seconds = pepsi.visible_seconds if pepsi else 0.0
    coca_pct = coca.visibility_pct if coca else 0.0
    pepsi_pct = pepsi.visibility_pct if pepsi else 0.0
    gap = abs(coca_seconds - pepsi_seconds)

    if gap < (balance_threshold_pct / 100) * duration_sec:
        balance_label = "balanced"
        dominant_brand = "balanced"
    elif coca_seconds >= pepsi_seconds:
        balance_label = "coca_cola_dominant"
        dominant_brand = BRAND_COCA_COLA
    else:
        balance_label = "pepsi_dominant"
        dominant_brand = BRAND_PEPSI

    return CompetitiveResult(
        dominant_brand=dominant_brand,
        coca_cola_seconds=coca_seconds,
        pepsi_seconds=pepsi_seconds,
        coca_cola_pct=coca_pct,
        pepsi_pct=pepsi_pct,
        visibility_gap_sec=round(gap, 2),
        balance_label=balance_label,
    )


def brand_metrics_to_dict(metrics: BrandMetrics) -> dict:
    return {
        "brand": metrics.brand,
        "visible_seconds": metrics.visible_seconds,
        "visibility_pct": metrics.visibility_pct,
        "detection_count": metrics.detection_count,
        "avg_confidence": metrics.avg_confidence,
    }


def competitive_result_to_dict(result: CompetitiveResult) -> dict:
    return {
        "dominant_brand": result.dominant_brand,
        "coca_cola_seconds": result.coca_cola_seconds,
        "pepsi_seconds": result.pepsi_seconds,
        "coca_cola_pct": result.coca_cola_pct,
        "pepsi_pct": result.pepsi_pct,
        "visibility_gap_sec": result.visibility_gap_sec,
        "balance_label": result.balance_label,
    }


def build_metrics_payload(video_filename: str, duration_sec: float, brand_metrics: list[BrandMetrics], competitive: CompetitiveResult) -> dict:
    by_brand = {item.brand: brand_metrics_to_dict(item) for item in brand_metrics}
    empty = {
        "visible_seconds": 0.0,
        "visibility_pct": 0.0,
        "detection_count": 0,
        "avg_confidence": 0.0,
    }
    return {
        "client": "Coca-Cola",
        "competitor": "Pepsi",
        "video_filename": video_filename,
        "duration_sec": duration_sec,
        "coca_cola": by_brand.get(BRAND_COCA_COLA, {**empty, "brand": BRAND_COCA_COLA}),
        "pepsi": by_brand.get(BRAND_PEPSI, {**empty, "brand": BRAND_PEPSI}),
        "dominant_brand": competitive.dominant_brand,
        "visibility_gap_sec": competitive.visibility_gap_sec,
        "balance_label": competitive.balance_label,
    }

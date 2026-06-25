"""Export visibility metrics as JSON / text summaries (#9)."""

import argparse
import json
import sys
from pathlib import Path

from src.config import get_settings
from src.db.connection import get_db_session
from src.db import repository
from src.metrics import build_metrics_payload


def format_metrics_text(payload: dict) -> str:
    """Human-readable summary for CLI and reports."""
    coca = payload["coca_cola"]
    pepsi = payload["pepsi"]
    lines = [
        f"Video: {payload['video_filename']} ({payload['duration_sec']:.1f}s)",
        "",
        "Coca-Cola",
        f"  Visible: {coca['visible_seconds']:.2f}s ({coca['visibility_pct']:.1f}%)",
        f"  Detections: {coca['detection_count']} | Avg confidence: {coca['avg_confidence']:.2%}",
        "",
        "Pepsi",
        f"  Visible: {pepsi['visible_seconds']:.2f}s ({pepsi['visibility_pct']:.1f}%)",
        f"  Detections: {pepsi['detection_count']} | Avg confidence: {pepsi['avg_confidence']:.2%}",
        "",
        f"Dominant brand: {payload['dominant_brand']}",
        f"Balance: {payload['balance_label']} (gap {payload['visibility_gap_sec']:.2f}s)",
    ]
    return "\n".join(lines)


def export_metrics_files(payload: dict, video_id: int, output_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``metrics_{id}.json`` and ``metrics_{id}.txt`` under outputs dir."""
    settings = get_settings()
    settings.ensure_dirs()
    out_dir = output_dir or settings.outputs_dir
    json_path = out_dir / f"metrics_{video_id}.json"
    text_path = out_dir / f"metrics_{video_id}.txt"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    text_path.write_text(format_metrics_text(payload) + "\n", encoding="utf-8")
    return json_path, text_path


def load_metrics_payload_from_db(session, video_id: int) -> dict:
    """Rebuild metrics payload from ``brand_summary`` + ``competitive_analysis`` tables."""
    video = repository.get_video(session, video_id)
    if video is None:
        raise ValueError(f"Video {video_id} not found")

    summaries = repository.get_brand_summaries(session, video_id)
    competitive = repository.get_competitive_analysis(session, video_id)
    if competitive is None:
        raise ValueError(f"No competitive_analysis row for video {video_id}")

    from src.metrics import BrandMetrics, CompetitiveResult

    brand_metrics = [
        BrandMetrics(
            brand=s.brand,
            visible_seconds=s.visible_seconds,
            visibility_pct=s.visibility_pct,
            detection_count=s.detection_count,
            avg_confidence=s.avg_confidence or 0.0,
        )
        for s in summaries
    ]
    comp = CompetitiveResult(
        dominant_brand=competitive.dominant_brand,
        coca_cola_seconds=competitive.coca_cola_seconds,
        pepsi_seconds=competitive.pepsi_seconds,
        coca_cola_pct=competitive.coca_cola_pct,
        pepsi_pct=competitive.pepsi_pct,
        visibility_gap_sec=competitive.visibility_gap_sec,
        balance_label=competitive.balance_label,
    )
    return build_metrics_payload(video.filename, video.duration_sec, brand_metrics, comp)


def main() -> int:
    parser = argparse.ArgumentParser(description="Show or export visibility metrics (#9).")
    parser.add_argument("--video-id", type=int, help="Load metrics from Supabase for this video id")
    parser.add_argument("--export", action="store_true", help="Write JSON + text files to data/outputs/")
    args = parser.parse_args()

    if args.video_id is None:
        print("ERROR: pass --video-id <id> (run detect_video or pipeline first).", file=sys.stderr)
        return 1

    try:
        with get_db_session() as session:
            payload = load_metrics_payload_from_db(session, args.video_id)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(format_metrics_text(payload))
    if args.export:
        json_path, text_path = export_metrics_files(payload, args.video_id)
        print(f"\nExported: {json_path}\n          {text_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

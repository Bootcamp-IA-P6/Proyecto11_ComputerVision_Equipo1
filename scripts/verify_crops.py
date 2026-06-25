"""Verify bbox crops on disk match Supabase ``detections.crop_path`` (#10)."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.crops import resolve_crop_path
from src.db.connection import get_db_session
from src.db import repository


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify detection crops for a video id.")
    parser.add_argument("--video-id", type=int, required=True)
    parser.add_argument("--limit", type=int, default=20, help="Max detections to print")
    args = parser.parse_args()

    with get_db_session() as session:
        video = repository.get_video(session, args.video_id)
        if video is None:
            print(f"ERROR: video {args.video_id} not found", file=sys.stderr)
            return 1
        detections = repository.get_detections(session, args.video_id)
        filename = video.filename
        rows = [
            {
                "frame_number": d.frame_number,
                "brand": d.brand,
                "crop_path": d.crop_path,
            }
            for d in detections
        ]

    if not rows:
        print(f"No detections for video_id={args.video_id}")
        return 1

    with_crop = [d for d in rows if d["crop_path"]]
    readable = [d for d in with_crop if resolve_crop_path(d["crop_path"])]
    print(f"Video #{args.video_id} — {filename}")
    print(f"Detections: {len(rows)} | crop_path set: {len(with_crop)} | files on disk: {len(readable)}")

    for det in rows[: args.limit]:
        path = resolve_crop_path(det["crop_path"])
        status = str(path) if path else (det["crop_path"] or "—")
        print(f"  frame {det['frame_number']:5d}  {det['brand']:10s}  {status}")

    if len(readable) == 0:
        print("ERROR: no readable crop files", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

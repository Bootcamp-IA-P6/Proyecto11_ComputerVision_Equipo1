"""Extract frames from demo videos for Roboflow labeling.

Usage:
    # Every 1 second (default)
    python scripts/extract_video_frames.py

    # Every 15 frames
    python scripts/extract_video_frames.py --every-n-frames 15

    # Every 2 seconds, one video
    python scripts/extract_video_frames.py --every-seconds 2 --video data/demo/demo1.mp4
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parent.parent
DEMO_DIR = ROOT / "data" / "demo"
FRAMES_DIR = ROOT / "data" / "frames"
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"}


def extract_frames(
    video_path: Path,
    output_dir: Path,
    *,
    every_n_frames: int | None,
    every_seconds: float | None,
) -> int:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    if every_n_frames is not None:
        step = max(1, every_n_frames)
    else:
        step = max(1, int(round(fps * every_seconds)))

    output_dir.mkdir(parents=True, exist_ok=True)
    saved = 0
    frame_idx = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if frame_idx % step == 0:
            out = output_dir / f"frame_{saved:06d}.jpg"
            cv2.imwrite(str(out), frame)
            saved += 1
        frame_idx += 1

    cap.release()
    return saved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract frames from videos in data/demo/")
    parser.add_argument(
        "--video",
        type=Path,
        default=None,
        help="Single video path (default: all videos in data/demo/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=FRAMES_DIR,
        help=f"Base output directory (default: {FRAMES_DIR})",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--every-n-frames",
        type=int,
        default=None,
        metavar="N",
        help="Save every Nth frame (e.g. 15)",
    )
    group.add_argument(
        "--every-seconds",
        type=float,
        default=None,
        metavar="X",
        help="Save one frame every X seconds (default: 1.0 if neither flag is set)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    every_n_frames = args.every_n_frames
    every_seconds = args.every_seconds if args.every_seconds is not None else (None if every_n_frames else 1.0)

    if args.video is not None:
        videos = [args.video]
    else:
        videos = sorted(
            p for p in DEMO_DIR.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS
        )

    if not videos:
        print(f"No videos found in {DEMO_DIR} (or at --video path).", file=sys.stderr)
        return 1

    total = 0
    for video_path in videos:
        if not video_path.exists():
            print(f"Skip missing file: {video_path}", file=sys.stderr)
            continue
        out_dir = args.output_dir / video_path.stem
        count = extract_frames(
            video_path,
            out_dir,
            every_n_frames=every_n_frames,
            every_seconds=every_seconds,
        )
        total += count
        mode = (
            f"every {every_n_frames} frames"
            if every_n_frames is not None
            else f"every {every_seconds}s"
        )
        print(f"{video_path.name}: {count} frames -> {out_dir} ({mode})")

    print(f"\nDone: {total} frames in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

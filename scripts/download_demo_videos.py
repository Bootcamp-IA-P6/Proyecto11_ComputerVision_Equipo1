"""Download BrandSight demo videos using yt-dlp.

Usage:
    python scripts/download_demo_videos.py

Requires yt-dlp:
    pip install yt-dlp
"""
import subprocess
import sys
from pathlib import Path

VIDEOS = [
    {
        "url": "https://www.youtube.com/watch?v=gI0mj2zATLA",
        "output": "demo1.mp4",
        "duration": "45s",
    },
    {
        "url": "https://www.youtube.com/watch?v=oWOG6PTs75s",
        "output": "demo2.mp4",
        "duration": "29s",
    },
    {
        "url": "https://www.youtube.com/watch?v=ekaHlWga5yA",
        "output": "demo3.mp4",
        "duration": "36s",
    },
    {
        "url": "https://www.youtube.com/watch?v=_sugeMMyKPY",
        "output": "demo4.mp4",
        "duration": "62s",
    },
]

DEMO_DIR = Path(__file__).resolve().parent.parent / "data" / "demo"


def download_video(url: str, output: Path) -> bool:
    if output.exists():
        print(f"  Already exists, skipping: {output.name}")
        return True
    print(f"  Downloading {output.name} ...")
    result = subprocess.run(
        [
            "yt-dlp",
            "-f", "best[ext=mp4][height<=720]",
            "-o", str(output),
            url,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"  Done: {output.name}")
        return True
    else:
        print(f"  ERROR: {result.stderr.strip()}")
        return False


def main() -> int:
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Demo directory: {DEMO_DIR}\n")

    ok = 0
    for video in VIDEOS:
        output = DEMO_DIR / video["output"]
        print(f"[{video['output']}] {video['duration']} — {video['url']}")
        if download_video(video["url"], output):
            ok += 1

    print(f"\n{ok}/{len(VIDEOS)} videos ready in {DEMO_DIR}")
    return 0 if ok == len(VIDEOS) else 1


if __name__ == "__main__":
    raise SystemExit(main())

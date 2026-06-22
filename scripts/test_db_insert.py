"""CLI: round-trip insert test for ``videos`` table (ISSUE-04).

Usage:
    python -m scripts.test_db_insert

Inserts a test row, reads it back, then deletes it (no leftover data).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import get_settings
from src.db.connection import check_connection, verify_schema
from src.db.connection import get_db_session
from src.db import repository

TEST_FILENAME = "__brandsight_db_test__.mp4"


def main() -> int:
    try:
        check_connection()
    except Exception as exc:
        print(f"ERROR: Connection failed — {exc}", file=sys.stderr)
        return 1

    missing = verify_schema()
    if missing:
        print(f"ERROR: Missing tables: {', '.join(missing)}", file=sys.stderr)
        return 1

    settings = get_settings()
    storage = settings.uploads_dir / TEST_FILENAME

    video_id: int | None = None
    try:
        with get_db_session() as session:
            video = repository.create_video(
                session,
                filename=TEST_FILENAME,
                storage_path=storage,
                duration_sec=1.0,
                fps=30.0,
                total_frames=30,
                status="test",
            )
            video_id = video.id

        with get_db_session() as session:
            loaded = repository.get_video(session, video_id)
            if loaded is None:
                print(f"ERROR: Inserted video id={video_id} not found on read-back", file=sys.stderr)
                return 1
            if loaded.filename != TEST_FILENAME:
                print("ERROR: Read-back filename mismatch", file=sys.stderr)
                return 1
            if loaded.storage_path != str(storage):
                print("ERROR: Read-back storage_path mismatch", file=sys.stderr)
                return 1

        print(f"Insert OK — videos.id={video_id}")
        print(f"  filename: {TEST_FILENAME}")
        print(f"  storage_path: {storage}")
        return 0
    finally:
        if video_id is not None:
            with get_db_session() as session:
                if repository.delete_video(session, video_id):
                    print(f"Cleanup OK — deleted test video id={video_id}")


if __name__ == "__main__":
    raise SystemExit(main())

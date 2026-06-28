"""Verify Supabase Storage bucket access for crop uploads."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import get_settings
from src.supabase_storage import storage_configured, verify_storage_bucket


def main() -> int:
    settings = get_settings()
    if not storage_configured():
        print(
            "ERROR: set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env",
            file=sys.stderr,
        )
        return 1

    try:
        verify_storage_bucket()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"OK: Storage bucket '{settings.storage_bucket}' is available")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

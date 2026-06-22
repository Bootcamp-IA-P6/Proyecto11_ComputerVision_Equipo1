"""CLI: verify Supabase connection and BrandSight schema (ISSUE-03)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.db.connection import EXPECTED_TABLES, check_connection, verify_schema


def main() -> int:
    try:
        check_connection()
        print("Connection OK")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: Could not connect — {exc}", file=sys.stderr)
        return 1

    missing = verify_schema()
    if missing:
        print("Schema check FAILED — missing tables:", ", ".join(missing), file=sys.stderr)
        print(f"Expected: {', '.join(EXPECTED_TABLES)}", file=sys.stderr)
        print("Run sql/schema.sql in Supabase SQL Editor (see docs/SUPABASE_SETUP.md).", file=sys.stderr)
        return 1

    print(f"Schema OK — {len(EXPECTED_TABLES)} tables: {', '.join(EXPECTED_TABLES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

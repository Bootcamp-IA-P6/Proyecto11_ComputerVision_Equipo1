"""Pre-deploy smoke checks — env, model, Supabase (#13). Never prints secret values."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import get_settings
from src.db.connection import check_connection, verify_schema

REQUIRED_ENV = ("DATABASE_URL",)
OPTIONAL_ENV = ("GEMINI_API_KEY", "OPENAI_API_KEY")


def main() -> int:
    import os

    settings = get_settings()
    errors: list[str] = []
    warnings: list[str] = []

    for key in REQUIRED_ENV:
        if not os.environ.get(key) and not getattr(settings, key.lower(), ""):
            errors.append(f"Missing required env: {key}")

    for key in OPTIONAL_ENV:
        if not os.environ.get(key) and not getattr(settings, key.lower(), ""):
            warnings.append(f"Optional env not set: {key} (AI report will use template fallback)")

    if not settings.model_path.exists():
        errors.append(f"Model weights not found: {settings.model_path}")

    if errors:
        for msg in errors:
            print(f"ERROR: {msg}", file=sys.stderr)
        return 1

    try:
        check_connection()
        print("OK: Supabase connection")
    except Exception as exc:
        print(f"ERROR: Database connection failed ({type(exc).__name__})", file=sys.stderr)
        return 1

    missing = verify_schema()
    if missing:
        print(f"ERROR: Missing tables: {', '.join(missing)}", file=sys.stderr)
        return 1
    print("OK: Schema (5 tables)")

    for msg in warnings:
        print(f"WARN: {msg}")

    print("OK: smoke_deploy passed — ready for Streamlit Cloud")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""CLI entry: python -m scripts.check_db"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.db.connection import check_connection


def main() -> None:
    check_connection()
    print("Supabase connection OK")


if __name__ == "__main__":
    main()

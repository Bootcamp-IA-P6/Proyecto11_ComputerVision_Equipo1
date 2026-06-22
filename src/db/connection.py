"""Supabase PostgreSQL connection — engine, sessions, and schema checks."""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import get_settings

EXPECTED_TABLES: tuple[str, ...] = (
    "videos",
    "detections",
    "brand_summary",
    "competitive_analysis",
    "marketing_reports",
)

_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def _normalize_database_url(url: str) -> str:
    if url.startswith("postgresql://") and "+psycopg2" not in url:
        return url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url


def get_engine() -> Engine:
    """Return a cached SQLAlchemy engine (reads ``DATABASE_URL`` from settings)."""
    global _engine, _SessionLocal
    if _engine is None:
        settings = get_settings()
        if not settings.database_url:
            raise ValueError(
                "DATABASE_URL is not set. Copy .env.example to .env and add your Supabase connection string."
            )
        _engine = create_engine(
            _normalize_database_url(settings.database_url),
            pool_pre_ping=True,
        )
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    get_engine()
    assert _SessionLocal is not None
    return _SessionLocal


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager: commit on success, rollback on error, always close."""
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def check_connection() -> bool:
    with get_engine().connect() as conn:
        conn.execute(text("SELECT 1"))
    return True


def verify_schema() -> list[str]:
    """Return public table names from EXPECTED_TABLES that are missing."""
    missing: list[str] = []
    with get_engine().connect() as conn:
        for table in EXPECTED_TABLES:
            row = conn.execute(
                text(
                    "SELECT 1 FROM information_schema.tables "
                    "WHERE table_schema = 'public' AND table_name = :name"
                ),
                {"name": table},
            ).fetchone()
            if row is None:
                missing.append(table)
    return missing

"""Load Streamlit Cloud secrets into ``os.environ`` for pydantic-settings (#13)."""

from __future__ import annotations

import os

_SECRET_KEYS = (
    "DATABASE_URL",
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY",
    "GEMINI_API_KEY",
    "OPENAI_API_KEY",
    "MODEL_PATH",
    "CONFIDENCE_THRESHOLD",
    "SAMPLE_STRIDE",
)


def inject_secrets() -> None:
    """Map ``st.secrets`` → environment variables (no-op outside Streamlit)."""
    try:
        import streamlit as st
    except ImportError:
        return

    try:
        secrets = st.secrets
    except Exception:
        return

    for key in _SECRET_KEYS:
        if key in secrets:
            os.environ.setdefault(key, str(secrets[key]))

    nested = secrets.get("env")
    if isinstance(nested, dict):
        for key, value in nested.items():
            os.environ.setdefault(str(key).upper(), str(value))


def redact_secrets(message: str, *values: str) -> str:
    """Replace secret substrings before showing errors in the UI."""
    redacted = message
    for value in values:
        if value and len(value) > 4:
            redacted = redacted.replace(value, "***")
    return redacted

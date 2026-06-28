"""Supabase Storage helpers for bbox crop images."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING

from src.config import get_settings

if TYPE_CHECKING:
    from supabase import Client

STORAGE_URI_PREFIX = "storage:"


def storage_configured() -> bool:
    settings = get_settings()
    return bool(settings.supabase_url and settings.supabase_service_role_key)


@lru_cache(maxsize=1)
def get_storage_client() -> Client:
    from supabase import create_client

    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required for crop uploads."
        )
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


def make_storage_uri(bucket: str, object_key: str) -> str:
    return f"{STORAGE_URI_PREFIX}{bucket}/{object_key.lstrip('/')}"


def parse_storage_uri(uri: str) -> tuple[str, str] | None:
    if not uri.startswith(STORAGE_URI_PREFIX):
        return None
    rest = uri[len(STORAGE_URI_PREFIX) :]
    if "/" not in rest:
        return None
    bucket, object_key = rest.split("/", 1)
    if not bucket or not object_key:
        return None
    return bucket, object_key


def upload_storage_file(local_path: Path, object_key: str, *, content_type: str) -> str:
    """Upload a file and return the ``storage:`` URI."""
    settings = get_settings()
    bucket = settings.storage_bucket
    client = get_storage_client()

    with local_path.open("rb") as handle:
        client.storage.from_(bucket).upload(
            object_key,
            handle,
            file_options={"content-type": content_type, "upsert": "true"},
        )

    return make_storage_uri(bucket, object_key)


def upload_crop_file(local_path: Path, object_key: str) -> str:
    """Upload a crop JPEG and return the ``storage:`` URI stored in ``crop_path``."""
    return upload_storage_file(local_path, object_key, content_type="image/jpeg")


def create_signed_crop_url(bucket: str, object_key: str, *, expires_in: int | None = None) -> str | None:
    settings = get_settings()
    ttl = expires_in if expires_in is not None else settings.crop_signed_url_seconds
    client = get_storage_client()
    result = client.storage.from_(bucket).create_signed_url(object_key, ttl)
    if isinstance(result, dict):
        return result.get("signedURL") or result.get("signedUrl")
    signed_url = getattr(result, "signed_url", None) or getattr(result, "signedURL", None)
    return str(signed_url) if signed_url else None


def crop_object_key(video_id: int, brand: str, index: int) -> str:
    return f"{video_id}/{brand}_{index}.jpg"


def annotated_object_key(video_id: int) -> str:
    return f"{video_id}/annotated.mp4"


def _bucket_names(buckets: list) -> set[str]:
    names: set[str] = set()
    for bucket in buckets:
        if isinstance(bucket, dict):
            for key in ("name", "id"):
                value = bucket.get(key)
                if value:
                    names.add(str(value))
        else:
            for attr in ("name", "id"):
                value = getattr(bucket, attr, None)
                if value:
                    names.add(str(value))
    return names


def verify_storage_bucket() -> None:
    """Raise if the configured bucket is missing."""
    settings = get_settings()
    client = get_storage_client()
    buckets = client.storage.list_buckets()
    names = _bucket_names(buckets)
    if settings.storage_bucket not in names:
        raise RuntimeError(
            f"Storage bucket '{settings.storage_bucket}' not found. Run sql/storage.sql in Supabase."
        )

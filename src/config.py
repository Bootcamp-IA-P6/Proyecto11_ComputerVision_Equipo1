from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BRAND_COCA_COLA = "coca_cola"
BRAND_PEPSI = "pepsi"
BRAND_LABELS = {0: BRAND_COCA_COLA, 1: BRAND_PEPSI}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=("settings_",),
    )

    database_url: str = ""
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    gemini_api_key: str = ""
    openai_api_key: str = ""
    model_path: Path = PROJECT_ROOT / "models" / "best.pt"
    confidence_threshold: float = 0.5
    sample_stride: int = 3
    crops_dir: Path = PROJECT_ROOT / "data" / "crops"
    uploads_dir: Path = PROJECT_ROOT / "data" / "uploads"
    outputs_dir: Path = PROJECT_ROOT / "data" / "outputs"

    def ensure_dirs(self) -> None:
        self.crops_dir.mkdir(parents=True, exist_ok=True)
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    return Settings()

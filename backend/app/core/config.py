from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "FaceRoom AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/faceroom"
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_BUCKET: str = "event-photos"

    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION: str = "face_embeddings"

    REDIS_URL: str = "redis://localhost:6379/0"

    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    FACE_SIMILARITY_THRESHOLD: float = 0.5
    DBSCAN_EPS: float = 0.45
    DBSCAN_MIN_SAMPLES: int = 2
    MAX_UPLOAD_SIZE_MB: int = 20
    ALLOWED_IMAGE_TYPES: str = "image/jpeg,image/png,image/jpg"

    RATE_LIMIT: str = "100/minute"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def allowed_mime_types(self) -> List[str]:
        return [t.strip() for t in self.ALLOWED_IMAGE_TYPES.split(",") if t.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

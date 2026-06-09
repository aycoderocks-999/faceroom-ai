import uuid
from pathlib import Path

from supabase import Client, create_client

from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

UPLOAD_ROOT = Path(__file__).resolve().parents[2] / "uploads"


class StorageService:
    def __init__(self):
        self._client: Client | None = None
        self._use_local = not (settings.SUPABASE_URL and settings.SUPABASE_KEY)
        if self._use_local:
            UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
            logger.info("Using local file storage at %s", UPLOAD_ROOT)

    @property
    def client(self) -> Client:
        if self._client is None:
            if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
                raise RuntimeError("Supabase credentials not configured")
            self._client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return self._client

    def _local_path(self, storage_path: str) -> Path:
        return UPLOAD_ROOT / storage_path

    def upload_image(self, file_bytes: bytes, filename: str, room_id: int, content_type: str) -> tuple[str, str]:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "jpg"
        storage_path = f"rooms/{room_id}/{uuid.uuid4()}.{ext}"

        if self._use_local:
            dest = self._local_path(storage_path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(file_bytes)
            public_url = f"/api/v1/files/{storage_path}"
            logger.info("Uploaded image locally to %s", storage_path)
            return public_url, storage_path

        self.client.storage.from_(settings.SUPABASE_BUCKET).upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": content_type, "upsert": "false"},
        )
        public_url = self.client.storage.from_(settings.SUPABASE_BUCKET).get_public_url(storage_path)
        logger.info("Uploaded image to %s", storage_path)
        return public_url, storage_path

    def download_image(self, storage_path: str) -> bytes:
        if self._use_local:
            return self._local_path(storage_path).read_bytes()
        return self.client.storage.from_(settings.SUPABASE_BUCKET).download(storage_path)

    def upload_face_crop(self, crop_bytes: bytes, room_id: int, image_id: int, face_index: int) -> str:
        storage_path = f"rooms/{room_id}/faces/{image_id}_{face_index}.jpg"

        if self._use_local:
            dest = self._local_path(storage_path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(crop_bytes)
            return f"/api/v1/files/{storage_path}"

        self.client.storage.from_(settings.SUPABASE_BUCKET).upload(
            path=storage_path,
            file=crop_bytes,
            file_options={"content-type": "image/jpeg", "upsert": "true"},
        )
        return self.client.storage.from_(settings.SUPABASE_BUCKET).get_public_url(storage_path)

    def delete_image(self, storage_path: str) -> None:
        if self._use_local:
            path = self._local_path(storage_path)
            if path.exists():
                path.unlink()
            return
        self.client.storage.from_(settings.SUPABASE_BUCKET).remove([storage_path])


def get_storage_service() -> StorageService:
    return StorageService()

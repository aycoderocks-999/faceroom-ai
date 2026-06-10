from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.repositories.image_repository import ImageRepository
from app.repositories.room_repository import RoomRepository
from app.schemas.image import ImageResponse, ImageUploadResponse
from app.services.storage_service import StorageService

settings = get_settings()


class ImageService:
    def __init__(self, db: Session, storage: StorageService | None = None):
        self.db = db
        self.repo = ImageRepository(db)
        self.room_repo = RoomRepository(db)
        self.storage = storage or StorageService()

    @staticmethod
    def _detect_image_type(header: bytes) -> str | None:
        """Return 'jpeg' or 'png' by inspecting magic bytes. No stdlib imghdr needed."""
        if header[:3] == b"\xff\xd8\xff":
            return "jpeg"
        if header[:8] == b"\x89PNG\r\n\x1a\n":
            return "png"
        return None

    def _validate_file(self, file: UploadFile, content: bytes) -> None:
        if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit",
            )
        img_type = self._detect_image_type(content[:8])
        if img_type not in ("jpeg", "png"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image format. Only JPEG and PNG are accepted.")
        if file.content_type and file.content_type not in settings.allowed_mime_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid content type")

    def _to_response(self, image) -> ImageResponse:
        return ImageResponse(
            id=image.id,
            room_id=image.room_id,
            uploader_id=image.uploader_id,
            image_url=image.image_url,
            filename=image.filename,
            processing_status=image.processing_status.value,
            upload_time=image.upload_time,
            face_count=self.repo.get_face_count(image.id),
        )

    async def upload_images(
        self, room_id: int, user_id: int, files: list[UploadFile]
    ) -> ImageUploadResponse:
        if not self.room_repo.is_member(room_id, user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a room member")
        if not files:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No files provided")

        uploaded: list[ImageResponse] = []
        task_ids: list[str] = []

        from app.workers.tasks import process_image_task

        for file in files:
            content = await file.read()
            self._validate_file(file, content)
            filename = file.filename or "upload.jpg"
            content_type = file.content_type or "image/jpeg"

            image_url, storage_path = self.storage.upload_image(content, filename, room_id, content_type)

            image = self.repo.create(room_id, user_id, image_url, storage_path, filename)
            uploaded.append(self._to_response(image))

            try:
                result = process_image_task.delay(image.id)
                task_ids.append(result.id)
            except Exception:
                task_ids.append("queued-offline")

        return ImageUploadResponse(uploaded=uploaded, task_ids=task_ids)

    def get_image(self, image_id: int, user_id: int) -> ImageResponse:
        image = self.repo.get_by_id(image_id)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
        if not self.room_repo.is_member(image.room_id, user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a room member")
        return self._to_response(image)

    def get_room_images(self, room_id: int, user_id: int, page: int = 1, page_size: int = 20) -> dict:
        if not self.room_repo.is_member(room_id, user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a room member")
        images, total = self.repo.get_room_images(room_id, page, page_size)
        pages = (total + page_size - 1) // page_size if page_size else 0
        return {
            "items": [self._to_response(img) for img in images],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }

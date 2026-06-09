from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.face import Face
from app.models.image import Image, ProcessingStatus


class ImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        room_id: int,
        uploader_id: int,
        image_url: str,
        storage_path: str,
        filename: str,
    ) -> Image:
        image = Image(
            room_id=room_id,
            uploader_id=uploader_id,
            image_url=image_url,
            storage_path=storage_path,
            filename=filename,
            processing_status=ProcessingStatus.PENDING,
        )
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    def get_by_id(self, image_id: int) -> Image | None:
        return self.db.query(Image).filter(Image.id == image_id).first()

    def get_room_images(self, room_id: int, page: int = 1, page_size: int = 20) -> tuple[list[Image], int]:
        query = self.db.query(Image).filter(Image.room_id == room_id).order_by(Image.upload_time.desc())
        total = query.count()
        images = query.offset((page - 1) * page_size).limit(page_size).all()
        return images, total

    def get_face_count(self, image_id: int) -> int:
        return self.db.query(func.count(Face.id)).filter(Face.image_id == image_id).scalar() or 0

    def update_status(self, image_id: int, status: ProcessingStatus) -> None:
        image = self.get_by_id(image_id)
        if image:
            image.processing_status = status
            self.db.commit()

    def get_recent_uploads(self, room_ids: list[int], limit: int = 10) -> list[Image]:
        if not room_ids:
            return []
        return (
            self.db.query(Image)
            .filter(Image.room_id.in_(room_ids))
            .order_by(Image.upload_time.desc())
            .limit(limit)
            .all()
        )

    def count_by_rooms(self, room_ids: list[int]) -> int:
        if not room_ids:
            return 0
        return self.db.query(func.count(Image.id)).filter(Image.room_id.in_(room_ids)).scalar() or 0

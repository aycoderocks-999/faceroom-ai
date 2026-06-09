from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False, index=True)
    uploader_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    processing_status: Mapped[ProcessingStatus] = mapped_column(
        SAEnum(ProcessingStatus), default=ProcessingStatus.PENDING, nullable=False
    )
    upload_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    room = relationship("Room", back_populates="images")
    uploader = relationship("User", back_populates="uploaded_images")
    faces = relationship("Face", back_populates="image", cascade="all, delete-orphan")

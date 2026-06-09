from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class FaceCluster(Base):
    __tablename__ = "face_clusters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), default="Unknown Person", nullable=False)
    representative_face_id: Mapped[int | None] = mapped_column(ForeignKey("faces.id"), nullable=True)
    representative_face_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    room = relationship("Room", back_populates="clusters")
    faces = relationship("Face", back_populates="cluster", foreign_keys="Face.cluster_id")
    representative_face = relationship("Face", foreign_keys=[representative_face_id], post_update=True)

from sqlalchemy import Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Face(Base):
    __tablename__ = "faces"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    image_id: Mapped[int] = mapped_column(ForeignKey("images.id"), nullable=False, index=True)
    embedding_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    cluster_id: Mapped[int | None] = mapped_column(ForeignKey("face_clusters.id"), nullable=True, index=True)
    bounding_box: Mapped[dict] = mapped_column(JSON, nullable=False)
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    crop_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    image = relationship("Image", back_populates="faces")
    cluster = relationship("FaceCluster", back_populates="faces", foreign_keys=[cluster_id])

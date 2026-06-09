from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SearchLog(Base):
    __tablename__ = "search_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False, index=True)
    latency_ms: Mapped[float] = mapped_column(Float, nullable=False)
    result_count: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="search_logs")

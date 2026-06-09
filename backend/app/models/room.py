from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_name: Mapped[str] = mapped_column(String(200), nullable=False)
    room_code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="owned_rooms")
    members = relationship("RoomMember", back_populates="room", cascade="all, delete-orphan")
    images = relationship("Image", back_populates="room", cascade="all, delete-orphan")
    clusters = relationship("FaceCluster", back_populates="room", cascade="all, delete-orphan")


class RoomMember(Base):
    __tablename__ = "room_members"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    room = relationship("Room", back_populates="members")
    user = relationship("User", back_populates="room_memberships")

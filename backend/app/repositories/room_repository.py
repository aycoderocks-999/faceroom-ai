import secrets
import string

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.face_cluster import FaceCluster
from app.models.image import Image
from app.models.room import Room, RoomMember


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def generate_room_code(self) -> str:
        chars = string.ascii_uppercase + string.digits
        while True:
            suffix = "".join(secrets.choice(chars) for _ in range(6))
            code = f"ROOM-{suffix}"
            if not self.get_by_code(code):
                return code

    def create(self, room_name: str, owner_id: int) -> Room:
        room = Room(room_name=room_name, room_code=self.generate_room_code(), owner_id=owner_id)
        self.db.add(room)
        self.db.flush()
        self.db.add(RoomMember(room_id=room.id, user_id=owner_id))
        self.db.commit()
        self.db.refresh(room)
        return room

    def get_by_id(self, room_id: int) -> Room | None:
        return self.db.query(Room).filter(Room.id == room_id).first()

    def get_by_code(self, room_code: str) -> Room | None:
        return self.db.query(Room).filter(Room.room_code == room_code.upper()).first()

    def is_member(self, room_id: int, user_id: int) -> bool:
        return (
            self.db.query(RoomMember)
            .filter(RoomMember.room_id == room_id, RoomMember.user_id == user_id)
            .first()
            is not None
        )

    def add_member(self, room_id: int, user_id: int) -> RoomMember:
        member = RoomMember(room_id=room_id, user_id=user_id)
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def remove_member(self, room_id: int, user_id: int) -> bool:
        member = (
            self.db.query(RoomMember)
            .filter(RoomMember.room_id == room_id, RoomMember.user_id == user_id)
            .first()
        )
        if not member:
            return False
        self.db.delete(member)
        self.db.commit()
        return True

    def get_user_rooms(self, user_id: int) -> list[Room]:
        return (
            self.db.query(Room)
            .join(RoomMember, RoomMember.room_id == Room.id)
            .filter(RoomMember.user_id == user_id)
            .order_by(Room.created_at.desc())
            .all()
        )

    def get_member_count(self, room_id: int) -> int:
        return self.db.query(func.count(RoomMember.id)).filter(RoomMember.room_id == room_id).scalar() or 0

    def get_image_count(self, room_id: int) -> int:
        return self.db.query(func.count(Image.id)).filter(Image.room_id == room_id).scalar() or 0

    def get_cluster_count(self, room_id: int) -> int:
        return self.db.query(func.count(FaceCluster.id)).filter(FaceCluster.room_id == room_id).scalar() or 0

    def delete(self, room: Room) -> None:
        self.db.delete(room)
        self.db.commit()

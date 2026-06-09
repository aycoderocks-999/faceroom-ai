from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.room_repository import RoomRepository
from app.schemas.room import RoomCreateRequest, RoomJoinRequest, RoomResponse


class RoomService:
    def __init__(self, db: Session):
        self.repo = RoomRepository(db)

    def _to_response(self, room) -> RoomResponse:
        return RoomResponse(
            id=room.id,
            room_name=room.room_name,
            room_code=room.room_code,
            owner_id=room.owner_id,
            created_at=room.created_at,
            member_count=self.repo.get_member_count(room.id),
            image_count=self.repo.get_image_count(room.id),
            cluster_count=self.repo.get_cluster_count(room.id),
        )

    def _ensure_member(self, room_id: int, user_id: int) -> None:
        if not self.repo.is_member(room_id, user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a room member")

    def create_room(self, user_id: int, data: RoomCreateRequest) -> RoomResponse:
        room = self.repo.create(data.room_name, user_id)
        return self._to_response(room)

    def join_room(self, user_id: int, data: RoomJoinRequest) -> RoomResponse:
        room = self.repo.get_by_code(data.room_code.upper())
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        if self.repo.is_member(room.id, user_id):
            return self._to_response(room)
        self.repo.add_member(room.id, user_id)
        return self._to_response(room)

    def leave_room(self, room_id: int, user_id: int) -> dict:
        room = self.repo.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        if room.owner_id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Owner cannot leave room. Delete the room instead.",
            )
        if not self.repo.remove_member(room_id, user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not a member")
        return {"message": "Left room successfully"}

    def get_user_rooms(self, user_id: int) -> list[RoomResponse]:
        rooms = self.repo.get_user_rooms(user_id)
        return [self._to_response(r) for r in rooms]

    def get_room(self, room_id: int, user_id: int) -> RoomResponse:
        room = self.repo.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        self._ensure_member(room_id, user_id)
        return self._to_response(room)

    def delete_room(self, room_id: int, user_id: int) -> dict:
        room = self.repo.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        if room.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can delete room")
        self.repo.delete(room)
        return {"message": "Room deleted successfully"}

    def ensure_member(self, room_id: int, user_id: int) -> None:
        self._ensure_member(room_id, user_id)

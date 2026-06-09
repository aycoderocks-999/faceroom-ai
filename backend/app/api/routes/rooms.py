from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.room import RoomCreateRequest, RoomJoinRequest, RoomResponse
from app.services.image_service import ImageService
from app.services.room_service import RoomService

router = APIRouter()


@router.post("/create", response_model=RoomResponse, status_code=201)
def create_room(data: RoomCreateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return RoomService(db).create_room(current_user.id, data)


@router.post("/join", response_model=RoomResponse)
def join_room(data: RoomJoinRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return RoomService(db).join_room(current_user.id, data)


@router.get("", response_model=list[RoomResponse])
def list_rooms(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return RoomService(db).get_user_rooms(current_user.id)


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return RoomService(db).get_room(room_id, current_user.id)


@router.delete("/{room_id}")
def delete_room(room_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return RoomService(db).delete_room(room_id, current_user.id)


@router.post("/{room_id}/leave")
def leave_room(room_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return RoomService(db).leave_room(room_id, current_user.id)


@router.get("/{room_id}/images")
def get_room_images(
    room_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ImageService(db).get_room_images(room_id, current_user.id, page, page_size)


@router.get("/{room_id}/clusters")
def get_room_clusters_alias(
    room_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    from app.services.cluster_service import ClusterService

    return ClusterService(db).get_room_clusters(room_id, current_user.id)

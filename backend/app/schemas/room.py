from datetime import datetime

from pydantic import BaseModel, Field


class RoomCreateRequest(BaseModel):
    room_name: str = Field(min_length=1, max_length=200)


class RoomJoinRequest(BaseModel):
    room_code: str = Field(min_length=5, max_length=20)


class RoomResponse(BaseModel):
    id: int
    room_name: str
    room_code: str
    owner_id: int
    created_at: datetime
    member_count: int = 0
    image_count: int = 0
    cluster_count: int = 0

    model_config = {"from_attributes": True}

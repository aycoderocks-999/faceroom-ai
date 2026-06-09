from datetime import datetime

from pydantic import BaseModel


class ImageResponse(BaseModel):
    id: int
    room_id: int
    uploader_id: int
    image_url: str
    filename: str
    processing_status: str
    upload_time: datetime
    face_count: int = 0

    model_config = {"from_attributes": True}


class ImageUploadResponse(BaseModel):
    uploaded: list[ImageResponse]
    task_ids: list[str]

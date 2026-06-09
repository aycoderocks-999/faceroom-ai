from datetime import datetime

from pydantic import BaseModel, Field


class SearchMatch(BaseModel):
    image_id: int
    image_url: str
    similarity: float
    face_id: int | None = None


class FaceSearchResponse(BaseModel):
    matches: list[SearchMatch]
    match_count: int
    search_time_ms: float
    threshold: float


class SearchHistoryItem(BaseModel):
    id: int
    room_id: int
    latency_ms: float
    result_count: int
    timestamp: datetime

    model_config = {"from_attributes": True}


class SearchHistoryResponse(BaseModel):
    items: list[SearchHistoryItem]
    total: int

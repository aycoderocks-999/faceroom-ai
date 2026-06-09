from datetime import datetime

from pydantic import BaseModel, Field


class ClusterResponse(BaseModel):
    id: int
    room_id: int
    name: str
    representative_face_url: str | None
    face_count: int = 0
    image_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class ClusterMergeRequest(BaseModel):
    source_cluster_ids: list[int] = Field(min_length=2)
    target_name: str | None = None


class ClusterSplitRequest(BaseModel):
    cluster_id: int
    face_ids: list[int] = Field(min_length=1)
    new_name: str | None = None


class ClusterUpdateRequest(BaseModel):
    name: str | None = None
    mark_unknown: bool = False

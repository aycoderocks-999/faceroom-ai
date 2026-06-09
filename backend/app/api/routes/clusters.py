from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.cluster import ClusterMergeRequest, ClusterResponse, ClusterSplitRequest, ClusterUpdateRequest
from app.services.cluster_service import ClusterService

router = APIRouter()


@router.get("/rooms/{room_id}/clusters", response_model=list[ClusterResponse])
def get_room_clusters(
    room_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return ClusterService(db).get_room_clusters(room_id, current_user.id)


@router.get("/{cluster_id}", response_model=ClusterResponse)
def get_cluster(cluster_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ClusterService(db).get_cluster(cluster_id, current_user.id)


@router.get("/{cluster_id}/images")
def get_cluster_images(
    cluster_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ClusterService(db).get_cluster_images(cluster_id, current_user.id, page, page_size)


@router.post("/merge", response_model=ClusterResponse)
def merge_clusters(
    room_id: int,
    data: ClusterMergeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ClusterService(db).merge_clusters(room_id, current_user.id, data)


@router.post("/split", response_model=ClusterResponse)
def split_cluster(
    room_id: int,
    data: ClusterSplitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ClusterService(db).split_cluster(room_id, current_user.id, data)


@router.patch("/{cluster_id}", response_model=ClusterResponse)
def update_cluster(
    cluster_id: int,
    data: ClusterUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ClusterService(db).update_cluster(cluster_id, current_user.id, data)


@router.post("/rooms/{room_id}/recluster")
def recluster_room(
    room_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return ClusterService(db).recluster(room_id, current_user.id)

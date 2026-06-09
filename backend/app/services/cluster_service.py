from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.cluster_repository import ClusterRepository
from app.repositories.face_repository import FaceRepository
from app.repositories.image_repository import ImageRepository
from app.repositories.room_repository import RoomRepository
from app.schemas.cluster import ClusterMergeRequest, ClusterResponse, ClusterSplitRequest, ClusterUpdateRequest
from app.workers.tasks import recluster_room_task


class ClusterService:
    def __init__(self, db: Session):
        self.db = db
        self.cluster_repo = ClusterRepository(db)
        self.face_repo = FaceRepository(db)
        self.image_repo = ImageRepository(db)
        self.room_repo = RoomRepository(db)

    def _to_response(self, cluster) -> ClusterResponse:
        return ClusterResponse(
            id=cluster.id,
            room_id=cluster.room_id,
            name=cluster.name,
            representative_face_url=cluster.representative_face_url,
            face_count=self.cluster_repo.get_face_count(cluster.id),
            image_count=self.cluster_repo.get_image_count(cluster.id),
            created_at=cluster.created_at,
        )

    def _ensure_member(self, room_id: int, user_id: int) -> None:
        if not self.room_repo.is_member(room_id, user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a room member")

    def get_room_clusters(self, room_id: int, user_id: int) -> list[ClusterResponse]:
        self._ensure_member(room_id, user_id)
        clusters = self.cluster_repo.get_room_clusters(room_id)
        return [self._to_response(c) for c in clusters]

    def get_cluster(self, cluster_id: int, user_id: int) -> ClusterResponse:
        cluster = self.cluster_repo.get_by_id(cluster_id)
        if not cluster:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cluster not found")
        self._ensure_member(cluster.room_id, user_id)
        return self._to_response(cluster)

    def get_cluster_images(self, cluster_id: int, user_id: int, page: int = 1, page_size: int = 20) -> dict:
        cluster = self.cluster_repo.get_by_id(cluster_id)
        if not cluster:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cluster not found")
        self._ensure_member(cluster.room_id, user_id)

        image_ids = self.face_repo.get_cluster_image_ids(cluster_id)
        total = len(image_ids)
        start = (page - 1) * page_size
        page_ids = image_ids[start : start + page_size]

        items = []
        for img_id in page_ids:
            img = self.image_repo.get_by_id(img_id)
            if img:
                items.append(
                    {
                        "id": img.id,
                        "image_url": img.image_url,
                        "filename": img.filename,
                        "upload_time": img.upload_time,
                    }
                )

        pages = (total + page_size - 1) // page_size if page_size else 0
        return {"items": items, "total": total, "page": page, "page_size": page_size, "pages": pages}

    def merge_clusters(self, room_id: int, user_id: int, data: ClusterMergeRequest) -> ClusterResponse:
        self._ensure_member(room_id, user_id)
        clusters = [self.cluster_repo.get_by_id(cid) for cid in data.source_cluster_ids]
        if any(c is None or c.room_id != room_id for c in clusters):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid cluster IDs")

        target = self.cluster_repo.create(room_id, data.target_name or clusters[0].name)
        for cluster in clusters:
            faces = self.face_repo.get_cluster_faces(cluster.id)
            self.face_repo.bulk_update_cluster([f.id for f in faces], target.id)
            if cluster.id != target.id:
                self.cluster_repo.delete(cluster)

        self._update_representative(target.id)
        return self._to_response(self.cluster_repo.get_by_id(target.id))

    def split_cluster(self, room_id: int, user_id: int, data: ClusterSplitRequest) -> ClusterResponse:
        self._ensure_member(room_id, user_id)
        cluster = self.cluster_repo.get_by_id(data.cluster_id)
        if not cluster or cluster.room_id != room_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cluster not found")

        new_cluster = self.cluster_repo.create(room_id, data.new_name or "Unknown Person")
        self.face_repo.bulk_update_cluster(data.face_ids, new_cluster.id)
        self._update_representative(cluster.id)
        self._update_representative(new_cluster.id)
        return self._to_response(new_cluster)

    def update_cluster(self, cluster_id: int, user_id: int, data: ClusterUpdateRequest) -> ClusterResponse:
        cluster = self.cluster_repo.get_by_id(cluster_id)
        if not cluster:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cluster not found")
        self._ensure_member(cluster.room_id, user_id)

        updates = {}
        if data.name:
            updates["name"] = data.name
        if data.mark_unknown:
            updates["name"] = "Unknown Person"
        if updates:
            self.cluster_repo.update(cluster, **updates)
        return self._to_response(self.cluster_repo.get_by_id(cluster_id))

    def recluster(self, room_id: int, user_id: int) -> dict:
        self._ensure_member(room_id, user_id)
        task = recluster_room_task.delay(room_id)
        return {"message": "Re-clustering started", "task_id": task.id}

    def _update_representative(self, cluster_id: int) -> None:
        faces = self.face_repo.get_cluster_faces(cluster_id)
        if not faces:
            return
        best = max(faces, key=lambda f: f.quality_score or 0)
        cluster = self.cluster_repo.get_by_id(cluster_id)
        if cluster:
            self.cluster_repo.update(
                cluster,
                representative_face_id=best.id,
                representative_face_url=best.crop_url,
            )

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.face import Face
from app.models.face_cluster import FaceCluster


class ClusterRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, room_id: int, name: str = "Unknown Person") -> FaceCluster:
        cluster = FaceCluster(room_id=room_id, name=name)
        self.db.add(cluster)
        self.db.commit()
        self.db.refresh(cluster)
        return cluster

    def get_by_id(self, cluster_id: int) -> FaceCluster | None:
        return self.db.query(FaceCluster).filter(FaceCluster.id == cluster_id).first()

    def get_room_clusters(self, room_id: int) -> list[FaceCluster]:
        return (
            self.db.query(FaceCluster)
            .filter(FaceCluster.room_id == room_id)
            .order_by(FaceCluster.created_at.desc())
            .all()
        )

    def update(self, cluster: FaceCluster, **kwargs) -> FaceCluster:
        for key, value in kwargs.items():
            setattr(cluster, key, value)
        self.db.commit()
        self.db.refresh(cluster)
        return cluster

    def delete(self, cluster: FaceCluster) -> None:
        self.db.delete(cluster)
        self.db.commit()

    def count_by_room(self, room_id: int) -> int:
        return self.db.query(func.count(FaceCluster.id)).filter(FaceCluster.room_id == room_id).scalar() or 0

    def count_by_rooms(self, room_ids: list[int]) -> int:
        if not room_ids:
            return 0
        return self.db.query(func.count(FaceCluster.id)).filter(FaceCluster.room_id.in_(room_ids)).scalar() or 0

    def get_face_count(self, cluster_id: int) -> int:
        return self.db.query(func.count(Face.id)).filter(Face.cluster_id == cluster_id).scalar() or 0

    def get_image_count(self, cluster_id: int) -> int:
        return (
            self.db.query(func.count(func.distinct(Face.image_id)))
            .filter(Face.cluster_id == cluster_id)
            .scalar()
            or 0
        )

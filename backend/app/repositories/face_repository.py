from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.face import Face
from app.models.face_cluster import FaceCluster


class FaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        image_id: int,
        embedding_id: str,
        bounding_box: dict,
        cluster_id: int | None = None,
        quality_score: float | None = None,
        crop_url: str | None = None,
    ) -> Face:
        face = Face(
            image_id=image_id,
            embedding_id=embedding_id,
            bounding_box=bounding_box,
            cluster_id=cluster_id,
            quality_score=quality_score,
            crop_url=crop_url,
        )
        self.db.add(face)
        self.db.commit()
        self.db.refresh(face)
        return face

    def get_by_id(self, face_id: int) -> Face | None:
        return self.db.query(Face).filter(Face.id == face_id).first()

    def get_by_embedding_id(self, embedding_id: str) -> Face | None:
        return self.db.query(Face).filter(Face.embedding_id == embedding_id).first()

    def get_room_faces(self, room_id: int) -> list[Face]:
        from app.models.image import Image

        return (
            self.db.query(Face)
            .join(Image, Image.id == Face.image_id)
            .filter(Image.room_id == room_id)
            .all()
        )

    def get_cluster_faces(self, cluster_id: int) -> list[Face]:
        return self.db.query(Face).filter(Face.cluster_id == cluster_id).all()

    def update_cluster(self, face_id: int, cluster_id: int | None) -> None:
        face = self.get_by_id(face_id)
        if face:
            face.cluster_id = cluster_id
            self.db.commit()

    def bulk_update_cluster(self, face_ids: list[int], cluster_id: int | None) -> None:
        self.db.query(Face).filter(Face.id.in_(face_ids)).update(
            {Face.cluster_id: cluster_id}, synchronize_session=False
        )
        self.db.commit()

    def bulk_clear_cluster(self, face_ids: list[int]) -> None:
        """Set cluster_id to NULL for all given face IDs (used before re-clustering)."""
        if face_ids:
            self.db.query(Face).filter(Face.id.in_(face_ids)).update(
                {Face.cluster_id: None}, synchronize_session=False
            )
            self.db.commit()

    def count_by_rooms(self, room_ids: list[int]) -> int:
        if not room_ids:
            return 0
        from app.models.image import Image

        return (
            self.db.query(func.count(Face.id))
            .join(Image, Image.id == Face.image_id)
            .filter(Image.room_id.in_(room_ids))
            .scalar()
            or 0
        )

    def get_cluster_face_count(self, cluster_id: int) -> int:
        return self.db.query(func.count(Face.id)).filter(Face.cluster_id == cluster_id).scalar() or 0

    def get_cluster_image_ids(self, cluster_id: int) -> list[int]:
        rows = self.db.query(Face.image_id).filter(Face.cluster_id == cluster_id).distinct().all()
        return [r[0] for r in rows]

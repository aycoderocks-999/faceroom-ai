from sqlalchemy.orm import Session

from app.repositories.cluster_repository import ClusterRepository
from app.repositories.face_repository import FaceRepository
from app.repositories.image_repository import ImageRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.search_repository import SearchRepository


class DashboardService:
    def __init__(self, db: Session):
        self.room_repo = RoomRepository(db)
        self.image_repo = ImageRepository(db)
        self.face_repo = FaceRepository(db)
        self.cluster_repo = ClusterRepository(db)
        self.search_repo = SearchRepository(db)

    def get_stats(self, user_id: int) -> dict:
        rooms = self.room_repo.get_user_rooms(user_id)
        room_ids = [r.id for r in rooms]

        recent_uploads = self.image_repo.get_recent_uploads(room_ids, limit=5)
        recent_searches = self.search_repo.get_recent_by_user(user_id, limit=5)

        return {
            "total_rooms": len(rooms),
            "total_images": self.image_repo.count_by_rooms(room_ids),
            "total_faces": self.face_repo.count_by_rooms(room_ids),
            "total_clusters": self.cluster_repo.count_by_rooms(room_ids),
            "recent_uploads": [
                {
                    "id": img.id,
                    "room_id": img.room_id,
                    "image_url": img.image_url,
                    "filename": img.filename,
                    "upload_time": img.upload_time,
                }
                for img in recent_uploads
            ],
            "recent_searches": [
                {
                    "id": s.id,
                    "room_id": s.room_id,
                    "result_count": s.result_count,
                    "latency_ms": s.latency_ms,
                    "timestamp": s.timestamp,
                }
                for s in recent_searches
            ],
        }

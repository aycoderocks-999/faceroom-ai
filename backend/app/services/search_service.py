import time

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.repositories.face_repository import FaceRepository
from app.repositories.image_repository import ImageRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.search_repository import SearchRepository
from app.schemas.search import FaceSearchResponse, SearchHistoryResponse, SearchHistoryItem, SearchMatch
from app.services.face_engine import detect_and_embed
from app.services.qdrant_service import QdrantService

settings = get_settings()


class SearchService:
    def __init__(self, db: Session, qdrant: QdrantService | None = None):
        self.db = db
        self.room_repo = RoomRepository(db)
        self.image_repo = ImageRepository(db)
        self.face_repo = FaceRepository(db)
        self.search_repo = SearchRepository(db)
        self.qdrant = qdrant or QdrantService()

    async def search_by_face(
        self,
        room_id: int,
        user_id: int,
        query_image: UploadFile,
        top_k: int = 50,
        threshold: float | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> FaceSearchResponse:
        if not self.room_repo.is_member(room_id, user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a room member")

        start = time.perf_counter()
        content = await query_image.read()
        detected = detect_and_embed(content)
        if not detected:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No face detected in query image")

        query_embedding = detected[0].embedding
        sim_threshold = threshold if threshold is not None else settings.FACE_SIMILARITY_THRESHOLD
        offset = (page - 1) * page_size

        hits = self.qdrant.search(
            query_vector=query_embedding,
            room_id=room_id,
            top_k=top_k,
            threshold=sim_threshold,
            offset=offset,
        )

        seen_images: set[int] = set()
        matches: list[SearchMatch] = []
        for hit in hits:
            image_id = hit["image_id"]
            if image_id in seen_images:
                continue
            seen_images.add(image_id)
            image = self.image_repo.get_by_id(image_id)
            if image:
                matches.append(
                    SearchMatch(
                        image_id=image.id,
                        image_url=image.image_url,
                        similarity=hit["similarity"],
                        face_id=hit.get("face_id"),
                    )
                )

        elapsed_ms = (time.perf_counter() - start) * 1000
        self.search_repo.create_log(user_id, room_id, elapsed_ms, len(matches))

        return FaceSearchResponse(
            matches=matches[:page_size],
            match_count=len(matches),
            search_time_ms=round(elapsed_ms, 2),
            threshold=sim_threshold,
        )

    def search_similar_face(
        self, face_id: int, user_id: int, top_k: int = 20, threshold: float | None = None
    ) -> FaceSearchResponse:
        face = self.face_repo.get_by_id(face_id)
        if not face:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Face not found")

        image = self.image_repo.get_by_id(face.image_id)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
        if not self.room_repo.is_member(image.room_id, user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a room member")

        from qdrant_client.http import models as qmodels

        start = time.perf_counter()
        point = self.qdrant.client.retrieve(
            collection_name=settings.QDRANT_COLLECTION,
            ids=[face.embedding_id],
            with_vectors=True,
        )
        if not point:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Embedding not found")

        query_vector = point[0].vector
        sim_threshold = threshold if threshold is not None else settings.FACE_SIMILARITY_THRESHOLD
        hits = self.qdrant.search(
            query_vector=query_vector,
            room_id=image.room_id,
            top_k=top_k + 1,
            threshold=sim_threshold,
        )

        matches: list[SearchMatch] = []
        for hit in hits:
            if hit.get("face_id") == face_id:
                continue
            img = self.image_repo.get_by_id(hit["image_id"])
            if img:
                matches.append(
                    SearchMatch(
                        image_id=img.id,
                        image_url=img.image_url,
                        similarity=hit["similarity"],
                        face_id=hit.get("face_id"),
                    )
                )

        elapsed_ms = (time.perf_counter() - start) * 1000
        return FaceSearchResponse(
            matches=matches,
            match_count=len(matches),
            search_time_ms=round(elapsed_ms, 2),
            threshold=sim_threshold,
        )

    def get_search_history(self, user_id: int, page: int = 1, page_size: int = 20) -> SearchHistoryResponse:
        items, total = self.search_repo.get_user_history(user_id, page, page_size)
        return SearchHistoryResponse(
            items=[SearchHistoryItem.model_validate(i) for i in items],
            total=total,
        )

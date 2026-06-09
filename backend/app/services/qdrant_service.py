import uuid
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http import models

from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()
VECTOR_SIZE = 512


class QdrantService:
    def __init__(self):
        self._client: QdrantClient | None = None

    @property
    def client(self) -> QdrantClient:
        if self._client is None:
            kwargs: dict[str, Any] = {"url": settings.QDRANT_URL}
            if settings.QDRANT_API_KEY:
                kwargs["api_key"] = settings.QDRANT_API_KEY
            self._client = QdrantClient(**kwargs)
        return self._client

    def ensure_collection(self) -> None:
        collections = [c.name for c in self.client.get_collections().collections]
        if settings.QDRANT_COLLECTION not in collections:
            self.client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
            )
            self.client.create_payload_index(
                collection_name=settings.QDRANT_COLLECTION,
                field_name="room_id",
                field_schema=models.PayloadSchemaType.INTEGER,
            )
            logger.info("Created Qdrant collection %s", settings.QDRANT_COLLECTION)

    def upsert_embedding(
        self,
        embedding: list[float],
        room_id: int,
        image_id: int,
        face_id: int,
        embedding_id: str | None = None,
    ) -> str:
        self.ensure_collection()
        point_id = embedding_id or str(uuid.uuid4())
        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={"room_id": room_id, "image_id": image_id, "face_id": face_id},
                )
            ],
        )
        return point_id

    def search(
        self,
        query_vector: list[float],
        room_id: int,
        top_k: int = 50,
        threshold: float | None = None,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        self.ensure_collection()
        results = self.client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=query_vector,
            query_filter=models.Filter(
                must=[models.FieldCondition(key="room_id", match=models.MatchValue(value=room_id))]
            ),
            limit=top_k + offset,
            score_threshold=threshold,
        )
        hits = results[offset : offset + top_k] if offset else results[:top_k]
        return [
            {
                "embedding_id": str(hit.id),
                "image_id": hit.payload.get("image_id"),
                "face_id": hit.payload.get("face_id"),
                "similarity": float(hit.score),
            }
            for hit in hits
        ]

    def delete_embedding(self, embedding_id: str) -> None:
        self.client.delete(
            collection_name=settings.QDRANT_COLLECTION,
            points_selector=models.PointIdsList(points=[embedding_id]),
        )


def get_qdrant_service() -> QdrantService:
    return QdrantService()

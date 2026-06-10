import uuid

from app.core.config import get_settings
from app.core.database import SessionLocal
from app.core.logging import logger
from app.models.image import ProcessingStatus
from app.models.processing_task import ProcessingTask, TaskStatus
from app.repositories.cluster_repository import ClusterRepository
from app.repositories.face_repository import FaceRepository
from app.repositories.image_repository import ImageRepository
from app.services.face_engine import cluster_embeddings, detect_and_embed
from app.services.qdrant_service import QdrantService
from app.services.storage_service import StorageService
from app.workers.celery_app import celery_app

settings = get_settings()


def _get_or_create_task(db, image_id: int, celery_task_id: str) -> ProcessingTask:
    task = db.query(ProcessingTask).filter(ProcessingTask.image_id == image_id).first()
    if not task:
        task = ProcessingTask(image_id=image_id, celery_task_id=celery_task_id, status=TaskStatus.QUEUED)
        db.add(task)
        db.commit()
        db.refresh(task)
    else:
        task.celery_task_id = celery_task_id
        task.status = TaskStatus.RUNNING
        db.commit()
    return task


@celery_app.task(bind=True, max_retries=3)
def process_image_task(self, image_id: int):
    db = SessionLocal()
    image_repo = ImageRepository(db)
    face_repo = FaceRepository(db)
    cluster_repo = ClusterRepository(db)
    storage = StorageService()
    qdrant = QdrantService()

    try:
        _get_or_create_task(db, image_id, self.request.id)
        image = image_repo.get_by_id(image_id)
        if not image:
            logger.error("Image %s not found", image_id)
            return

        image_repo.update_status(image_id, ProcessingStatus.PROCESSING)

        try:
            image_bytes = storage.download_image(image.storage_path)
        except Exception:
            logger.warning("Could not download from storage for image %s, skipping", image_id)
            image_repo.update_status(image_id, ProcessingStatus.FAILED)
            return

        detected_faces = detect_and_embed(image_bytes)
        logger.info("Detected %d faces in image %s", len(detected_faces), image_id)

        for idx, face_data in enumerate(detected_faces):
            crop_url = None
            try:
                crop_url = storage.upload_face_crop(
                    face_data.crop_bytes, image.room_id, image_id, idx
                )
            except Exception as e:
                logger.warning("Failed to upload face crop: %s", e)

            # Reserve a placeholder row in Postgres first so we have the real
            # face.id before upserting into Qdrant — avoids the face_id=0 race.
            temp_embedding_id = str(uuid.uuid4())
            face = face_repo.create(
                image_id=image_id,
                embedding_id=temp_embedding_id,
                bounding_box=face_data.bounding_box,
                quality_score=face_data.quality_score,
                crop_url=crop_url,
            )

            # Now upsert with the real face.id — no race window.
            embedding_id = qdrant.upsert_embedding(
                embedding=face_data.embedding,
                room_id=image.room_id,
                image_id=image_id,
                face_id=face.id,
                embedding_id=temp_embedding_id,   # reuse the same UUID
            )

        image_repo.update_status(image_id, ProcessingStatus.COMPLETED)
        task = db.query(ProcessingTask).filter(ProcessingTask.image_id == image_id).first()
        if task:
            task.status = TaskStatus.COMPLETED
            db.commit()

        run_room_clustering.delay(image.room_id)

    except Exception as exc:
        logger.exception("Failed to process image %s", image_id)
        image_repo.update_status(image_id, ProcessingStatus.FAILED)
        task = db.query(ProcessingTask).filter(ProcessingTask.image_id == image_id).first()
        if task:
            task.status = TaskStatus.FAILED
            task.error_message = str(exc)
            task.retry_count += 1
            db.commit()
        raise self.retry(exc=exc)
    finally:
        db.close()


@celery_app.task(bind=True, max_retries=2)
def run_room_clustering(self, room_id: int):
    db = SessionLocal()
    face_repo = FaceRepository(db)
    cluster_repo = ClusterRepository(db)

    try:
        faces = face_repo.get_room_faces(room_id)
        if not faces:
            return

        embeddings = []
        face_ids = []
        for face in faces:
            point = QdrantService().client.retrieve(
                collection_name=settings.QDRANT_COLLECTION,
                ids=[face.embedding_id],
                with_vectors=True,
            )
            if point and point[0].vector is not None:
                embeddings.append(point[0].vector)
                face_ids.append(face.id)

        if not embeddings:
            return

        # Clear all existing clusters for this room before re-clustering
        # to prevent duplicate accumulation on each run.
        face_repo.bulk_clear_cluster([f.id for f in faces])
        for old_cluster in cluster_repo.get_room_clusters(room_id):
            cluster_repo.delete(old_cluster)

        labels = cluster_embeddings(embeddings)
        label_to_cluster: dict[int, int] = {}

        for face_id, label in zip(face_ids, labels):
            if label == -1:
                cluster = cluster_repo.create(room_id, "Unknown Person")
                face_repo.update_cluster(face_id, cluster.id)
                rep_face = face_repo.get_by_id(face_id)
                if rep_face and rep_face.crop_url:
                    cluster_repo.update(cluster, representative_face_id=face_id, representative_face_url=rep_face.crop_url)
                continue

            if label not in label_to_cluster:
                cluster = cluster_repo.create(room_id, f"Person {label + 1}")
                label_to_cluster[label] = cluster.id

            cluster_id = label_to_cluster[label]
            face_repo.update_cluster(face_id, cluster_id)

        for cluster_id in label_to_cluster.values():
            _update_cluster_representative(db, cluster_id)

        logger.info("Clustering complete for room %s", room_id)

    except Exception as exc:
        logger.exception("Clustering failed for room %s", room_id)
        raise self.retry(exc=exc)
    finally:
        db.close()


@celery_app.task
def recluster_room_task(room_id: int):
    run_room_clustering.delay(room_id)


def _update_cluster_representative(db, cluster_id: int):
    face_repo = FaceRepository(db)
    cluster_repo = ClusterRepository(db)
    faces = face_repo.get_cluster_faces(cluster_id)
    if not faces:
        return
    best = max(faces, key=lambda f: f.quality_score or 0)
    cluster = cluster_repo.get_by_id(cluster_id)
    if cluster:
        cluster_repo.update(
            cluster,
            representative_face_id=best.id,
            representative_face_url=best.crop_url,
        )

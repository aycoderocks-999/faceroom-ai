import threading
from dataclasses import dataclass

import numpy as np

from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

_model_lock = threading.Lock()
_face_app = None
_ml_available: bool | None = None


def _check_ml_available() -> bool:
    global _ml_available
    if _ml_available is None:
        try:
            import cv2  # noqa: F401
            from insightface.app import FaceAnalysis  # noqa: F401
            from sklearn.cluster import DBSCAN  # noqa: F401

            _ml_available = True
        except ImportError:
            _ml_available = False
            logger.warning("ML dependencies not installed. Face detection unavailable.")
    return _ml_available


@dataclass
class DetectedFace:
    bounding_box: dict
    embedding: list[float]
    quality_score: float
    crop_bytes: bytes


def _get_face_app():
    if not _check_ml_available():
        raise RuntimeError("Install ML dependencies: pip install -r requirements-ml.txt")
    global _face_app
    if _face_app is None:
        with _model_lock:
            if _face_app is None:
                from insightface.app import FaceAnalysis

                app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
                app.prepare(ctx_id=-1, det_size=(640, 640))
                _face_app = app
                logger.info("InsightFace model loaded (RetinaFace + ArcFace)")
    return _face_app


def _compute_quality(face_img: np.ndarray) -> float:
    import cv2

    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return min(1.0, laplacian_var / 500.0)


def detect_and_embed(image_bytes: bytes) -> list[DetectedFace]:
    import cv2

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")

    app = _get_face_app()
    faces = app.get(img)
    results: list[DetectedFace] = []

    for face in faces:
        bbox = face.bbox.astype(int)
        x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
        h, w = img.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)

        crop = img[y1:y2, x1:x2]
        if crop.size == 0:
            continue

        _, buffer = cv2.imencode(".jpg", crop)
        quality = _compute_quality(crop)
        embedding = face.normed_embedding.tolist()

        results.append(
            DetectedFace(
                bounding_box={"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2)},
                embedding=embedding,
                quality_score=quality,
                crop_bytes=buffer.tobytes(),
            )
        )

    return results


def cluster_embeddings(embeddings: list[list[float]]) -> list[int]:
    if len(embeddings) < 2:
        return [-1] * len(embeddings)

    from sklearn.cluster import DBSCAN

    X = np.array(embeddings)
    clustering = DBSCAN(eps=settings.DBSCAN_EPS, min_samples=settings.DBSCAN_MIN_SAMPLES, metric="cosine")
    labels = clustering.fit_predict(X)
    return labels.tolist()

import numpy as np

from app.services.face_engine import cluster_embeddings


def test_cluster_embeddings_single_face():
    embedding = np.random.randn(512).tolist()
    labels = cluster_embeddings([embedding])
    assert labels == [-1]


def test_cluster_embeddings_identical_faces():
    base = np.random.randn(512)
    base = base / np.linalg.norm(base)
    embeddings = [base.tolist(), base.tolist(), base.tolist()]
    labels = cluster_embeddings(embeddings)
    assert len(labels) == 3

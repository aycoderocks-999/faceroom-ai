from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.search import FaceSearchResponse, SearchHistoryResponse
from app.services.search_service import SearchService

router = APIRouter()


@router.post("/face", response_model=FaceSearchResponse)
async def search_face(
    room_id: int = Form(...),
    query_image: UploadFile = File(...),
    top_k: int = Form(50),
    threshold: float | None = Form(None),
    page: int = Form(1),
    page_size: int = Form(20),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return await SearchService(db).search_by_face(
        room_id, current_user.id, query_image, top_k, threshold, page, page_size
    )


@router.get("/face/{face_id}/similar", response_model=FaceSearchResponse)
def search_similar_face(
    face_id: int,
    top_k: int = Query(20, ge=1, le=100),
    threshold: float | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return SearchService(db).search_similar_face(face_id, current_user.id, top_k, threshold)


@router.get("/history", response_model=SearchHistoryResponse)
def search_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return SearchService(db).get_search_history(current_user.id, page, page_size)

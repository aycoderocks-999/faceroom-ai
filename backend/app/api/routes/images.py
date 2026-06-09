from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.image import ImageResponse, ImageUploadResponse
from app.services.image_service import ImageService

router = APIRouter()


@router.post("/upload", response_model=ImageUploadResponse, status_code=201)
async def upload_images(
    room_id: int = Form(...),
    files: list[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return await ImageService(db).upload_images(room_id, current_user.id, files)


@router.get("/{image_id}", response_model=ImageResponse)
def get_image(image_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ImageService(db).get_image(image_id, current_user.id)

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_admin_user, get_current_user
from app.core.config import get_settings
from app.core.database import get_db
from app.models.image import Image, ProcessingStatus
from app.models.processing_task import ProcessingTask, TaskStatus
from app.models.user import User

router = APIRouter()
settings = get_settings()


@router.get("/files/{file_path:path}")
def serve_local_file(file_path: str):
    from app.services.storage_service import UPLOAD_ROOT

    full_path = (UPLOAD_ROOT / file_path).resolve()
    if not str(full_path).startswith(str(UPLOAD_ROOT.resolve())):
        raise HTTPException(status_code=403, detail="Access denied")
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(full_path)


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@router.get("/processing/status")
def processing_status(
    room_id: int | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(ProcessingTask)
    if room_id:
        from app.models.image import Image as Img

        image_ids = db.query(Img.id).filter(Img.room_id == room_id).subquery()
        query = query.filter(ProcessingTask.image_id.in_(image_ids))

    total = query.count()
    by_status = (
        db.query(ProcessingTask.status, func.count(ProcessingTask.id)).group_by(ProcessingTask.status).all()
    )
    pending_images = (
        db.query(func.count(Image.id))
        .filter(Image.processing_status.in_([ProcessingStatus.PENDING, ProcessingStatus.PROCESSING]))
        .scalar()
        or 0
    )

    return {
        "total_tasks": total,
        "by_status": {s.value: c for s, c in by_status},
        "pending_images": pending_images,
    }


@router.get("/admin/stats")
def admin_stats(current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    from app.models.face import Face
    from app.models.room import Room

    return {
        "users": db.query(func.count(User.id)).scalar(),
        "rooms": db.query(func.count(Room.id)).scalar(),
        "images": db.query(func.count(Image.id)).scalar(),
        "faces": db.query(func.count(Face.id)).scalar(),
        "failed_tasks": db.query(func.count(ProcessingTask.id))
        .filter(ProcessingTask.status == TaskStatus.FAILED)
        .scalar(),
    }

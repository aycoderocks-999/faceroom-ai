from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/stats")
def get_dashboard_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return DashboardService(db).get_stats(current_user.id)

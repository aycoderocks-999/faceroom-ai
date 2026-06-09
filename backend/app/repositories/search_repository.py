from sqlalchemy.orm import Session

from app.models.search_log import SearchLog


class SearchRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_log(self, user_id: int, room_id: int, latency_ms: float, result_count: int) -> SearchLog:
        log = SearchLog(user_id=user_id, room_id=room_id, latency_ms=latency_ms, result_count=result_count)
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_user_history(self, user_id: int, page: int = 1, page_size: int = 20) -> tuple[list[SearchLog], int]:
        query = self.db.query(SearchLog).filter(SearchLog.user_id == user_id).order_by(SearchLog.timestamp.desc())
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def get_recent_by_user(self, user_id: int, limit: int = 5) -> list[SearchLog]:
        return (
            self.db.query(SearchLog)
            .filter(SearchLog.user_id == user_id)
            .order_by(SearchLog.timestamp.desc())
            .limit(limit)
            .all()
        )

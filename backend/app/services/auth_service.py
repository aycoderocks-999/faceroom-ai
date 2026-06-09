from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: RegisterRequest) -> UserResponse:
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        if self.repo.get_by_username(data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        user = self.repo.create(data.email, data.username, hash_password(data.password))
        return UserResponse.model_validate(user)

    def login(self, data: LoginRequest) -> TokenResponse:
        user = self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return TokenResponse(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )

    def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        user_id = payload.get("sub")
        user = self.repo.get_by_id(int(user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return TokenResponse(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )

    def get_user(self, user_id: int) -> UserResponse:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)

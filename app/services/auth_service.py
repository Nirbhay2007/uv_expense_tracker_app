from fastapi import HTTPException

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse, UserLogin, UserRegister


class AuthService:
    def __init__(
        self,
        repository: UserRepository,
    ) -> None:
        self.repository = repository

    def register(
        self,
        user: UserRegister,
    ):
        existing_user = self.repository.get_by_email(
            user.email
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )

        password_hash = hash_password(
            user.password
        )

        return self.repository.create(
            email=user.email,
            password_hash=password_hash,
        )

    def login(
        self,
        credentials: UserLogin,
    ) -> TokenResponse:
        user = self.repository.get_by_email(
            credentials.email
        )

        if (
            user is None
            or not verify_password(
                credentials.password,
                user.password_hash,
            )
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        access_token = create_access_token(
            user.email,
        )

        return TokenResponse(
            access_token=access_token,
        )
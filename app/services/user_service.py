import logging
from datetime import datetime, timezone
from typing import Any

from app.repositories.user_repository import InMemoryUserRepository
from app.schemas.user import UserCreate, UserUpdate


logger = logging.getLogger("user_api")


class UserService:
    def __init__(self, repository: InMemoryUserRepository) -> None:
        self.repository = repository

    def create(self, payload: UserCreate) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        user_data = payload.model_dump(mode="json")
        user_data.update(
            email=str(payload.email).casefold(),
            created_at=now,
            updated_at=now,
        )
        user = self.repository.create(user_data)
        logger.info("User created user_id=%s", user["id"])
        return user

    def list(self, offset: int, limit: int) -> list[dict[str, Any]]:
        return self.repository.list(offset, limit)

    def get(self, user_id: str) -> dict[str, Any]:
        return self.repository.get(user_id)

    def update(self, user_id: str, payload: UserUpdate) -> dict[str, Any]:
        updates = payload.model_dump(exclude_unset=True, mode="json")
        if "email" in updates:
            updates["email"] = updates["email"].casefold()
        updates["updated_at"] = datetime.now(timezone.utc)
        user = self.repository.update(user_id, updates)
        logger.info("User updated user_id=%s", user_id)
        return user

    def delete(self, user_id: str) -> None:
        self.repository.delete(user_id)
        logger.info("User deleted user_id=%s", user_id)


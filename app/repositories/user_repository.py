import secrets
from threading import RLock
from typing import Any

from app.core.exceptions import EmailAlreadyExistsError, UserNotFoundError


class InMemoryUserRepository:
    """Thread-safe repository backed by a list of dictionaries."""

    def __init__(self) -> None:
        self._users: list[dict[str, Any]] = []
        self._lock = RLock()

    def _find(self, user_id: str) -> dict[str, Any]:
        for user in self._users:
            if user["id"] == user_id:
                return user
        raise UserNotFoundError()

    def _ensure_unique_email(
        self, email: str, exclude_user_id: str | None = None
    ) -> None:
        for user in self._users:
            if user["email"] == email and user["id"] != exclude_user_id:
                raise EmailAlreadyExistsError()

    def _generate_id(self) -> str:
        existing_ids = {user["id"] for user in self._users}
        for _ in range(100):
            user_id = f"user{secrets.randbelow(900_000) + 100_000}"
            if user_id not in existing_ids:
                return user_id
        raise RuntimeError("Unable to generate a unique user ID")

    def create(self, user_data: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            self._ensure_unique_email(user_data["email"])
            user = {"id": self._generate_id(), **user_data}
            self._users.append(user)
            return user.copy()

    def list(self, offset: int, limit: int) -> list[dict[str, Any]]:
        with self._lock:
            return [user.copy() for user in self._users[offset : offset + limit]]

    def get(self, user_id: str) -> dict[str, Any]:
        with self._lock:
            return self._find(user_id).copy()

    def update(self, user_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            user = self._find(user_id)
            if "email" in updates:
                self._ensure_unique_email(updates["email"], exclude_user_id=user_id)
            user.update(updates)
            return user.copy()

    def delete(self, user_id: str) -> None:
        with self._lock:
            user = self._find(user_id)
            self._users.remove(user)

    def clear(self) -> None:
        """Clear storage; useful for test isolation."""
        with self._lock:
            self._users.clear()


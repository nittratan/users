from typing import Any

from fastapi import APIRouter, Query, Response, status

from app.dependencies import user_service
from app.schemas.user import User, UserCreate, UserUpdate


router = APIRouter()


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate) -> dict[str, Any]:
    return user_service.create(payload)


@router.get("", response_model=list[User])
def list_users(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
) -> list[dict[str, Any]]:
    return user_service.list(offset=offset, limit=limit)


@router.get("/{user_id}", response_model=User)
def get_user(user_id: str) -> dict[str, Any]:
    return user_service.get(user_id)


@router.patch("/{user_id}", response_model=User)
def update_user(user_id: str, payload: UserUpdate) -> dict[str, Any]:
    return user_service.update(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str) -> Response:
    user_service.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


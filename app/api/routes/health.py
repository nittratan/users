from fastapi import APIRouter


router = APIRouter(tags=["system"])


@router.get("/")
def home() -> dict[str, str]:
    return {"message": "User API is running"}


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


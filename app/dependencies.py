from app.repositories.user_repository import InMemoryUserRepository
from app.services.user_service import UserService


user_repository = InMemoryUserRepository()
user_service = UserService(user_repository)


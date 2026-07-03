class AppError(Exception):
    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


class UserNotFoundError(AppError):
    def __init__(self) -> None:
        super().__init__(404, "USER_NOT_FOUND", "User not found")


class EmailAlreadyExistsError(AppError):
    def __init__(self) -> None:
        super().__init__(409, "EMAIL_ALREADY_EXISTS", "Email already exists")


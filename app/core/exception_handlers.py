import logging
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppError


logger = logging.getLogger("user_api")


def error_response(
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details: Any | None = None,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    error: dict[str, Any] = {"code": code, "message": message}
    if details is not None:
        error["details"] = jsonable_encoder(details)

    return JSONResponse(
        status_code=status_code,
        content={"error": error, "request_id": request_id},
        headers={"X-Request-ID": request_id} if request_id else None,
    )


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return error_response(request, exc.status_code, exc.code, exc.message)


async def http_error_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return error_response(
        request,
        exc.status_code,
        f"HTTP_{exc.status_code}",
        str(exc.detail),
    )


async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return error_response(
        request,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "VALIDATION_ERROR",
        "Request validation failed",
        exc.errors(),
    )


async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "Unhandled error request_id=%s",
        getattr(request.state, "request_id", None),
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return error_response(
        request,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "INTERNAL_SERVER_ERROR",
        "Something went wrong",
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(
        StarletteHTTPException, http_error_handler  # type: ignore[arg-type]
    )
    app.add_exception_handler(
        RequestValidationError, validation_error_handler  # type: ignore[arg-type]
    )
    app.add_exception_handler(Exception, unexpected_error_handler)

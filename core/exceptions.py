import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("ai_hub")


def error_response(status_code: int, code: str, message: str, detail: object | None = None) -> JSONResponse:
    payload: dict[str, object] = {
        "success": False,
        "error": {"code": code, "message": message},
    }
    if detail is not None:
        payload["error"]["detail"] = detail
    return JSONResponse(status_code=status_code, content=payload)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return error_response(422, "validation_error", "Request validation failed", exc.errors())

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        return error_response(exc.status_code, "http_error", str(exc.detail))

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception", extra={"error": str(exc)})
        return error_response(500, "internal_error", "Internal server error")

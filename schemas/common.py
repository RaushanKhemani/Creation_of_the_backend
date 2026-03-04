from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorPayload(BaseModel):
    code: str
    message: str
    detail: object | None = None


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T


class APIErrorResponse(BaseModel):
    success: bool = False
    error: ErrorPayload

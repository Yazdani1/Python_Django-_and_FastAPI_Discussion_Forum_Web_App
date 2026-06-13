from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    field: str | None = None
    message: str


class MetaData(BaseModel):
    page: int | None = None
    page_size: int | None = None
    total: int | None = None
    total_pages: int | None = None


class ApiResponse(BaseModel, Generic[T]):
    """Standard success response envelope for all API endpoints."""

    success: bool = True
    message: str = "Success"
    data: T | None = None
    errors: list[ErrorDetail] | None = None
    meta: MetaData | None = None

    @classmethod
    def ok(
        cls,
        data: Any = None,
        message: str = "Success",
        meta: MetaData | None = None,
    ) -> "ApiResponse":
        return cls(success=True, message=message, data=data, meta=meta)

    @classmethod
    def created(cls, data: Any = None, message: str = "Created successfully") -> "ApiResponse":
        return cls(success=True, message=message, data=data)


class ApiError(BaseModel):
    """Standard error response envelope for all API endpoints."""

    success: bool = False
    message: str
    data: None = None
    errors: list[ErrorDetail] | None = None
    meta: None = None

    @classmethod
    def validation_error(cls, errors: list[ErrorDetail], message: str = "Validation failed") -> "ApiError":
        return cls(message=message, errors=errors)

    @classmethod
    def not_found(cls, resource: str = "Resource") -> "ApiError":
        return cls(message=f"{resource} not found")

    @classmethod
    def unauthorized(cls, message: str = "Authentication required") -> "ApiError":
        return cls(message=message)

    @classmethod
    def forbidden(cls, message: str = "Insufficient permissions") -> "ApiError":
        return cls(message=message)

    @classmethod
    def server_error(cls, message: str = "An unexpected error occurred") -> "ApiError":
        return cls(message=message)

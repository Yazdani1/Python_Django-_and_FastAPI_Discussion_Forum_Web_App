from fastapi import APIRouter

from fastapi_app.utils.responses import ApiResponse

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> ApiResponse:
    return ApiResponse(message="API is healthy", data={"status": "ok"})

from fastapi import APIRouter

from .endpoints.admin import router as admin_router
from .endpoints.answers import router as answers_router
from .endpoints.auth import router as auth_router
from .endpoints.health import router as health_router
from .endpoints.posts import router as posts_router
from .endpoints.users import router as users_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(posts_router)
api_v1_router.include_router(answers_router)
api_v1_router.include_router(admin_router)

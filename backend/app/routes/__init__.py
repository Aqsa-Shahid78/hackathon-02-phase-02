from fastapi import APIRouter

from app.routes.auth import router as auth_router
from app.routes.tasks import router as tasks_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(tasks_router, tags=["tasks"])

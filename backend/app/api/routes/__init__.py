from app.api.routes.health import router as health_router
from app.api.routes.storage_classes import router as storage_classes_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(
    storage_classes_router, prefix="/starage-classes", tags=["starage-classes"]
)

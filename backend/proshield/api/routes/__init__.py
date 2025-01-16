from fastapi import APIRouter
from proshield.api.routes.attenuation_coefficients import (
    router as attenuation_coefficients_router,
)
from proshield.api.routes.health import router as health_router
from proshield.api.routes.materials import router as materials_router
from proshield.api.routes.storage_classes import router as storage_classes_router

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(
    storage_classes_router, prefix="/storage-classes", tags=["storage-classes"]
)
router.include_router(materials_router, prefix="/materials", tags=["materials"])
router.include_router(
    attenuation_coefficients_router,
    prefix="/attenuation-coefficients",
    tags=["attenuation-coefficients"],
)
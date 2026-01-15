from fastapi import APIRouter

from proshield.api.routes.attenuation_coefficients import (
    router as attenuation_coefficients_router,
)
from proshield.api.routes.building_types import router as building_types
from proshield.api.routes.buildings_coefficients import (
    router as buildings_coefficients_router,
)
from proshield.api.routes.calculations import router as calculations_router
from proshield.api.routes.health import router as health_router
from proshield.api.routes.location_condition_coefficients import (
    router as location_condition_coefficients_router,
)
from proshield.api.routes.materials import router as materials_router
from proshield.api.routes.storage_classes import router as storage_classes_router
from proshield.api.routes.wall_materials import router as wall_materials_router

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
router.include_router(building_types, prefix="/building-types", tags=["building-types"])
router.include_router(
    location_condition_coefficients_router,
    prefix="/location-condition-coefficients",
    tags=["location-condition-coefficients"],
)
router.include_router(
    wall_materials_router, prefix="/wall-materials", tags=["wall-materials"]
)
router.include_router(
    buildings_coefficients_router,
    prefix="/buildings-coefficients",
    tags=["buildings-coefficients"],
)
router.include_router(
    calculations_router, prefix="/calculations", tags=["calculations"]
)

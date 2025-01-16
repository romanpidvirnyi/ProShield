from app.views.attenuation_coefficients import AttenuationCoefficientsView
from app.views.building_types import BuildingTypesView
from app.views.buildings_coefficients import BuildingCoeficientsView
from app.views.home import HomeView
from app.views.location_condition_coefficients import LocationConditionCoeficientView
from app.views.materials import MaterialsView
from app.views.starage_classes import StorageClassesView
from app.views.wall_materials import WallMaterialsView

__all__ = [
    "AttenuationCoefficientsView",
    "MaterialsView",
    "StorageClassesView",
    "HomeView",
    "BuildingTypesView",
    "LocationConditionCoeficientView",
    "WallMaterialsView",
    "BuildingCoeficientsView",
]

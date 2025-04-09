from fastapi import APIRouter
from proshield.views.main.home import router as home_router
from proshield.views.square_law.square_law import router as square_law_router

router = APIRouter()

router.include_router(home_router, prefix="/home", tags=["home"])
router.include_router(square_law_router, prefix="/square-law", tags=["square-law"])

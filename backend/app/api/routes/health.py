from app.schemas.health import HealthResponse
from fastapi import APIRouter, HTTPException, Response, Security, status

router = APIRouter(prefix="")


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
)
async def get_health_status() -> HealthResponse:
    return HealthResponse(status="ok")

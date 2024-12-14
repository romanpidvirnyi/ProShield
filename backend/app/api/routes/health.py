from fastapi import APIRouter, HTTPException, Response, Security, status

from backend.app.schemas.health import HealthResponse

router = APIRouter(prefix="")


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
)
async def get_health_status() -> HealthResponse:
    return HealthResponse(status="ok")

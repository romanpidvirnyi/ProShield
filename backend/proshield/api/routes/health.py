from fastapi import APIRouter, HTTPException, Request, Response, Security, status
from proshield.schemas.health import HealthResponse

router = APIRouter(prefix="")


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
)
async def get_health_status() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get(
    "/headers",
    status_code=status.HTTP_200_OK,
)
async def debug_headers(request: Request):
    return {
        "headers": dict(request.headers),
        "scheme": request.scope.get("scheme"),
        "server": request.scope.get("server"),
        "base_url": str(request.base_url),
        "url_for_static": str(request.url_for("static", path="test.css")),
    }

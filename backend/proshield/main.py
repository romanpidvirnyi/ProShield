import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from proshield import content
from proshield.api.routes import router as api_router
from proshield.core.database import SessionLocal, get_db
from proshield.views import router as views_routes
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db: Session = SessionLocal()
    content.preload_templates(db=db)
    yield


app = FastAPI(
    title="Protection Shield Coefficient API",
    description="Protection Shield Coefficient API",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    lifespan=lifespan,
)


# Custom middleware to handle X-Forwarded-Proto
@app.middleware("http")
async def fix_scheme_middleware(request: Request, call_next):
    # Check X-Forwarded-Proto header from Nginx
    forwarded_proto = request.headers.get("X-Forwarded-Proto")
    if forwarded_proto:
        request.scope["scheme"] = forwarded_proto

    # Also fix the host if needed
    forwarded_host = request.headers.get("X-Forwarded-Host") or request.headers.get(
        "Host"
    )
    if forwarded_host:
        request.scope["server"] = (
            forwarded_host.split(":")[0],
            443 if forwarded_proto == "https" else 80,
        )

    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
STATIC_PATH = os.path.join(Path(__file__).resolve().parent, "static")
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

# Include routers
app.include_router(api_router, prefix="/api", tags=["API"])
app.include_router(views_routes)

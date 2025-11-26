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


class ProxyHeadersMiddleware:
    """ASGI middleware that modifies scope based on proxy headers."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))

            # Get X-Forwarded-Proto (headers are bytes)
            forwarded_proto = headers.get(b"x-forwarded-proto", b"").decode("latin-1")
            if forwarded_proto:
                scope["scheme"] = forwarded_proto

            # Get the correct host
            forwarded_host = headers.get(b"x-forwarded-host", b"").decode("latin-1")
            host = headers.get(b"host", b"").decode("latin-1")

            actual_host = forwarded_host or host
            if actual_host:
                # Remove port if present
                hostname = actual_host.split(":")[0]
                port = 443 if forwarded_proto == "https" else 80
                scope["server"] = (hostname, port)

        await self.app(scope, receive, send)


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


# Wrap the app with the proxy middleware (this is the key!)
app = ProxyHeadersMiddleware(app)

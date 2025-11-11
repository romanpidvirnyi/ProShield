import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI
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
    # get db session
    db: Session = SessionLocal()

    # pre-load
    content.preload_templates(db=db)

    yield


# Initialize FastAPI application
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
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# Mount static files
STATIC_PATH = os.path.join(Path(__file__).resolve().parent, "static")
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

# Include routers
app.include_router(api_router, prefix="/api", tags=["API"])
app.include_router(views_routes)

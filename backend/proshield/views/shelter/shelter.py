import json
import os

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from proshield import crud
from proshield.content.base import INIT_DATA_DIR
from proshield.core.database import get_db
from proshield.views.dependencies import get_templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def shelter_main(request: Request, templates=Depends(get_templates)):
    return templates.TemplateResponse(
        request=request,
        name="shelter/shelter-01.html",
        context={},
    )


@router.get("/separate-recessed", response_class=HTMLResponse)
async def shelter_separate_recessed(
    request: Request,
    templates=Depends(get_templates),
    db=Depends(get_db),
):
    storage_classes = crud.get_storage_classes(db=db)
    materials = crud.get_materials(db=db)
    host_url = str(request.base_url)

    return templates.TemplateResponse(
        request=request,
        name="shelter/shelter-separate-recessed.html",
        context={
            "storage_classes": storage_classes,
            "materials": materials,
            "host_url": host_url,
        },
    )


@router.get("/separate-embanked", response_class=HTMLResponse)
async def shelter_separate_embanked(request: Request, templates=Depends(get_templates)):
    return templates.TemplateResponse(
        request=request,
        name="shelter/shelter-separate-embanked.html",
        context={},
    )

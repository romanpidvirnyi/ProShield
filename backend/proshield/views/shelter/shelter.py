import json
import os

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from proshield.content.base import INIT_DATA_DIR
from proshield.views.dependencies import get_templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def shelter_view(request: Request, templates=Depends(get_templates)):
    return templates.TemplateResponse(
        request=request,
        name="shelter/shelter-01.html",
        context={},
    )

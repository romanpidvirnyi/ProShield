import json
import os

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from proshield.content.base import INIT_DATA_DIR
from proshield.views.dependencies import get_templates

router = APIRouter()


FILE_NAME = "radioactive_isotopes.json"


@router.get("/", response_class=HTMLResponse)
async def square_law_view(request: Request, templates=Depends(get_templates)):
    # load radioactive isotope data from json
    radioactive_isotopes_file_path = os.path.join(INIT_DATA_DIR, FILE_NAME)
    with open(radioactive_isotopes_file_path, "r") as file:
        data = json.load(file)

    return templates.TemplateResponse(
        request=request,
        name="square-law/square_law.html",
        context={"radioactive_isotopes": data},
    )

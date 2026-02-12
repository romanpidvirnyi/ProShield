from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from proshield.views.dependencies import get_templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home_view(request: Request, templates=Depends(get_templates)):
    return templates.TemplateResponse(
        request=request, name="main/home.html", context={}
    )


@router.get("/about", response_class=HTMLResponse)
async def about_view(request: Request, templates=Depends(get_templates)):
    return templates.TemplateResponse(
        request=request, name="main/about.html", context={}
    )

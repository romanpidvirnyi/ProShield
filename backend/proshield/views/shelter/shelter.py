from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
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
    return templates.TemplateResponse(
        request=request,
        name="shelter/shelter-separate-recessed.html",
    )


@router.get("/separate-embanked", response_class=HTMLResponse)
async def shelter_separate_embanked(request: Request, templates=Depends(get_templates)):
    return templates.TemplateResponse(
        request=request,
        name="shelter/shelter-separate-recessed.html",
        context={},
    )


@router.get("/separate-freestanding", response_class=HTMLResponse)
async def shelter_separate_freestanding(
    request: Request, templates=Depends(get_templates)
):
    return templates.TemplateResponse(
        request=request,
        name="shelter/shelter-separate-recessed.html",
        context={},
    )

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(tags=["Web UI"])

# Ensure templates directory exists relative to current file
templates_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "web", "templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/", response_class=HTMLResponse, summary="Dashboard UI")
async def dashboard(request: Request):
    """
    Serves the main web dashboard interface.
    """
    return templates.TemplateResponse("index.html", {"request": request})

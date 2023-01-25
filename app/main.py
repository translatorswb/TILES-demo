from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .library.helpers import openfile
from app.routers import tiles
from dotenv import load_dotenv
load_dotenv()

import mimetypes
mimetypes.init() 


app = FastAPI()

templates = Jinja2Templates(directory="templates")

mimetypes.add_type('application/javascript', '.js')
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(tiles.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("tilesrpi.html", {"request": request})

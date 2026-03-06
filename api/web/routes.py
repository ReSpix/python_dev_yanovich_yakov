from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

web_router = APIRouter(prefix="/web")

@web_router.get("/")
def index():
    with open("web/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import audio, auth
from fastapi.responses import HTMLResponse, FileResponse
import os

app = FastAPI()

# Montaje de archivos estáticos
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))

if not os.path.exists(STATIC_DIR):
    raise RuntimeError(f"Directory '{STATIC_DIR}' does not exist")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Incluye los routers
app.include_router(audio.router, prefix="/audio")
app.include_router(auth.router, prefix="/auth")

# Ruta principal para servir el index.html
@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return HTMLResponse("<h1>Index no encontrado</h1>", status_code=404)
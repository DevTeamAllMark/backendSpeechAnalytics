from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from app.services.processor import scan_folder, process_audio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Scanning
    await scan_folder()
    
    # Create task
    task = asyncio.create_task(process_audio())
    
    try:
        yield  # Ready
    finally:
        #Clean controller
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("🔴 Tarea de procesamiento de audio cancelada correctamente.")

app = FastAPI(lifespan=lifespan)
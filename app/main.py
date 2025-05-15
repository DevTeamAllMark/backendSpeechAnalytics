from fastapi import FastAPI
import asyncio
from app.services.processor import scan_folder, process_audio

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await scan_folder()
    asyncio.create_task(process_audio())
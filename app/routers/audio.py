from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.whisper import transcribe_with_whisper
from app.utils.audio_utils import convert_to_wav, is_audio_file
from app.db.mongo import collection
import os
import shutil
import asyncio

router = APIRouter()
UPLOAD_FOLDER = "uploads/"

# Crear un semáforo en la lógica para limitar la cantidad de archivos procesados simultáneamente
semaphore = asyncio.Semaphore(10)

# 🌀 Función para procesar archivos de audio, con limitación de concurrencia
async def process_audio_with_limit(wav_path: str):
    async with semaphore:  # Limitar la concurrencia
        transcription = await transcribe_with_whisper(wav_path)

        # Guardar la transcripción en la base de datos
        await collection.insert_one({
            "filename": os.path.basename(wav_path),
            "transcription": transcription
        })

        print(f"✅ Transcripción guardada: {wav_path}")

@router.get("/transcriptions")
async def get_transcriptions():
    try:
        transcriptions = list(collection.find({}, {"_id": 0}))
        return {"transcriptions": transcriptions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload", response_model=None)
async def upload_file(file: UploadFile = File(...)):
    try:
        # Crear carpeta si no existe
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Guardar archivo temporal
        temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Verificar que el archivo es de audio
        if not is_audio_file(temp_path):
            os.remove(temp_path)
            raise HTTPException(status_code=400, detail="El archivo no es un formato de audio compatible.")

        # Convertir a WAV si es necesario
        wav_path = convert_to_wav(temp_path)

        # Procesar el archivo en segundo plano con semáforo
        await process_audio_with_limit(wav_path)

        # Eliminar archivo temporal
        if temp_path != wav_path and os.path.exists(temp_path):
            os.remove(temp_path)

        return {"filename": file.filename, "status": "En proceso de transcripción"}

    except Exception as e:
        # Lanzar excepción de FastAPI
        raise HTTPException(status_code=500, detail=str(e))
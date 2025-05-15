import os
import asyncio
from app.config import AUDIO_FOLDER
from app.utils.audio_utils import is_audio_file, convert_to_wav
from app.services.assemblyai import transcribe_with_assembly
from app.services.whisper import transcribe_with_whisper
from app.db.mongo import collection

queue = asyncio.Queue()

async def scan_folder():
    for file in os.listdir(AUDIO_FOLDER):
        path = os.path.join(AUDIO_FOLDER, file)
        if os.path.isfile(path) and is_audio_file(file):
            await queue.put(path)

async def process_audio():
    while True:
        audio_path = await queue.get()
        try:
            print(f"🟡 Procesando: {audio_path}")
            wav_path = convert_to_wav(audio_path)
            text = await transcribe_with_whisper(wav_path)

            await collection.insert_one({
                "filename": os.path.basename(audio_path),
                "text": text
            })
            print(f"✅ Transcripción guardada: {audio_path}")
        except Exception as e:
            print(f"❌ Error con el")
        queue.task_done()
import asyncio
import httpx
from app.config import ASSEMBLYAI_API_KEY

API_URL = "https://api.assemblyai.com/v2/transcript"

async def transcribe_with_assembly(audio_path: str) -> str:
    headers = {
        "authorization": ASSEMBLYAI_API_KEY
    }

    async with httpx.AsyncClient() as client:
        # Paso 1: subir audio
        with open(audio_path, "rb") as f:
            upload_res = await client.post(
                "https://api.assemblyai.com/v2/upload",
                headers=headers,
                content=f
            )
        audio_url = upload_res.json()["upload_url"]

        # Paso 2: solicitar transcripción en español
        transcribe_res = await client.post(
            API_URL,
            headers=headers,
            json={
                "audio_url": audio_url,
                "language_code": "es"
            }
        )
        transcript_id = transcribe_res.json()["id"]

        # Paso 3: hacer polling hasta que la transcripción esté completa
        while True:
            poll_res = await client.get(f"{API_URL}/{transcript_id}", headers=headers)
            data = poll_res.json()
            status = data.get("status")

            if status == "completed":
                return data.get("text", "")
            elif status == "error":
                raise Exception(f"Transcription failed: {data}")
            else:
                await asyncio.sleep(5)
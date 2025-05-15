import whisper
import os
import shutil

model = whisper.load_model("medium")
new_pathWav = r"C:\AudiosTestWav"

async def transcribe_with_whisper(audio_path: str) -> str:
    try:
        # Crear el directorio de destino si no existe
        if not os.path.exists(new_pathWav):
            os.makedirs(new_pathWav)
        
        # Mover el archivo
        print(f"✅ Verificando archivo antes de mover: {audio_path} -> {os.path.exists(audio_path)}")
        destino = os.path.join(new_pathWav, os.path.basename(audio_path))
        shutil.move(audio_path, destino)

        # Normaliza la ruta para evitar problemas con separadores
        destino = os.path.abspath(os.path.normpath(destino))

        # Validaciones de existencia y permisos
        if not os.path.exists(destino):
            raise FileNotFoundError(f"El archivo no existe: {destino}")

        if not destino.endswith(".wav"):
            raise ValueError(f"El archivo debe ser WAV, pero se recibió: {destino}")

        if not os.access(destino, os.R_OK):
            raise PermissionError(f"⚠️ No tienes permisos para leer el archivo: {destino}")

        # Verificación adicional del contenido del archivo
        try:
            with open(destino, "rb") as f:
                print(f"✅ Archivo leído correctamente: {destino}")
        except Exception as read_err:
            raise Exception(f"❌ No se pudo leer el archivo: {destino} - Error: {read_err}")

        # Transcripción
        options = {
            "language": "es",
            "best_of": 5,
            "temperature": 0.0,
            "fp16": False
        }
        result = model.transcribe(destino, **options)
        return result["text"]
    
    except Exception as e:
        print(f"❌ Error de transcripción: {e}")
        raise e
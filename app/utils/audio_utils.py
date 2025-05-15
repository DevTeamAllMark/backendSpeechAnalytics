import os
import subprocess
import shutil
import time

ffmpeg_path = r"C:/Program Files/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"
new_pathWav = r"C:\AudiosTestWav"

def is_audio_file(filename: str) -> bool:
    return filename.endswith((".mp3", ".wav", ".m4a", ".ogg"))

def convert_to_wav(input_path: str, duration: int = 210) -> str:
    # Asegurarse de que la ruta es absoluta
    input_path = os.path.abspath(input_path)
    output_path = os.path.splitext(input_path)[0] + ".wav"
    
    # Verifica si el archivo ya es .wav
    if input_path.endswith(".wav"):
        return input_path

    # Verifica si el archivo de entrada existe
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"El archivo no existe: {input_path}")

    try:
        # Convertir y recortar a los primeros 2 minutos
        result = subprocess.run([
            ffmpeg_path, "-y", "-i", input_path,
            "-ar", "16000", "-ac", "1",
            "-t", str(duration),  # Recorte de duración
            output_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Error en la conversión de {input_path} a .wav:\n{result.stderr}")
        
        time.sleep(5)
        
        if not os.path.exists(output_path):
            raise Exception(f"La conversión no se completó correctamente. El archivo no se creó: {output_path}")
        
        return output_path
          
    except Exception as e:
        print(f"❌ Error en la conversión con ffmpeg. Error: {e}")
        raise e

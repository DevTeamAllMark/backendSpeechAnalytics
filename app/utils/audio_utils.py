import os
import subprocess

def convert_to_wav(input_path: str) -> str:
    output_path = input_path.rsplit(".", 1)[0] + ".wav"
    if input_path.endswith(".wav"):
        return input_path 

    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-ar", "16000", "-ac", "1", output_path
    ], check=True)
    return output_path

def is_audio_file(filename: str):
    return filename.endswith((".mp3", ".wav", ".m4a", ".ogg"))
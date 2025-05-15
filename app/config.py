import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
AUDIO_FOLDER = os.getenv("AUDIO_FOLDER", "C:\\AudiosTest")
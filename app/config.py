import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
AUDIO_FOLDER = os.getenv("AUDIO_FOLDER", "C:\\AudiosTest")

JWT_SECRET = os.getenv("JWT_SECRET", "defaultsecret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))
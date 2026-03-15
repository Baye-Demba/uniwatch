import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

# Charger la clé depuis .env
FERNET_KEY = os.getenv("FERNET_KEY")
fernet = Fernet(FERNET_KEY.encode())

def chiffrer(url: str) -> str:
    """Chiffre une URL RTSP avant stockage en base"""
    return fernet.encrypt(url.encode()).decode()

def dechiffrer(url_chiffree: str) -> str:
    """Déchiffre une URL RTSP pour établir la connexion"""
    return fernet.decrypt(url_chiffree.encode()).decode()
"""Configuration de l'application.

Deux modes :
- DevelopmentConfig : mode dev avec CAS simule (CAS_DEV_MODE=true)
- ProductionConfig : mode prod avec vrai CAS de l'universite

Les valeurs sont lues depuis les variables d'environnement (.env)
"""

import os
from dotenv import load_dotenv

# Charge les variables depuis le fichier .env
load_dotenv()


class Config:
    """Configuration de base (heritee par Dev et Prod)."""
    
    # Cle secrete pour signer les cookies de session
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Connexion MySQL
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    DB_NAME = os.environ.get('DB_NAME', 'suivi_colis')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    
    # URL du serveur CAS de l'universite
    CAS_SERVER = os.environ.get('CAS_SERVER', 'https://cas.univ-paris13.fr/cas')
    
    # URL publique de l'application (pour le callback CAS)
    APP_URL = os.environ.get('APP_URL', 'http://localhost:5000')


class DevelopmentConfig(Config):
    """Config developpement : debug actif, CAS simule."""
    DEBUG = True
    # En dev, on peut se connecter sans passer par le vrai CAS
    CAS_DEV_MODE = os.environ.get('CAS_DEV_MODE', 'true').lower() == 'true'


class ProductionConfig(Config):
    """Config production : debug desactive, vrai CAS."""
    DEBUG = False
    CAS_DEV_MODE = False  # Toujours utiliser le vrai CAS en prod

"""Point d'entree de l'application Flask.

Ce fichier initialise l'application, configure les parametres,
et importe tous les controllers pour enregistrer les routes.
"""

from flask import Flask
from config import DevelopmentConfig, ProductionConfig
import os

# Creation de l'instance Flask
app = Flask(__name__)

# Chargement de la config selon l'environnement (dev ou prod)
if os.environ.get('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Cle secrete pour les sessions (cookies securises)
app.secret_key = app.config.get('SECRET_KEY', 'dev-secret-key')

# Configuration de l'upload de fichiers
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite 16 MB

# Creation des dossiers d'upload s'ils n'existent pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'bc'), exist_ok=True)  # Bons de commande
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'bl'), exist_ok=True)  # Bons de livraison

# Initialisation de la connexion base de donnees
from app.dao.DatabaseConnection import db
db.init_app(app)

# Import des controllers (enregistre les routes)
# Chaque controller definit ses propres @app.route()
from app.controllers import AuthController       # /login, /logout, /auth/cas/*
from app.controllers import IndexController      # / (accueil)
from app.controllers import CommandeController   # /commandes/*
from app.controllers import ColisController      # /colis/*
from app.controllers import FournisseurController # /fournisseurs/*
from app.controllers import AdminController      # /admin/*
from app.controllers import NotificationController # /notifications/*
from app.controllers import BonLivraisonController # /bons-livraison/*
from app.controllers import UploadController     # /uploads/* (sert les fichiers)

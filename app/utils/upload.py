"""Utilitaires pour l'upload de fichiers.

Gere le stockage des fichiers (BC, BL) :
- Validation du type de fichier
- Generation de noms uniques (UUID)
- Stockage dans les sous-dossiers

Formats acceptes : PDF, PNG, JPG, JPEG, GIF
Taille max : 16 MB (configure dans __init__.py)
"""

import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid

# Extensions autorisees
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Verifie si l'extension du fichier est autorisee."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, subfolder=''):
    """Sauvegarde un fichier uploade et retourne le chemin relatif.
    
    Args:
        file: Objet FileStorage de Flask
        subfolder: Sous-dossier ('bc' ou 'bl')
    
    Returns:
        Chemin relatif du fichier (ex: 'bc/abc123.pdf')
    
    Raises:
        ValueError: Si le type de fichier n'est pas autorise
    """
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        raise ValueError('Type de fichier non autorise. Extensions acceptees: PDF, PNG, JPG, JPEG, GIF')
    
    # Generer un nom unique pour eviter les collisions
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    
    # Creer le sous-dossier si necessaire
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if subfolder:
        upload_folder = os.path.join(upload_folder, subfolder)
        os.makedirs(upload_folder, exist_ok=True)
    
    # Sauvegarder le fichier
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    
    # Retourner le chemin relatif (pour stockage en DB)
    if subfolder:
        return f"{subfolder}/{filename}"
    return filename


def delete_file(filepath):
    """Supprime un fichier uploade.
    
    Args:
        filepath: Chemin relatif du fichier (ex: 'bc/abc123.pdf')
    """
    if not filepath:
        return
    
    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filepath)
    if os.path.exists(full_path):
        os.remove(full_path)


def get_file_url(filepath):
    """Retourne l'URL pour acceder au fichier.
    
    Args:
        filepath: Chemin relatif (ex: 'bc/abc123.pdf')
    
    Returns:
        URL (ex: '/uploads/bc/abc123.pdf')
    """
    if not filepath:
        return None
    return f"/uploads/{filepath}"

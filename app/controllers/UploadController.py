"""Controller pour servir les fichiers uploades.

Les fichiers (BC, BL) sont stockes dans /app/uploads/.
Ce controller les sert aux utilisateurs connectes.

Route :
- /uploads/<path:filename> : Retourne le fichier demande
"""

import os
from flask import send_from_directory, abort
from app import app
from app.controllers.AuthController import require_login


@app.route('/uploads/<path:filename>')
@require_login
def uploaded_file(filename):
    """Sert un fichier uploade.
    
    Securite :
    - Requiert une connexion (pas d'acces anonyme)
    - Verifie que le fichier existe
    """
    upload_folder = app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, filename)
    
    if not os.path.exists(filepath):
        abort(404)
    
    directory = os.path.dirname(filepath)
    file = os.path.basename(filepath)
    return send_from_directory(directory, file)

"""Point d'entree pour lancer l'application Flask.

Usage :
    python run.py
    
Ou avec Docker :
    docker-compose up

L'application demarre sur http://localhost:8000
"""

import os
from app import app

if __name__ == '__main__':
    # host='0.0.0.0' pour etre accessible depuis Docker
    # debug=True active le rechargement automatique en dev
    # Port 8000 par defaut (5000 est utilise par AirPlay sur Mac)
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)

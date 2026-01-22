# =============================================================================
# Dockerfile pour l'application Suivi Colis
# =============================================================================
# 
# Build : docker build -t suivi-colis .
# Run   : docker run -p 5000:5000 suivi-colis
#
# En pratique, utiliser docker-compose up
# =============================================================================

# Image de base Python 3.11
FROM python:3.11-slim

# Dossier de travail dans le container
WORKDIR /app

# Copier les dependances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Creer les dossiers d'upload
RUN mkdir -p /app/app/uploads/bc /app/app/uploads/bl

# Port expose
EXPOSE 5000

# Commande de demarrage
CMD ["python", "run.py"]

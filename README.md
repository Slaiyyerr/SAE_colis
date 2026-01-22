# Suivi Colis - IUT Villetaneuse

Application web de suivi des colis commandes par l'IUT.

---

## Demarrage avec Docker

### Prerequis

| OS | Installation Docker |
|----|---------------------|
| **Windows** | [Docker Desktop](https://www.docker.com/products/docker-desktop/) + activer WSL2 |
| **Mac** | [Docker Desktop](https://www.docker.com/products/docker-desktop/) |
| **Linux** | `sudo apt install docker.io docker-compose` |

### Lancer l'application

```bash
# 1. Cloner le projet
git clone https://github.com/RoyalSec-Corp/SAE_colis.git
cd SAE_colis

# 2. Lancer (premiere fois : attendre 1-2 min)
docker-compose up --build
```

Ouvrir **http://localhost:5000**

---

### Probleme d'encodage (caracteres bizarres) ?

```bash
# Reset complet de la base
docker-compose down -v
docker-compose up --build
```

### Windows : Si ca ne marche pas

```bash
# Option 1 : Reinitialiser les fins de ligne
git config core.autocrlf false
rd /s /q SAE_colis
git clone https://github.com/RoyalSec-Corp/SAE_colis.git
cd SAE_colis
docker-compose up --build

# Option 2 : Reset complet Docker
docker-compose down -v
docker system prune -af
docker-compose up --build
```

---

### Commandes utiles

```bash
# Lancer en arriere-plan
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arreter
docker-compose down

# Reset complet (supprime les donnees)
docker-compose down -v
docker-compose up --build
```

---

## Installation sans Docker

```bash
# Prerequis: Python 3.10+, MySQL 8

pip install -r requirements.txt
cp .env.example .env
# Editer .env avec vos credentials MySQL

# Creer la base
mysql -u root -p -e "CREATE DATABASE suivi_colis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
mysql -u root -p suivi_colis < app/database/schema.sql
mysql -u root -p suivi_colis < app/database/donnees_de_test.sql

python run.py
```

---

## Comptes de test

| Email | Role | Droits |
|-------|------|--------|
| `admin@iutv.univ-paris13.fr` | Admin | Tout |
| `reprographie@iutv.univ-paris13.fr` | Responsable colis | Reception/livraison |
| `compta@iutv.univ-paris13.fr` | Editeur | Commandes/fournisseurs |
| `p.durand@iutv.univ-paris13.fr` | Demandeur | Consultation |

---

## Roles et permissions

| Role | Consultation | Commandes | Fournisseurs | Colis | Admin |
|------|-------------|-----------|--------------|-------|-------|
| Demandeur | Oui | - | - | - | - |
| Editeur | Oui | Creer/Modifier | Creer/Modifier | - | - |
| Responsable colis | Oui | - | - | Reception/Livraison | - |
| Admin | Oui | Tout | Tout | Tout | Oui |

---

## Structure du projet

```
app/
|-- controllers/    # Routes Flask
|-- services/       # Logique metier
|-- dao/            # Acces base de donnees
|-- models/         # Classes de donnees
|-- templates/      # HTML Jinja2
|-- utils/          # CAS client
`-- database/       # Scripts SQL
```

---

## Workflow colis

```
attendu --> recu --> en_distribution --> livre
                `--> probleme
```

**Statut "probleme"** : Colis avec un souci (destinataire inconnu, etiquette illisible, colis endommage...)

---

## Technologies

- Python 3.11 / Flask 3.0
- MySQL 8.0
- Jinja2
- Docker / Docker Compose

---

## Depannage

| Probleme | Solution |
|----------|----------|
| `Connection refused` | Attendre 30s que MySQL demarre |
| `Access denied` | `docker-compose down -v` puis relancer |
| Caracteres bizarres | Reset: `docker-compose down -v` |
| Port 5000 occupe | Changer le port dans docker-compose.yml |

---

*Projet SAE - IUT Villetaneuse 2025*

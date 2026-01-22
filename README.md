
\# Suivi Colis \- IUT Villetaneuse

Application web de gestion et suivi des colis commandés par l'IUT de Villetaneuse.

\#\# À propos  
Cette application a été conçue pour répondre aux besoins réels de l’IUT de Villetaneuse en matière de gestion logistique. Elle facilite le suivi complet des colis, depuis la commande jusqu’à la remise au destinataire final.

Chaque jour, le service de reprographie reçoit de nombreux colis destinés aux différents services et personnels de l’établissement.

Grâce à cette application, chaque colis est enregistré dès son arrivée, son statut évolue en temps réel, et les destinataires peuvent facilement consulter l’avancement de leurs commandes. Le système de rôles permet de répartir clairement les responsabilités : les demandeurs suivent leurs colis, les éditeurs gèrent les commandes et fournisseurs, les responsables traitent la réception et la distribution, et les administrateurs supervisent l’ensemble de la plateforme.

L’authentification via CAS assure une intégration fluide dans le système informatique de l’université, en limitant la création de comptes supplémentaires et en simplifiant l’accès pour les utilisateurs.

\#\# Démarrage rapide avec Docker (recommandé)

\#\#\# Prérequis

Installer Docker sur votre système :

| Système d'exploitation | Installation |  
|------------------------|--------------|  
| **\*\*Windows\*\*** | \[Docker Desktop\](https://www.docker.com/products/docker-desktop/) (activer WSL2) |  
| **\*\*macOS\*\*** | \[Docker Desktop\](https://www.docker.com/products/docker-desktop/) |  
| **\*\*Linux\*\*** | \`sudo apt install docker.io docker-compose\` |

\#\#\# Installation et lancement

\`\`\`bash  
\# Cloner le dépôt  
git clone https://github.com/Slaiyyerr/SAE\_colis.git  
cd SAE\_colis

\# Lancer l'application  
docker-compose up \--build  
\`\`\`

**\*\*L'application est accessible sur http://localhost:8000\*\***

\#\#\# Commandes Docker utiles

\`\`\`bash  
\# Lancer en arrière-plan  
docker-compose up \-d

\# Afficher les logs en temps réel  
docker-compose logs \-f

\# Arrêter l'application  
docker-compose down

\# Reset complet (cela supprime toutes les données)  
docker-compose down \-v  
docker-compose up \--build  
\`\`\`

\#\# Dépannage Docker

\#\#\# Problème d'encodage (caractères bizarres)

Si vous voyez des caractères mal affichés :

\`\`\`bash  
docker-compose down \-v  
docker-compose up \--build  
\`\`\`

\#\#\# Erreurs spécifiques Windows

**\*\*Problème de fins de ligne :\*\***  
\`\`\`bash  
git config core.autocrlf false  
rd /s /q SAE\_colis  
git clone https://github.com/Slaiyyerr/SAE\_colis.git  
cd SAE\_colis  
docker-compose up \--build  
\`\`\`

**\*\*Reset complet de Docker :\*\***  
\`\`\`bash  
docker-compose down \-v  
docker system prune \-af  
docker-compose up \--build  
\`\`\`

\#\#\# Autres problèmes courants

| Problème | Solution |  
|----------|----------|  
| \`Connection refused\` | Attendre 30 secondes que MySQL démarre complètement |  
| \`Access denied for user\` | Exécuter \`docker-compose down \-v\` puis relancer |  
| Caractères mal encodés | Reset complet : \`docker-compose down \-v\` |  
| Port 8000 déjà utilisé | Modifier le port dans \`docker-compose.yml\` (ex: \`8001\`à la place de \`8000\`) |  
| Conteneur qui redémarre en boucle | Vérifier les logs : \`docker-compose logs app\` |

\#\# Installation manuelle (sans Docker)

\#\#\# Prérequis  
\- Python 3.10 (ou supérieur)  
\- MySQL 8.0 (ou supérieur)

\#\#\# Étapes d'installation

\`\`\`bash  
\# Installer les dépendances Python  
pip install \-r requirements.txt

\# Configurer les variables d'environnement  
cp .env.example .env  
\# Éditer .env avec vos identifiants MySQL

\# Créer et initialiser la base de données  
mysql \-u root \-p \-e "CREATE DATABASE suivi\_colis CHARACTER SET utf8mb4 COLLATE utf8mb4\_unicode\_ci"  
mysql \-u root \-p suivi\_colis \< app/database/schema.sql  
mysql \-u root \-p suivi\_colis \< app/database/donnees\_de\_test.sql

\# Lancer l'application  
python run.py  
\`\`\`

L'application sera accessible sur **\*\*http://localhost:8000\*\***

\#\# Comptes de test

Tous les comptes utilisent le même mot de passe (défini dans les données de test).

| Email | Rôle | Permissions principales |  
|-------|------|------------------------|  
| \`admin@iutv.univ-paris13.fr\` | Administrateur | Accès complet à toutes les fonctionnalités |  
| \`reprographie@iutv.univ-paris13.fr\` | Responsable colis | Réception et livraison des colis |  
| \`compta@iutv.univ-paris13.fr\` | Éditeur | Gestion des commandes et fournisseurs |  
| \`p.durand@iutv.univ-paris13.fr\` | Demandeur | Consultation uniquement |

\#\# Système de permissions

| Rôle | Consultation | Commandes | Fournisseurs | Colis | Administration |  
|------|:------------:|:---------:|:------------:|:-----:|:--------------:|  
| **\*\*Demandeur\*\*** | Oui | Non | Non | Non | Non |  
| **\*\*Éditeur\*\*** | Oui | Créer/Modifier | Créer/Modifier | Non | Non |  
| **\*\*Responsable colis\*\*** | Oui | Non | Non | Réception/Livraison | Non |  
| **\*\*Administrateur\*\*** | Oui | Oui | Oui | Oui | Oui |

\#\# Workflow de gestion des colis

\`\`\`  
┌─────────┐  
│ Attendu │ Colis commandé, en attente de réception  
└────┬────┘  
    │  
    ▼  
┌─────────┐  
│  Reçu   │ Colis réceptionné à la reprographie  
└────┬────┘  
    │  
    ├──────────────────┐  
    ▼                  ▼  
┌──────────────┐   ┌──────────┐  
│Distribution  │   │ Problème │ Destinataire inconnu, colis endommagé...  
└──────┬───────┘   └──────────┘  
      │  
      ▼  
┌──────────┐  
│  Livré   │ Colis remis au destinataire  
└──────────┘  
\`\`\`

Le statut **\*\*"Problème"\*\*** est utilisé pour signaler un colis avec une anomalie (destinataire inconnu, adresse incomplète...).

\#\# Architecture du projet

\`\`\`  
SAE\_colis/  
├── app/  
│   ├── controllers/       \# Routes et endpoints Flask  
│   ├── services/          \# Logique métier de l'application  
│   ├── dao/               \# Data Access Objects (accès BD)  
│   ├── models/            \# Modèles de données  
│   ├── templates/         \# Templates HTML (Jinja2)  
│   ├── static/            \# Fichiers statiques  
│   ├── utils/             \# Utilitaires (client CAS ...)  
│   └── database/          \# Scripts SQL  
├── docker-compose.yml     \# Configuration Docker  
├── Dockerfile             \# Image Docker de l'application  
├── requirements.txt       \# Dépendances Python  
├── .env.example           \# Template de configuration  
└── run.py                 \# Point d'entrée de l'application  
\`\`\`

\#\# Technologies utilisées

\- **\*\*Backend\*\*** : Python 3.11, Flask 3.0  
\- **\*\*Base de données\*\*** : MySQL 8.0  
\- **\*\*Templating\*\*** : Jinja2  
\- **\*\*Conteneurisation\*\*** : Docker, Docker Compose  
\- **\*\*Authentification\*\*** : CAS de l'université

\#\# Fonctionnalités principales

\- Suivi en temps réel des colis  
\- Gestion multi-rôles avec permissions  
\- Historique complet des mouvements de colis  
\- Gestion des commandes et fournisseurs  
\- Notifications de réception et livraison  
\- Export et rapports détaillés  
\- Interface responsive et intuitive

\#\# Equipe de développement  
| Nom       | Rôle                   | Contributions                                                                      |  
| \--------- | \---------------------- | \---------------------------------------------------------------------------------- |  
| **\*\*MOHAMMAD Rehan\*\*** | Base de données        | Création et gestion de la base de données, Développement des DAO                                     |  
| **\*\*BOUSLAMA Adel\*\***  | DAO & Services         | Développement des DAO, logique métier, liaison avec les controllers                |  
| **\*\*KEBBICHE Rayan\*\*** | Services & Controllers | Développement des services et controllers, liaison back\-end / front\-end avec Jinja |  
| **\*\*BENANNI Fares\*\*** | Front\-end              | Développement de l’interface utilisateur                                           |  
| **\*\*ATANASE Gabin Ateba\*\*** | Front\-end              | Développement de l’interface utilisateur                                           |

Projet développé dans le cadre d'une SAE à l'IUT de Villetaneuse.

\[retour en haut\](\#top)


# Configuration CAS - Universite Paris 13

Ce guide explique comment configurer l'authentification CAS pour la production.

---

## 1. Prerequis

### Cote universite

Contacter la DSI de l'universite pour :

1. **Enregistrer votre application** comme service CAS autorise
2. **Obtenir l'URL du serveur CAS** (generalement `https://cas.univ-paris13.fr/cas`)
3. **Declarer l'URL de callback** de votre application : `https://votre-domaine.fr/auth/cas/callback`

### Informations a fournir a la DSI

| Information | Exemple |
|-------------|----------|
| Nom de l'application | Suivi Colis IUT Villetaneuse |
| URL de l'application | https://colis.iutv.univ-paris13.fr |
| URL de callback CAS | https://colis.iutv.univ-paris13.fr/auth/cas/callback |
| Responsable technique | Votre nom + email |
| Attributs CAS requis | mail, uid, displayName (optionnel) |

---

## 2. Configuration de l'application

### Variables d'environnement

Modifier le fichier `.env` en production :

```bash
# IMPORTANT : Desactiver le mode dev
CAS_DEV_MODE=false

# URL du serveur CAS de l'universite
CAS_SERVER=https://cas.univ-paris13.fr/cas

# URL publique de votre application (SANS slash final)
APP_URL=https://colis.iutv.univ-paris13.fr

# Cle secrete (generer une vraie cle !)
SECRET_KEY=votre-cle-secrete-aleatoire-de-32-caracteres
```

### Generer une cle secrete

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## 3. Fonctionnement du CAS

### Flux d'authentification

```
1. Utilisateur clique "Connexion"
         |
         v
2. Redirection vers CAS : https://cas.univ-paris13.fr/cas/login?service=...
         |
         v
3. Utilisateur entre ses identifiants universite
         |
         v
4. CAS redirige vers : https://votre-app.fr/auth/cas/callback?ticket=ST-xxxxx
         |
         v
5. L'application valide le ticket aupres du CAS
         |
         v
6. CAS retourne l'email de l'utilisateur
         |
         v
7. L'application verifie si l'email est dans la whitelist (table utilisateur)
         |
         v
8. Si oui -> session creee, acces autorise
   Si non -> "Non autorise"
```

---

## 4. Whitelist des utilisateurs

### Principe

Seuls les utilisateurs **presents dans la table `utilisateur`** peuvent acceder a l'application.

### Ajouter un utilisateur autorise

**Option 1 : Via l'interface admin**
1. Se connecter en tant qu'admin
2. Aller dans Admin > Utilisateurs
3. Ajouter l'email universitaire

**Option 2 : Via SQL**

```sql
INSERT INTO utilisateur (email, nom, prenom, role, id_departement)
VALUES ('prenom.nom@univ-paris13.fr', 'Nom', 'Prenom', 'demandeur', 1);
```

### Roles disponibles

| Role | Description |
|------|-------------|
| `demandeur` | Peut consulter ses commandes/colis |
| `editeur` | Peut creer/modifier commandes et fournisseurs |
| `responsable_colis` | Peut gerer les colis (reception, distribution, livraison) |
| `admin` | Acces complet + gestion utilisateurs |

---

## 5. Attributs CAS

Le serveur CAS peut retourner des attributs supplementaires. L'application utilise :

| Attribut | Utilisation |
|----------|-------------|
| `mail` | Email de l'utilisateur (obligatoire) |
| `uid` | Identifiant unique (fallback si mail absent) |
| `displayName` | Nom affiche (optionnel) |

Si l'attribut `mail` n'est pas retourne, l'application construit l'email : `{uid}@univ-paris13.fr`

---

## 6. Test de la configuration

### Verifier la connexion CAS

1. Mettre `CAS_DEV_MODE=false`
2. Redemarrer l'application
3. Acceder a http://votre-app.fr/login
4. Vous devez etre redirige vers le CAS
5. Apres authentification, vous revenez sur l'app

### Debug

Si ca ne marche pas, verifier :

1. **URL de callback** : doit correspondre exactement a ce qui est declare a la DSI
2. **Certificat SSL** : l'application doit etre en HTTPS en production
3. **Logs** : `docker-compose logs -f web`

---

## 7. Deploiement Docker en production

### docker-compose.prod.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - DB_HOST=db
      - DB_PORT=3306
      - DB_NAME=suivi_colis
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - CAS_DEV_MODE=false
      - CAS_SERVER=https://cas.univ-paris13.fr/cas
      - APP_URL=https://colis.iutv.univ-paris13.fr
    depends_on:
      db:
        condition: service_healthy
    restart: always

  db:
    image: mysql:8.0
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
    environment:
      - MYSQL_ROOT_PASSWORD=${DB_PASSWORD}
      - MYSQL_DATABASE=suivi_colis
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: always

volumes:
  mysql_data:
```

### Reverse proxy (Nginx)

L'application doit etre derriere un reverse proxy avec HTTPS :

```nginx
server {
    listen 443 ssl;
    server_name colis.iutv.univ-paris13.fr;
    
    ssl_certificate /etc/ssl/certs/votre-cert.pem;
    ssl_certificate_key /etc/ssl/private/votre-key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 8. Checklist de deploiement

- [ ] Application enregistree aupres de la DSI
- [ ] URL de callback declaree
- [ ] Certificat SSL installe
- [ ] `CAS_DEV_MODE=false`
- [ ] `APP_URL` correctement configure
- [ ] `SECRET_KEY` aleatoire et securise
- [ ] Utilisateur admin cree dans la base
- [ ] Test de connexion CAS reussi

---

## Support

Problemes courants :

| Erreur | Cause probable | Solution |
|--------|----------------|----------|
| "Pas de ticket CAS" | URL de callback incorrecte | Verifier APP_URL |
| "Ticket invalide" | Callback non autorise par la DSI | Contacter la DSI |
| "Non autorise" | Email pas dans la whitelist | Ajouter l'utilisateur |
| Boucle de redirection | Probleme de session/cookie | Verifier SECRET_KEY |

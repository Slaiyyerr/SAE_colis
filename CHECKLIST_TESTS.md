# 📋 CHECKLIST DE TESTS - Application Suivi Colis IUT

## 🔑 Comptes de test

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Admin | `admin@iutv.univ-paris13.fr` | `password` |
| Responsable Colis | `reprographie@iutv.univ-paris13.fr` | `password` |
| Éditeur | `compta@iutv.univ-paris13.fr` | `password` |
| Demandeur | `p.durand@iutv.univ-paris13.fr` | `password` |

---

## 1️⃣ AUTHENTIFICATION

### 1.1 Page de connexion
- [ ] La page `/login` s'affiche correctement
- [ ] Le formulaire contient email + mot de passe
- [ ] Les champs sont obligatoires (validation HTML)
- [ ] Le style de la page est correct (fond bleu, carte blanche)

### 1.2 Connexion valide
- [ ] Connexion avec `admin@iutv.univ-paris13.fr` / `password` → succès
- [ ] Connexion avec `reprographie@iutv.univ-paris13.fr` / `password` → succès
- [ ] Connexion avec `compta@iutv.univ-paris13.fr` / `password` → succès
- [ ] Connexion avec `p.durand@iutv.univ-paris13.fr` / `password` → succès
- [ ] Après connexion, redirection vers le tableau de bord

### 1.3 Connexion invalide
- [ ] Email incorrect → message d'erreur "Identifiants invalides"
- [ ] Mot de passe incorrect → message d'erreur "Identifiants invalides"
- [ ] Email vide → validation HTML empêche la soumission
- [ ] Mot de passe vide → validation HTML empêche la soumission

### 1.4 Déconnexion
- [ ] Clic sur "Se déconnecter" → retour à `/login`
- [ ] Après déconnexion, accès à `/` redirige vers `/login`
- [ ] Session détruite (impossible d'accéder aux pages protégées)

### 1.5 Protection des routes
- [ ] Accès à `/` sans connexion → redirection vers `/login`
- [ ] Accès à `/colis` sans connexion → redirection vers `/login`
- [ ] Accès à `/admin` sans connexion → redirection vers `/login`

---

## 2️⃣ NAVIGATION PAR RÔLE

### 2.1 Demandeur (p.durand@iutv.univ-paris13.fr)
- [ ] Navbar affiche : Tableau de bord, Mes colis, Mes commandes, Notifications
- [ ] Le titre de la navbar affiche "Demandeur"
- [ ] Pas d'accès à "Fournisseurs" dans le menu
- [ ] Pas d'accès à "Utilisateurs" dans le menu
- [ ] Pas d'accès à "Incidents" dans le menu
- [ ] Badge de notifications visible si notifications non lues

### 2.2 Éditeur (compta@iutv.univ-paris13.fr)
- [ ] Navbar affiche : Tableau de bord, Commandes, Fournisseurs
- [ ] Le titre de la navbar affiche "Éditeur"
- [ ] Pas d'accès à "Colis" dans le menu
- [ ] Pas d'accès à "Utilisateurs" dans le menu
- [ ] Pas d'accès à "Incidents" dans le menu

### 2.3 Responsable Colis (reprographie@iutv.univ-paris13.fr)
- [ ] Navbar affiche : Tableau de bord, Colis, Incidents, Scanner, Commandes
- [ ] Le titre de la navbar affiche "Responsable Colis"
- [ ] Pas d'accès à "Fournisseurs" dans le menu
- [ ] Pas d'accès à "Utilisateurs" dans le menu
- [ ] Lien "Incidents" présent et fonctionnel

### 2.4 Admin (admin@iutv.univ-paris13.fr)
- [ ] Navbar affiche : Tableau de bord, Colis, Commandes, Fournisseurs, Utilisateurs, Départements, Rapports
- [ ] Le titre de la navbar affiche "Administrateur"
- [ ] Tous les menus sont accessibles

---

## 3️⃣ TABLEAUX DE BORD

### 3.1 Tableau de bord Demandeur
- [ ] Message de bienvenue avec le prénom de l'utilisateur
- [ ] Stats : Mes commandes, Mes colis, En attente, Livrés
- [ ] Section "Mes colis en cours" avec liste des colis non livrés
- [ ] Section "Mes commandes récentes" avec 5 dernières commandes
- [ ] Section "Notifications récentes"
- [ ] Liens "Voir tous..." fonctionnels
- [ ] Seuls les colis/commandes du département de l'utilisateur sont affichés

### 3.2 Tableau de bord Éditeur
- [ ] Stats : Total commandes, À valider, Validées, Refusées, Fournisseurs
- [ ] Section "Commandes à valider" avec liste des BC en attente
- [ ] Section "Commandes par fournisseur" (top 5)
- [ ] Section "Actions rapides" avec boutons
- [ ] Bouton "+ Nouvelle commande" présent et fonctionnel
- [ ] Section "Dernières commandes créées"

### 3.3 Tableau de bord Responsable Colis
- [ ] Stats : Total colis, À réceptionner, À distribuer, En distribution, Incidents
- [ ] Section "Colis à réceptionner" avec liste
- [ ] Section "Colis à distribuer" avec liste
- [ ] Section "Incidents en cours" si colis en problème
- [ ] Bouton "Scanner un colis" présent
- [ ] Bouton "Incidents" avec compteur
- [ ] Section "Activité récente"

### 3.4 Tableau de bord Admin
- [ ] Stats globales : Commandes, Colis, En attente, À distribuer, Incidents
- [ ] Section "Colis par département" avec stats
- [ ] Section "Commandes par fournisseur" (top 5)
- [ ] Section "Utilisateurs" avec compteur
- [ ] Section "Référentiels" avec compteur départements
- [ ] Section "Administration" avec boutons d'actions
- [ ] Section "Activité récente du système"

---

## 4️⃣ GESTION DES COMMANDES

### 4.1 Liste des commandes
- [ ] `/commandes` affiche la liste des commandes
- [ ] Filtre par statut fonctionnel (paramètre ?statut=)
- [ ] Demandeur voit uniquement les commandes de son département
- [ ] Éditeur voit toutes les commandes
- [ ] Responsable colis voit toutes les commandes (lecture seule)
- [ ] Admin voit toutes les commandes

### 4.2 Détail d'une commande
- [ ] `/commandes/<id>` affiche les détails
- [ ] Numéro BC, fournisseur, département, date affichés
- [ ] Statut de la commande affiché
- [ ] Liste des articles (lignes de commande) affichée
- [ ] Liste des bons de livraison affichée
- [ ] Fichier BC téléchargeable si présent
- [ ] Demandeur ne peut pas modifier (pas de bouton Modifier)
- [ ] Responsable colis ne peut pas modifier (pas de bouton Modifier)

### 4.3 Création d'une commande (Éditeur, Admin)
- [ ] `/commandes/new` accessible uniquement pour éditeur et admin
- [ ] Formulaire avec : N° BC, Fournisseur, Département, Date prévue, Notes, Fichier
- [ ] Ajout d'articles dynamique (+ Ajouter une ligne)
- [ ] Validation des champs obligatoires
- [ ] Création réussie → redirection vers détail + message succès
- [ ] Upload de fichier BC fonctionnel (PDF, images)
- [ ] Demandeur ne peut PAS accéder à `/commandes/new` → erreur 403 ou redirection

### 4.4 Modification d'une commande (Éditeur, Admin)
- [ ] `/commandes/<id>/edit` accessible uniquement pour éditeur et admin
- [ ] Formulaire pré-rempli avec les données existantes
- [ ] Modification du statut possible (dropdown)
- [ ] **Statut "Non validée (refusée)" présent dans le dropdown**
- [ ] Modification fichier BC possible
- [ ] Sauvegarde réussie → redirection + message succès
- [ ] Demandeur ne peut PAS accéder → erreur 403

### 4.5 Suppression d'une commande (Admin uniquement)
- [ ] `/commandes/<id>/delete` accessible uniquement pour admin
- [ ] Page de confirmation affichée
- [ ] Warning sur suppression en cascade
- [ ] Suppression réussie → redirection + message succès
- [ ] Éditeur ne peut PAS supprimer
- [ ] Demandeur ne peut PAS supprimer

### 4.6 Statuts des commandes
- [ ] Statut "en_attente" affiché correctement
- [ ] Statut "validee" affiché correctement
- [ ] **Statut "non_validee" affiché correctement (nouveau)**
- [ ] Statut "en_cours" affiché correctement
- [ ] Statut "recue" affiché correctement
- [ ] Statut "annulee" affiché correctement

---

## 5️⃣ GESTION DES COLIS

### 5.1 Liste des colis
- [ ] `/colis` affiche la liste des colis
- [ ] Filtre par statut fonctionnel
- [ ] Demandeur voit uniquement les colis de son département
- [ ] Responsable colis voit tous les colis
- [ ] Admin voit tous les colis
- [ ] **Éditeur n'a PAS accès à `/colis`** → erreur 403

### 5.2 Détail d'un colis
- [ ] `/colis/<id>` affiche les détails
- [ ] N° suivi, transporteur, statut affichés
- [ ] Destination (département, lieu) affichée
- [ ] Bon de livraison lié affiché
- [ ] Commande liée affichée
- [ ] Historique des actions affiché
- [ ] Demandeur peut voir mais pas d'actions
- [ ] Responsable colis a les boutons d'actions

### 5.3 Actions sur les colis (Responsable, Admin)
- [ ] Bouton "Réceptionner" visible sur colis "attendu"
- [ ] Réceptionner → statut passe à "recu" + historique
- [ ] Bouton "Distribuer" visible sur colis "recu"
- [ ] Distribuer → statut passe à "en_distribution" + historique
- [ ] Bouton "Livrer" visible sur colis "en_distribution"
- [ ] Livrer → statut passe à "livre" + historique + notification demandeur
- [ ] Bouton "Signaler problème" visible
- [ ] Signaler problème → statut passe à "probleme" + historique
- [ ] Demandeur ne voit PAS les boutons d'actions

### 5.4 Création d'un colis (Responsable, Admin)
- [ ] `/bons-livraison/<id>/colis/new` accessible
- [ ] Formulaire avec : N° suivi, Transporteur, Notes
- [ ] Création réussie → redirection vers détail

### 5.5 Pages spéciales colis
- [ ] `/colis/en-attente` affiche les colis attendus
- [ ] `/colis/a-distribuer` affiche les colis reçus + en distribution
- [ ] `/colis/incidents` affiche les colis en problème
- [ ] `/colis/search` permet la recherche par n° suivi
- [ ] `/colis/scan` accessible (interface scanner)

### 5.6 Page Incidents (Responsable, Admin)
- [ ] `/colis/incidents` accessible pour responsable et admin
- [ ] Liste des colis avec statut "probleme"
- [ ] Bouton "Gérer" pour chaque colis
- [ ] Message si aucun incident
- [ ] Lien vers incidents dans la navbar responsable

---

## 6️⃣ GESTION DES FOURNISSEURS

### 6.1 Liste des fournisseurs
- [ ] `/fournisseurs` affiche la liste
- [ ] Accessible pour éditeur et admin
- [ ] **Non accessible pour demandeur et responsable colis**
- [ ] Nom, contact, téléphone, email affichés

### 6.2 Détail d'un fournisseur
- [ ] `/fournisseurs/<id>` affiche les détails
- [ ] Notes internes affichées
- [ ] Liste des commandes du fournisseur affichée

### 6.3 Création d'un fournisseur (Éditeur, Admin)
- [ ] `/fournisseurs/new` accessible
- [ ] Formulaire avec : Nom, Contact, Téléphone, Email, Notes
- [ ] Création réussie → redirection + message

### 6.4 Modification d'un fournisseur (Éditeur, Admin)
- [ ] `/fournisseurs/<id>/edit` accessible
- [ ] Formulaire pré-rempli
- [ ] Sauvegarde réussie

### 6.5 Suppression d'un fournisseur (Admin uniquement)
- [ ] Accessible uniquement pour admin
- [ ] Confirmation requise
- [ ] Éditeur ne peut PAS supprimer

---

## 7️⃣ GESTION DES BONS DE LIVRAISON

### 7.1 Création d'un BL
- [ ] Depuis le détail d'une commande
- [ ] Formulaire avec : N° BL fournisseur, Date, Fichier
- [ ] Création réussie → possibilité d'ajouter des colis

### 7.2 Détail d'un BL
- [ ] Affiche les informations du BL
- [ ] Liste des colis du BL
- [ ] Bouton "Ajouter un colis" (responsable, admin)

---

## 8️⃣ ADMINISTRATION

### 8.1 Gestion des utilisateurs (Admin)
- [ ] `/admin/utilisateurs` accessible uniquement pour admin
- [ ] Liste de tous les utilisateurs
- [ ] Bouton "Ajouter un utilisateur"
- [ ] Bouton "Modifier" par utilisateur
- [ ] Bouton "Activer/Désactiver" par utilisateur

### 8.2 Création d'un utilisateur
- [ ] `/admin/utilisateurs/new` accessible
- [ ] Formulaire : Email, Nom, Prénom, Rôle, Département, Mot de passe
- [ ] Sélection du rôle dans dropdown
- [ ] Sélection du département dans dropdown
- [ ] Création réussie → message avec mot de passe par défaut

### 8.3 Modification d'un utilisateur
- [ ] `/admin/utilisateurs/<id>/edit` accessible
- [ ] Modification du rôle possible
- [ ] Modification du département possible
- [ ] Réinitialisation mot de passe possible

### 8.4 Gestion des départements (Admin)
- [ ] `/admin/departements` accessible
- [ ] Liste des 6 départements
- [ ] Bouton "Ajouter un département"
- [ ] Bouton "Modifier" par département
- [ ] Bouton "Supprimer" par département

### 8.5 Création/Modification de département
- [ ] Formulaire : Nom, Lieu de livraison
- [ ] Création/modification réussie

### 8.6 Rapports (Admin)
- [ ] `/admin/reporting` accessible
- [ ] Stats par fournisseur affichées
- [ ] Stats par département affichées
- [ ] Données cohérentes avec la réalité

---

## 9️⃣ NOTIFICATIONS

### 9.1 Liste des notifications
- [ ] `/notifications` accessible pour tous les utilisateurs connectés
- [ ] Liste des notifications de l'utilisateur
- [ ] Notifications non lues mises en évidence
- [ ] Date et heure affichées

### 9.2 Badge dans la navbar
- [ ] Badge rouge affiché si notifications non lues
- [ ] Nombre de notifications affiché dans le badge
- [ ] Badge visible uniquement pour le demandeur (navbar)

### 9.3 Actions sur les notifications
- [ ] Clic sur notification → redirection vers le lien associé
- [ ] Bouton "Marquer comme lue" fonctionnel
- [ ] Bouton "Tout marquer comme lu" fonctionnel

### 9.4 Génération automatique
- [ ] Notification créée quand un colis est livré
- [ ] Notification envoyée au demandeur du département

---

## 🔟 CONTRÔLE D'ACCÈS (RBAC)

### 10.1 Demandeur - Restrictions
- [ ] Ne peut PAS créer de commande
- [ ] Ne peut PAS modifier de commande
- [ ] Ne peut PAS supprimer de commande
- [ ] Ne peut PAS accéder aux fournisseurs
- [ ] Ne peut PAS effectuer d'actions sur les colis
- [ ] Ne peut PAS accéder à l'administration
- [ ] Voit UNIQUEMENT les données de son département

### 10.2 Éditeur - Restrictions
- [ ] Peut créer des commandes ✓
- [ ] Peut modifier des commandes ✓
- [ ] Ne peut PAS supprimer de commande
- [ ] Peut gérer les fournisseurs ✓
- [ ] Ne peut PAS accéder aux colis
- [ ] Ne peut PAS accéder à l'administration
- [ ] Voit TOUTES les commandes (tous départements)

### 10.3 Responsable Colis - Restrictions
- [ ] Peut voir les commandes (lecture seule)
- [ ] Ne peut PAS créer/modifier de commande
- [ ] Peut gérer les colis ✓
- [ ] Peut effectuer toutes les actions sur les colis ✓
- [ ] Ne peut PAS accéder aux fournisseurs
- [ ] Ne peut PAS accéder à l'administration
- [ ] Voit TOUS les colis (tous départements)

### 10.4 Admin - Permissions complètes
- [ ] Accès à toutes les fonctionnalités
- [ ] Peut supprimer (commandes, fournisseurs, utilisateurs, départements)
- [ ] Accès aux rapports
- [ ] Gestion des utilisateurs
- [ ] Gestion des départements

---

## 1️⃣1️⃣ INTERFACE UTILISATEUR

### 11.1 Responsive
- [ ] Site utilisable sur desktop (1920px)
- [ ] Site utilisable sur tablette (768px)
- [ ] Site utilisable sur mobile (480px)
- [ ] Navbar s'adapte sur petit écran

### 11.2 Messages flash
- [ ] Messages de succès (vert) affichés correctement
- [ ] Messages d'erreur (rouge) affichés correctement
- [ ] Messages d'avertissement (jaune) affichés correctement

### 11.3 Tableaux
- [ ] Scroll horizontal si tableau trop large
- [ ] Headers fixes
- [ ] Données alignées correctement

### 11.4 Formulaires
- [ ] Labels clairs
- [ ] Champs obligatoires marqués avec *
- [ ] Validation côté client (HTML5)
- [ ] Messages d'erreur explicites

### 11.5 Navigation
- [ ] Logo cliquable → retour accueil
- [ ] Lien actif mis en évidence
- [ ] Fil d'Ariane si applicable
- [ ] Boutons "Retour" fonctionnels

---

## 1️⃣2️⃣ DONNÉES ET COHÉRENCE

### 12.1 Intégrité des données
- [ ] Suppression d'une commande supprime les BL et colis associés
- [ ] Suppression d'un BL supprime les colis associés
- [ ] Suppression d'un utilisateur ne casse pas les références

### 12.2 Historique
- [ ] Chaque action sur un colis est enregistrée
- [ ] Date/heure correcte
- [ ] Utilisateur qui a effectué l'action enregistré
- [ ] Ancien et nouveau statut enregistrés

### 12.3 Statistiques
- [ ] Compteurs cohérents avec les données
- [ ] Stats par statut correctes
- [ ] Stats par département correctes
- [ ] Stats par fournisseur correctes

---

## 1️⃣3️⃣ CAS LIMITES

### 13.1 Données vides
- [ ] Dashboard sans commande → message approprié
- [ ] Liste de colis vide → message "Aucun colis"
- [ ] Notifications vides → message approprié

### 13.2 Erreurs
- [ ] Accès à une commande inexistante → message d'erreur
- [ ] Accès à un colis inexistant → message d'erreur
- [ ] Accès non autorisé → redirection ou erreur 403

### 13.3 Upload de fichiers
- [ ] Fichier trop volumineux → message d'erreur
- [ ] Type de fichier non autorisé → message d'erreur
- [ ] Fichier uploadé accessible après création

---

## 📊 RÉSUMÉ DES TESTS

| Catégorie | Nombre de tests | Passés | Échoués |
|-----------|-----------------|--------|--------|
| Authentification | 18 | ☐ | ☐ |
| Navigation | 20 | ☐ | ☐ |
| Tableaux de bord | 28 | ☐ | ☐ |
| Commandes | 30 | ☐ | ☐ |
| Colis | 28 | ☐ | ☐ |
| Fournisseurs | 12 | ☐ | ☐ |
| Bons de livraison | 6 | ☐ | ☐ |
| Administration | 14 | ☐ | ☐ |
| Notifications | 10 | ☐ | ☐ |
| Contrôle d'accès | 20 | ☐ | ☐ |
| Interface | 15 | ☐ | ☐ |
| Données | 10 | ☐ | ☐ |
| Cas limites | 8 | ☐ | ☐ |
| **TOTAL** | **~220** | ☐ | ☐ |

---

## 🚀 Procédure de test recommandée

1. **Lancer l'application** : `docker-compose up --build`
2. **Tester chaque rôle séparément** (4 navigateurs ou fenêtres privées)
3. **Commencer par l'authentification**
4. **Puis tester la navigation et les tableaux de bord**
5. **Ensuite les fonctionnalités CRUD**
6. **Terminer par les cas limites et le contrôle d'accès**

Bonne session de tests ! 🧪

"""Modele Utilisateur.

Represente un utilisateur autorise a acceder a l'application.
Authentification par email + mot de passe.

Roles possibles :
- demandeur : consulte ses commandes/colis (lecture seule)
- editeur : cree/modifie les commandes et fournisseurs
- responsable_colis : gere les colis (reception, distribution, livraison)
- admin : acces complet + gestion des utilisateurs
"""


class Utilisateur:
    def __init__(self, data=None):
        """Constructeur depuis un dictionnaire (resultat SQL)."""
        data = data or {}
        self.id_utilisateur = data.get('id_utilisateur')
        self.email = data.get('email')
        self.mot_de_passe = data.get('mot_de_passe')  # Hash du mot de passe
        self.nom = data.get('nom')
        self.prenom = data.get('prenom')
        self.role = data.get('role', 'demandeur')
        self.id_departement = data.get('id_departement')
        self.est_actif = data.get('est_actif', True)
        self.date_creation = data.get('date_creation')
        # Champ optionnel depuis jointure
        self.nom_departement = data.get('nom_departement')

"""Modele HistoriqueColis.

Trace chaque evenement dans la vie d'un colis.
Permet de voir l'historique complet : qui a fait quoi et quand.

Exemples d'actions enregistrees :
- "Reception du colis"
- "Mise en distribution"
- "Livraison au secretariat GEA"
- "Probleme: Destinataire inconnu sur etiquette"
"""


class HistoriqueColis:
    def __init__(self, data=None):
        """Constructeur depuis un dictionnaire (resultat SQL)."""
        data = data or {}
        self.id_hist = data.get('id_hist')
        self.id_colis = data.get('id_colis')            # FK vers Colis
        self.id_utilisateur = data.get('id_utilisateur')  # Qui a fait l'action
        self.date_heure = data.get('date_heure')        # Quand
        self.action = data.get('action')                # Description de l'action
        self.ancien_statut = data.get('ancien_statut')  # Statut avant
        self.nouveau_statut = data.get('nouveau_statut')  # Statut apres
        # Infos utilisateur (via jointure)
        self.utilisateur_nom = data.get('utilisateur_nom')
        self.utilisateur_prenom = data.get('utilisateur_prenom')
    
    @property
    def utilisateur_complet(self):
        """Retourne le nom complet de l'utilisateur ou 'Systeme' si inconnu."""
        if self.utilisateur_prenom and self.utilisateur_nom:
            return f"{self.utilisateur_prenom} {self.utilisateur_nom}"
        elif self.utilisateur_nom:
            return self.utilisateur_nom
        return "Systeme"

"""Modele Notification.

Represente une notification envoyee a un utilisateur.
Les notifications sont creees automatiquement lors des changements de statut des colis.

Exemples :
- "Votre colis est arrive a la reprographie"
- "Votre colis a ete livre"
- "Un probleme a ete signale sur votre colis"
"""


class Notification:
    def __init__(self, data=None):
        """Constructeur depuis un dictionnaire (resultat SQL)."""
        data = data or {}
        self.id_notification = data.get('id_notification')
        self.id_utilisateur = data.get('id_utilisateur')  # Destinataire de la notif
        self.titre = data.get('titre')                    # Ex: "Colis CHRO-FR-789456123"
        self.message = data.get('message')                # Ex: "Votre colis est arrive"
        self.lien = data.get('lien')                      # URL vers le detail (ex: /colis/1)
        self.est_lue = data.get('est_lue', False)         # True si l'utilisateur l'a vue
        self.date_creation = data.get('date_creation')

"""Modele Colis.

Represente un colis physique recu a la reprographie.
C'est l'entite centrale pour le suivi : on trace son parcours de la reception a la livraison.

Statuts possibles :
- attendu : BL cree, colis pas encore arrive
- recu : colis arrive a la reprographie
- en_distribution : colis en cours de livraison vers le departement
- livre : colis remis au destinataire
- probleme : anomalie (destinataire inconnu, colis endommage, etc.)
"""


class Colis:
    def __init__(self, data=None):
        """Constructeur depuis un dictionnaire (resultat SQL)."""
        data = data or {}
        self.id_colis = data.get('id_colis')
        self.id_bl = data.get('id_bl')                      # FK vers BonLivraison
        self.num_suivi_transporteur = data.get('num_suivi_transporteur')  # Ex: "CHRO-FR-789456123"
        self.nom_transporteur = data.get('nom_transporteur')  # Ex: "Chronopost", "La Poste"
        self.statut_actuel = data.get('statut_actuel', 'attendu')
        self.lieu_stockage = data.get('lieu_stockage')      # Ou est le colis actuellement
        self.date_reception = data.get('date_reception')    # Quand il est arrive
        self.date_livraison = data.get('date_livraison')    # Quand il a ete livre
        self.notes = data.get('notes')

"""Modele BonLivraison.

Represente un bon de livraison recu du fournisseur.
Une commande peut avoir plusieurs BL (livraisons partielles).
Chaque BL peut contenir plusieurs colis.

Relation : Commande (1) -> BonLivraison (N) -> Colis (N)
"""


class BonLivraison:
    def __init__(self, data=None):
        """Constructeur depuis un dictionnaire (resultat SQL)."""
        data = data or {}
        self.id_bl = data.get('id_bl')
        self.id_commande = data.get('id_commande')          # FK vers Commande
        self.num_bl_fournisseur = data.get('num_bl_fournisseur')  # Numero BL du fournisseur
        self.date_bl = data.get('date_bl')                  # Date sur le BL
        self.fichier_bl = data.get('fichier_bl')            # Chemin vers le PDF/image uploade
        self.date_reception = data.get('date_reception')    # Date d'enregistrement dans l'app

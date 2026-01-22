"""Modele LigneCommande.

Represente un article dans une commande.
Une commande contient une ou plusieurs lignes (ex: 12 PC + 12 ecrans).
"""


class LigneCommande:
    def __init__(self, data=None):
        """Constructeur depuis un dictionnaire (resultat SQL)."""
        data = data or {}
        self.id_ligne = data.get('id_ligne')
        self.id_commande = data.get('id_commande')    # FK vers Commande
        self.ref_produit = data.get('ref_produit')    # Reference fournisseur (optionnel)
        self.designation = data.get('designation')     # Description de l'article
        self.quantite = data.get('quantite', 1)

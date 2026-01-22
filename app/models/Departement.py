"""Modele Departement.

Represente un departement de l'IUT (Informatique, GEA, GEII, etc.).
Chaque departement a un lieu de livraison specifique (batiment, etage, bureau).
"""


class Departement:
    def __init__(self, data=None):
        """Constructeur depuis un dictionnaire (resultat SQL)."""
        data = data or {}
        self.id_departement = data.get('id_departement')
        self.nom_departement = data.get('nom_departement')  # Ex: "Informatique"
        self.lieu_livraison = data.get('lieu_livraison')    # Ex: "Batiment A - 2eme etage"

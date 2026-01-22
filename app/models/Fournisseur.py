"""Modele Fournisseur.

Represente une entreprise aupres de laquelle l'IUT passe des commandes.
Contient les coordonnees et notes internes sur le fournisseur.
"""


class Fournisseur:
    def __init__(self, data=None):
        """Constructeur depuis un dictionnaire (resultat SQL)."""
        data = data or {}
        self.id_fournisseur = data.get('id_fournisseur')
        self.nom_societe = data.get('nom_societe')      # Ex: "LDLC Pro"
        self.contact_nom = data.get('contact_nom')      # Nom du contact commercial
        self.telephone = data.get('telephone')
        self.email = data.get('email')
        self.notes_internes = data.get('notes_internes')  # Remarques privees (delais, problemes...)

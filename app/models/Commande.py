"""Modele Commande (Bon de Commande).

Represente une commande passee aupres d'un fournisseur.
Une commande peut generer plusieurs bons de livraison (livraisons partielles).

Statuts possibles :
- en_attente : commande creee, pas encore validee
- validee : commande approuvee, en attente d'expedition
- en_cours : au moins un colis en transit
- recue : tous les colis livres
- annulee : commande annulee
"""


class Commande:
    def __init__(self, data=None):
        """Constructeur depuis un dictionnaire (resultat SQL)."""
        data = data or {}
        self.id_commande = data.get('id_commande')
        self.numero_bc = data.get('numero_bc')          # Numero unique du bon de commande
        self.id_fournisseur = data.get('id_fournisseur')
        self.id_departement = data.get('id_departement')  # Departement destinataire
        self.id_demandeur = data.get('id_demandeur')      # Utilisateur qui a fait la demande
        self.date_creation = data.get('date_creation')
        self.date_livraison_prevue = data.get('date_livraison_prevue')
        self.statut_global = data.get('statut_global', 'en_attente')
        self.notes = data.get('notes')
        self.fichier_bc = data.get('fichier_bc')  # Chemin vers le PDF/image du BC uploade
        
        # Champs issus des jointures (optionnels)
        self.fournisseur_nom = data.get('fournisseur_nom')
        self.departement_nom = data.get('departement_nom')
        self.demandeur_nom = data.get('demandeur_nom')

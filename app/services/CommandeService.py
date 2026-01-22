"""Service pour la gestion des commandes (bons de commande).

Gere la logique metier des commandes :
- Creation avec lignes de commande
- Recuperation des BL associes
- Statistiques
"""

from app.dao.CommandeDAO import CommandeDAO
from app.dao.LigneCommandeDAO import LigneCommandeDAO
from app.dao.BonLivraisonDAO import BonLivraisonDAO


class CommandeService:
    def __init__(self):
        self.dao = CommandeDAO()
        self.ligne_dao = LigneCommandeDAO()
        self.bl_dao = BonLivraisonDAO()
    
    def getAll(self):
        """Retourne toutes les commandes."""
        return self.dao.find_all()
    
    def getById(self, id):
        """Retourne une commande par ID."""
        return self.dao.find_by_id(id)
    
    def getByNumero(self, numero_bc):
        """Retourne une commande par numero BC."""
        return self.dao.find_by_numero(numero_bc)
    
    def getByStatut(self, statut):
        """Retourne les commandes ayant un statut specifique."""
        return self.dao.find_by_statut(statut)
    
    def getByDepartement(self, id_departement):
        """Retourne les commandes d'un departement."""
        return self.dao.find_by_departement(id_departement)
    
    def getByFournisseur(self, id_fournisseur):
        """Retourne les commandes d'un fournisseur."""
        return self.dao.find_by_fournisseur(id_fournisseur)
    
    def getLignes(self, id_commande):
        """Retourne les lignes (articles) d'une commande."""
        return self.ligne_dao.find_by_commande(id_commande)
    
    def getBonsLivraison(self, id_commande):
        """Retourne les bons de livraison d'une commande."""
        return self.bl_dao.find_by_commande(id_commande)
    
    def countByStatut(self):
        """Retourne le nombre de commandes par statut (pour le dashboard)."""
        return self.dao.count_by_statut()
    
    def countByStatutAndDepartement(self, id_departement):
        """Retourne le nombre de commandes par statut pour un departement."""
        return self.dao.count_by_statut_and_departement(id_departement)
    
    def create(self, form, lignes=None):
        """Cree une commande avec ses lignes.
        
        Args:
            form: Donnees de la commande
            lignes: Liste de dicts {'ref_produit', 'designation', 'quantite'}
        
        Returns:
            ID de la commande creee
        """
        # Creer la commande
        id_commande = self.dao.create(form)
        
        # Creer les lignes de commande
        if lignes:
            for ligne in lignes:
                ligne['id_commande'] = id_commande
                self.ligne_dao.create(ligne)
        
        return id_commande
    
    def update(self, id, form):
        """Met a jour une commande."""
        return self.dao.update(id, form)
    
    def delete(self, id):
        """Supprime une commande (et ses lignes, BL, colis en cascade)."""
        return self.dao.delete(id)
    
    def getStats(self):
        """Retourne les statistiques pour le dashboard."""
        return self.dao.count_by_statut()

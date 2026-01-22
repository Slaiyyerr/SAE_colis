"""Service pour la gestion de l'historique des colis.

Couche metier entre les controllers et le DAO.
"""

from app.dao.HistoriqueColisDAO import HistoriqueColisDAO


class HistoriqueColisService:
    def __init__(self):
        self.dao = HistoriqueColisDAO()
    
    def getByColis(self, id_colis):
        """Retourne l'historique d'un colis."""
        return self.dao.find_by_colis(id_colis)
    
    def getRecent(self, limit=10):
        """Retourne les dernieres entrees d'historique."""
        return self.dao.find_recent(limit)
    
    def getRecentByDepartement(self, id_departement, limit=10):
        """Retourne les dernieres entrees d'historique pour un departement."""
        return self.dao.find_recent_by_departement(id_departement, limit)
    
    def create(self, form):
        """Cree une entree d'historique."""
        return self.dao.create(form)
    
    def logReception(self, id_colis, id_utilisateur):
        """Enregistre une reception."""
        return self.dao.log_reception(id_colis, id_utilisateur)
    
    def logChangementStatut(self, id_colis, id_utilisateur, ancien, nouveau):
        """Enregistre un changement de statut."""
        return self.dao.log_changement_statut(id_colis, id_utilisateur, ancien, nouveau)
    
    def logLivraison(self, id_colis, id_utilisateur, lieu=None):
        """Enregistre une livraison."""
        return self.dao.log_livraison(id_colis, id_utilisateur, lieu)

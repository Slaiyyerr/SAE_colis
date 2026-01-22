"""Service pour la logique métier des colis."""

from app.dao.ParcelSqlDAO import ParcelSqlDAO


class ParcelService:
    """Service gérant les opérations sur les colis."""
    
    def __init__(self):
        self.dao = ParcelSqlDAO()
    
    def get_all_parcels(self):
        """Récupère tous les colis."""
        return self.dao.find_all()
    
    def get_parcel_by_id(self, parcel_id):
        """Récupère un colis par son ID."""
        return self.dao.find_by_id(parcel_id)
    
    def receive_parcel(self, parcel_id):
        """Marque un colis comme reçu."""
        return self.dao.update_status(parcel_id, 'received')
    
    def deliver_parcel(self, parcel_id):
        """Marque un colis comme livré."""
        return self.dao.update_status(parcel_id, 'delivered')
    
    def get_parcels_by_status(self, status):
        """Récupère les colis par statut."""
        return self.dao.find_by_status(status)
    
    def get_delayed_parcels(self):
        """Récupère les colis en retard."""
        return self.dao.find_delayed()

"""DAO pour les colis."""

from app.dao.DatabaseConnection import DatabaseConnection
from app.models.Parcel import Parcel


class ParcelSqlDAO:
    """Data Access Object pour les colis."""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def find_all(self):
        """Récupère tous les colis."""
        # TODO: Implémenter
        return []
    
    def find_by_id(self, parcel_id):
        """Récupère un colis par son ID."""
        # TODO: Implémenter
        return None
    
    def find_by_status(self, status):
        """Récupère les colis par statut."""
        # TODO: Implémenter
        return []
    
    def find_delayed(self):
        """Récupère les colis en retard."""
        # TODO: Implémenter
        return []
    
    def update_status(self, parcel_id, status):
        """Met à jour le statut d'un colis."""
        # TODO: Implémenter
        pass

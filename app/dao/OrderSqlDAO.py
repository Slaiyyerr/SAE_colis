"""DAO pour les bons de commande."""

from app.dao.DatabaseConnection import DatabaseConnection
from app.models.Order import Order


class OrderSqlDAO:
    """Data Access Object pour les bons de commande."""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def find_all(self):
        """Récupère tous les bons de commande."""
        # TODO: Implémenter
        return []
    
    def find_by_id(self, order_id):
        """Récupère un bon de commande par son ID."""
        # TODO: Implémenter
        return None
    
    def create(self, data):
        """Crée un nouveau bon de commande."""
        # TODO: Implémenter
        pass
    
    def update(self, order_id, data):
        """Met à jour un bon de commande."""
        # TODO: Implémenter
        pass
    
    def delete(self, order_id):
        """Supprime un bon de commande."""
        # TODO: Implémenter
        pass

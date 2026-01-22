"""DAO pour les fournisseurs."""

from app.dao.DatabaseConnection import DatabaseConnection
from app.models.Supplier import Supplier


class SupplierSqlDAO:
    """Data Access Object pour les fournisseurs."""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def find_all(self):
        """Récupère tous les fournisseurs."""
        # TODO: Implémenter
        return []
    
    def find_by_id(self, supplier_id):
        """Récupère un fournisseur par son ID."""
        # TODO: Implémenter
        return None
    
    def create(self, data):
        """Crée un nouveau fournisseur."""
        # TODO: Implémenter
        pass
    
    def update(self, supplier_id, data):
        """Met à jour un fournisseur."""
        # TODO: Implémenter
        pass
    
    def delete(self, supplier_id):
        """Supprime un fournisseur."""
        # TODO: Implémenter
        pass

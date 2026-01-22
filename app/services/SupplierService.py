"""Service pour la logique métier des fournisseurs."""

from app.dao.SupplierSqlDAO import SupplierSqlDAO


class SupplierService:
    """Service gérant les opérations sur les fournisseurs."""
    
    def __init__(self):
        self.dao = SupplierSqlDAO()
    
    def get_all_suppliers(self):
        """Récupère tous les fournisseurs."""
        return self.dao.find_all()
    
    def get_supplier_by_id(self, supplier_id):
        """Récupère un fournisseur par son ID."""
        return self.dao.find_by_id(supplier_id)
    
    def create_supplier(self, data):
        """Crée un nouveau fournisseur."""
        return self.dao.create(data)
    
    def update_supplier(self, supplier_id, data):
        """Met à jour un fournisseur."""
        return self.dao.update(supplier_id, data)
    
    def delete_supplier(self, supplier_id):
        """Supprime un fournisseur."""
        return self.dao.delete(supplier_id)

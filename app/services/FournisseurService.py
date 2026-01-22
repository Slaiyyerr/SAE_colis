"""Service pour la gestion des fournisseurs.

Couche metier entre les controllers et le DAO.
"""

from app.dao.FournisseurDAO import FournisseurDAO


class FournisseurService:
    def __init__(self):
        self.dao = FournisseurDAO()
    
    def getAll(self):
        """Retourne tous les fournisseurs."""
        return self.dao.find_all()
    
    def getById(self, id):
        """Retourne un fournisseur par ID."""
        return self.dao.find_by_id(id)
    
    def create(self, form):
        """Cree un nouveau fournisseur."""
        return self.dao.create(form)
    
    def update(self, id, form):
        """Met a jour un fournisseur."""
        return self.dao.update(id, form)
    
    def delete(self, id):
        """Supprime un fournisseur."""
        return self.dao.delete(id)

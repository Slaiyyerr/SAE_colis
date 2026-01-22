"""Service pour la gestion des departements.

Couche metier entre les controllers et le DAO.
"""

from app.dao.DepartementDAO import DepartementDAO


class DepartementService:
    def __init__(self):
        self.dao = DepartementDAO()
    
    def getAll(self):
        """Retourne tous les departements."""
        return self.dao.find_all()
    
    def getById(self, id):
        """Retourne un departement par ID."""
        return self.dao.find_by_id(id)
    
    def create(self, form):
        """Cree un nouveau departement."""
        return self.dao.create(form)
    
    def update(self, id, form):
        """Met a jour un departement."""
        return self.dao.update(id, form)
    
    def delete(self, id):
        """Supprime un departement."""
        return self.dao.delete(id)

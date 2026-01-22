"""Service pour la gestion des utilisateurs.

Couche metier entre les controllers et le DAO.
Pour l'instant, delegation simple vers le DAO.
"""

from app.dao.UtilisateurDAO import UtilisateurDAO


class UtilisateurService:
    def __init__(self):
        self.dao = UtilisateurDAO()
    
    def getAll(self):
        """Retourne tous les utilisateurs."""
        return self.dao.find_all()
    
    def getById(self, id):
        """Retourne un utilisateur par ID."""
        return self.dao.find_by_id(id)
    
    def getByEmail(self, email):
        """Retourne un utilisateur par email (pour authentification CAS)."""
        return self.dao.find_by_email(email)
    
    def getByRole(self, role):
        """Retourne les utilisateurs ayant un role specifique."""
        return self.dao.find_by_role(role)
    
    def getActifs(self):
        """Retourne les utilisateurs actifs uniquement."""
        return self.dao.find_actifs()
    
    def create(self, form):
        """Cree un nouvel utilisateur."""
        return self.dao.create(form)
    
    def update(self, id, form):
        """Met a jour un utilisateur."""
        return self.dao.update(id, form)
    
    def activer(self, id):
        """Active un utilisateur."""
        return self.dao.set_actif(id, True)
    
    def desactiver(self, id):
        """Desactive un utilisateur (sans le supprimer)."""
        return self.dao.set_actif(id, False)
    
    def delete(self, id):
        """Supprime definitivement un utilisateur."""
        return self.dao.delete(id)

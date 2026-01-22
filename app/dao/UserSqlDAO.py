"""DAO pour les utilisateurs."""

from app.dao.DatabaseConnection import DatabaseConnection
from app.models.User import User


class UserSqlDAO:
    """Data Access Object pour les utilisateurs."""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def find_all(self):
        """Récupère tous les utilisateurs."""
        # TODO: Implémenter
        return []
    
    def find_by_id(self, user_id):
        """Récupère un utilisateur par son ID."""
        # TODO: Implémenter
        return None
    
    def find_by_username(self, username):
        """Récupère un utilisateur par son nom d'utilisateur."""
        # TODO: Implémenter
        return None
    
    def create(self, data):
        """Crée un nouvel utilisateur."""
        # TODO: Implémenter
        pass
    
    def update(self, user_id, data):
        """Met à jour un utilisateur."""
        # TODO: Implémenter
        pass
    
    def update_role(self, user_id, role):
        """Met à jour le rôle d'un utilisateur."""
        # TODO: Implémenter
        pass

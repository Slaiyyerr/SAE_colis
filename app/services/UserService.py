"""Service pour la logique métier des utilisateurs."""

from app.dao.UserSqlDAO import UserSqlDAO


class UserService:
    """Service gérant les opérations sur les utilisateurs."""
    
    def __init__(self):
        self.dao = UserSqlDAO()
    
    def get_all_users(self):
        """Récupère tous les utilisateurs."""
        return self.dao.find_all()
    
    def get_user_by_id(self, user_id):
        """Récupère un utilisateur par son ID."""
        return self.dao.find_by_id(user_id)
    
    def get_user_by_username(self, username):
        """Récupère un utilisateur par son nom d'utilisateur."""
        return self.dao.find_by_username(username)
    
    def create_user(self, data):
        """Crée un nouvel utilisateur."""
        return self.dao.create(data)
    
    def update_user(self, user_id, data):
        """Met à jour un utilisateur."""
        return self.dao.update(user_id, data)
    
    def update_user_role(self, user_id, role):
        """Met à jour le rôle d'un utilisateur."""
        return self.dao.update_role(user_id, role)

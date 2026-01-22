"""Service pour la logique métier des bons de commande."""

from app.dao.OrderSqlDAO import OrderSqlDAO


class OrderService:
    """Service gérant les opérations sur les bons de commande."""
    
    def __init__(self):
        self.dao = OrderSqlDAO()
    
    def get_all_orders(self):
        """Récupère tous les bons de commande."""
        return self.dao.find_all()
    
    def get_order_by_id(self, order_id):
        """Récupère un bon de commande par son ID."""
        return self.dao.find_by_id(order_id)
    
    def create_order(self, data):
        """Crée un nouveau bon de commande."""
        return self.dao.create(data)
    
    def update_order(self, order_id, data):
        """Met à jour un bon de commande."""
        return self.dao.update(order_id, data)
    
    def delete_order(self, order_id):
        """Supprime un bon de commande."""
        return self.dao.delete(order_id)

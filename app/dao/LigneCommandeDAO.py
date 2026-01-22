"""DAO pour la table ligne_commande.

Gere les articles d'une commande.
"""

from app.dao.DatabaseConnection import db
from app.models.LigneCommande import LigneCommande


class LigneCommandeDAO:
    
    def find_by_commande(self, id_commande):
        """Retourne toutes les lignes d'une commande."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM ligne_commande WHERE id_commande = %s ORDER BY id_ligne", (id_commande,))
            rows = cursor.fetchall()
            return [LigneCommande(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def create(self, form):
        """Cree une nouvelle ligne de commande."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "INSERT INTO ligne_commande (id_commande, ref_produit, designation, quantite) VALUES (%s, %s, %s, %s)",
                (form.get('id_commande'), form.get('ref_produit'), form.get('designation'), form.get('quantite', 1))
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def delete_by_commande(self, id_commande):
        """Supprime toutes les lignes d'une commande."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM ligne_commande WHERE id_commande = %s", (id_commande,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

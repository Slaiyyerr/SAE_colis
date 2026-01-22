"""DAO pour la table departement.

Gere les operations CRUD sur les departements de l'IUT.
"""

from app.dao.DatabaseConnection import db
from app.models.Departement import Departement


class DepartementDAO:
    
    def find_all(self):
        """Retourne tous les departements."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM departement ORDER BY nom_departement")
            rows = cursor.fetchall()
            return [Departement(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_id(self, id):
        """Retourne un departement par son ID, ou None si non trouve."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM departement WHERE id_departement = %s", (id,))
            row = cursor.fetchone()
            return Departement(row) if row else None
        finally:
            cursor.close()
            conn.close()
    
    def create(self, form):
        """Cree un nouveau departement. Retourne l'ID cree."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "INSERT INTO departement (nom_departement, lieu_livraison) VALUES (%s, %s)",
                (form.get('nom_departement'), form.get('lieu_livraison'))
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def update(self, id, form):
        """Met a jour un departement existant."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "UPDATE departement SET nom_departement = %s, lieu_livraison = %s WHERE id_departement = %s",
                (form.get('nom_departement'), form.get('lieu_livraison'), id)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def delete(self, id):
        """Supprime un departement."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM departement WHERE id_departement = %s", (id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

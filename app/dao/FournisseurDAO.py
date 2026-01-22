"""DAO pour la table fournisseur.

Gere les operations CRUD sur les fournisseurs.
"""

from app.dao.DatabaseConnection import db
from app.models.Fournisseur import Fournisseur


class FournisseurDAO:
    
    def find_all(self):
        """Retourne tous les fournisseurs tries par nom."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM fournisseur ORDER BY nom_societe")
            rows = cursor.fetchall()
            return [Fournisseur(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_id(self, id):
        """Retourne un fournisseur par son ID, ou None."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM fournisseur WHERE id_fournisseur = %s", (id,))
            row = cursor.fetchone()
            return Fournisseur(row) if row else None
        finally:
            cursor.close()
            conn.close()
    
    def create(self, form):
        """Cree un nouveau fournisseur. Retourne l'ID cree."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """INSERT INTO fournisseur (nom_societe, contact_nom, telephone, email, notes_internes) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (form.get('nom_societe'), form.get('contact_nom'), form.get('telephone'),
                 form.get('email'), form.get('notes_internes'))
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
        """Met a jour un fournisseur existant."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """UPDATE fournisseur 
                   SET nom_societe = %s, contact_nom = %s, telephone = %s, email = %s, notes_internes = %s 
                   WHERE id_fournisseur = %s""",
                (form.get('nom_societe'), form.get('contact_nom'), form.get('telephone'),
                 form.get('email'), form.get('notes_internes'), id)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def delete(self, id):
        """Supprime un fournisseur. Attention: CASCADE sur les commandes!"""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM fournisseur WHERE id_fournisseur = %s", (id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

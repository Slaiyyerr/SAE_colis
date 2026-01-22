"""DAO pour la table bon_livraison.

Gere les bons de livraison recus des fournisseurs.
Un BL est rattache a une commande et peut contenir plusieurs colis.
"""

from app.dao.DatabaseConnection import db
from app.models.BonLivraison import BonLivraison


class BonLivraisonDAO:
    
    def find_all(self):
        """Retourne tous les BL (plus recents en premier)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM bon_livraison ORDER BY date_reception DESC")
            rows = cursor.fetchall()
            return [BonLivraison(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_id(self, id):
        """Retourne un BL par son ID, ou None."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM bon_livraison WHERE id_bl = %s", (id,))
            row = cursor.fetchone()
            return BonLivraison(row) if row else None
        finally:
            cursor.close()
            conn.close()
    
    def find_by_commande(self, id_commande):
        """Retourne tous les BL d'une commande."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM bon_livraison WHERE id_commande = %s ORDER BY date_reception DESC",
                (id_commande,)
            )
            rows = cursor.fetchall()
            return [BonLivraison(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def create(self, form):
        """Cree un nouveau BL. Retourne l'ID cree."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "INSERT INTO bon_livraison (id_commande, num_bl_fournisseur, date_bl, fichier_bl) VALUES (%s, %s, %s, %s)",
                (form.get('id_commande'), form.get('num_bl_fournisseur'),
                 form.get('date_bl'), form.get('fichier_bl'))
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
        """Met a jour un BL existant."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            fields = []
            values = []
            for key in ['num_bl_fournisseur', 'date_bl', 'fichier_bl']:
                if key in form:
                    fields.append(f"{key} = %s")
                    values.append(form[key] if form[key] != '' else None)
            values.append(id)
            cursor.execute(f"UPDATE bon_livraison SET {', '.join(fields)} WHERE id_bl = %s", values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def delete(self, id):
        """Supprime un BL (CASCADE sur les colis)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM bon_livraison WHERE id_bl = %s", (id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

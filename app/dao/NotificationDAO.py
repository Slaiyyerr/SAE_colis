"""DAO pour la table notification.

Gere les notifications envoyees aux utilisateurs.
Les notifications sont creees automatiquement lors des changements de statut.
"""

from app.dao.DatabaseConnection import db
from app.models.Notification import Notification


class NotificationDAO:
    
    def find_by_utilisateur(self, id_utilisateur, limit=50):
        """Retourne les notifications d'un utilisateur (plus recentes en premier)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM notification WHERE id_utilisateur = %s ORDER BY date_creation DESC LIMIT %s",
                (id_utilisateur, limit)
            )
            rows = cursor.fetchall()
            return [Notification(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_non_lues(self, id_utilisateur):
        """Retourne les notifications non lues d'un utilisateur."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM notification WHERE id_utilisateur = %s AND est_lue = FALSE ORDER BY date_creation DESC",
                (id_utilisateur,)
            )
            rows = cursor.fetchall()
            return [Notification(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def count_non_lues(self, id_utilisateur):
        """Compte les notifications non lues (pour le badge)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT COUNT(*) as count FROM notification WHERE id_utilisateur = %s AND est_lue = FALSE",
                (id_utilisateur,)
            )
            result = cursor.fetchone()
            return result['count'] if result else 0
        finally:
            cursor.close()
            conn.close()
    
    def find_by_id(self, id_notification):
        """Retourne une notification par son ID."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM notification WHERE id_notification = %s", (id_notification,))
            row = cursor.fetchone()
            return Notification(row) if row else None
        finally:
            cursor.close()
            conn.close()
    
    def create(self, form):
        """Cree une nouvelle notification."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "INSERT INTO notification (id_utilisateur, titre, message, lien) VALUES (%s, %s, %s, %s)",
                (form.get('id_utilisateur'), form.get('titre'), form.get('message'), form.get('lien'))
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def marquer_lue(self, id_notification):
        """Marque une notification comme lue."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE notification SET est_lue = TRUE WHERE id_notification = %s", (id_notification,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def marquer_toutes_lues(self, id_utilisateur):
        """Marque toutes les notifications d'un utilisateur comme lues."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE notification SET est_lue = TRUE WHERE id_utilisateur = %s", (id_utilisateur,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def delete(self, id_notification):
        """Supprime une notification."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM notification WHERE id_notification = %s", (id_notification,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def delete_anciennes(self, jours=30):
        """Supprime les notifications de plus de X jours (nettoyage)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "DELETE FROM notification WHERE date_creation < DATE_SUB(NOW(), INTERVAL %s DAY)",
                (jours,)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

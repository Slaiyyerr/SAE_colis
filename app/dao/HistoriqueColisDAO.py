"""DAO pour la table historique_colis.

Enregistre chaque evenement dans la vie d'un colis.
Permet la tracabilite complete des actions.
"""

from app.dao.DatabaseConnection import db
from app.models.HistoriqueColis import HistoriqueColis


class HistoriqueColisDAO:
    
    def find_by_colis(self, id_colis):
        """Retourne l'historique d'un colis avec les infos utilisateur (plus recent en premier)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT hc.*, u.nom as utilisateur_nom, u.prenom as utilisateur_prenom
                FROM historique_colis hc
                LEFT JOIN utilisateur u ON hc.id_utilisateur = u.id_utilisateur
                WHERE hc.id_colis = %s 
                ORDER BY hc.date_heure DESC
            """, (id_colis,))
            rows = cursor.fetchall()
            return [HistoriqueColis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_recent(self, limit=10):
        """Retourne les dernieres entrees d'historique avec infos utilisateur (pour le dashboard)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT hc.*, u.nom as utilisateur_nom, u.prenom as utilisateur_prenom
                FROM historique_colis hc
                LEFT JOIN utilisateur u ON hc.id_utilisateur = u.id_utilisateur
                ORDER BY hc.date_heure DESC 
                LIMIT %s
            """, (limit,))
            rows = cursor.fetchall()
            return [HistoriqueColis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_recent_by_departement(self, id_departement, limit=10):
        """Retourne les dernieres entrees d'historique pour un departement.
        
        Jointure : historique_colis -> colis -> bon_livraison -> commande -> departement
        """
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT hc.*, u.nom as utilisateur_nom, u.prenom as utilisateur_prenom
                FROM historique_colis hc
                LEFT JOIN utilisateur u ON hc.id_utilisateur = u.id_utilisateur
                JOIN colis c ON hc.id_colis = c.id_colis
                JOIN bon_livraison bl ON c.id_bl = bl.id_bl
                JOIN commande cmd ON bl.id_commande = cmd.id_commande
                WHERE cmd.id_departement = %s
                ORDER BY hc.date_heure DESC 
                LIMIT %s
            """, (id_departement, limit))
            rows = cursor.fetchall()
            return [HistoriqueColis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def create(self, form):
        """Cree une nouvelle entree d'historique."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """INSERT INTO historique_colis (id_colis, id_utilisateur, action, ancien_statut, nouveau_statut) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (form.get('id_colis'), form.get('id_utilisateur'), form.get('action'),
                 form.get('ancien_statut'), form.get('nouveau_statut'))
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def log_reception(self, id_colis, id_utilisateur):
        """Raccourci : enregistre une reception de colis."""
        return self.create({
            'id_colis': id_colis,
            'id_utilisateur': id_utilisateur,
            'action': 'Reception du colis',
            'ancien_statut': 'attendu',
            'nouveau_statut': 'recu'
        })
    
    def log_changement_statut(self, id_colis, id_utilisateur, ancien, nouveau):
        """Raccourci : enregistre un changement de statut."""
        return self.create({
            'id_colis': id_colis,
            'id_utilisateur': id_utilisateur,
            'action': 'Changement de statut',
            'ancien_statut': ancien,
            'nouveau_statut': nouveau
        })
    
    def log_livraison(self, id_colis, id_utilisateur, lieu=None):
        """Raccourci : enregistre une livraison."""
        action = 'Livraison' + (f' a {lieu}' if lieu else '')
        return self.create({
            'id_colis': id_colis,
            'id_utilisateur': id_utilisateur,
            'action': action,
            'ancien_statut': 'en_distribution',
            'nouveau_statut': 'livre'
        })
    
    def log_resolution_probleme(self, id_colis, id_utilisateur, nouveau_statut='recu'):
        """Raccourci : enregistre une resolution de probleme."""
        return self.create({
            'id_colis': id_colis,
            'id_utilisateur': id_utilisateur,
            'action': 'Resolution du probleme',
            'ancien_statut': 'probleme',
            'nouveau_statut': nouveau_statut
        })

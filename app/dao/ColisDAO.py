"""DAO pour la table colis.

Gere les colis physiques recus a la reprographie.
C'est l'entite principale pour le suivi.
"""

from app.dao.DatabaseConnection import db
from app.models.Colis import Colis


class ColisDAO:
    
    def _base_query_with_joins(self):
        """Requete de base avec jointures pour recuperer les infos departement."""
        return """
            SELECT c.*, cmd.id_departement
            FROM colis c
            LEFT JOIN bon_livraison bl ON c.id_bl = bl.id_bl
            LEFT JOIN commande cmd ON bl.id_commande = cmd.id_commande
        """
    
    def find_all(self):
        """Retourne tous les colis (plus recents en premier)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM colis ORDER BY id_colis DESC")
            rows = cursor.fetchall()
            return [Colis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_id(self, id):
        """Retourne un colis par son ID, ou None."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM colis WHERE id_colis = %s", (id,))
            row = cursor.fetchone()
            return Colis(row) if row else None
        finally:
            cursor.close()
            conn.close()
    
    def find_by_bl(self, id_bl):
        """Retourne tous les colis d'un bon de livraison."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM colis WHERE id_bl = %s ORDER BY id_colis", (id_bl,))
            rows = cursor.fetchall()
            return [Colis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_statut(self, statut):
        """Retourne les colis ayant un statut specifique."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM colis WHERE statut_actuel = %s ORDER BY id_colis DESC", (statut,))
            rows = cursor.fetchall()
            return [Colis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_departement(self, id_departement):
        """Retourne tous les colis d'un departement.
        
        Jointure : colis -> bon_livraison -> commande -> departement
        """
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.* 
                FROM colis c
                JOIN bon_livraison bl ON c.id_bl = bl.id_bl
                JOIN commande cmd ON bl.id_commande = cmd.id_commande
                WHERE cmd.id_departement = %s
                ORDER BY c.id_colis DESC
            """, (id_departement,))
            rows = cursor.fetchall()
            return [Colis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_statut_and_departement(self, statut, id_departement):
        """Retourne les colis d'un statut pour un departement."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.* 
                FROM colis c
                JOIN bon_livraison bl ON c.id_bl = bl.id_bl
                JOIN commande cmd ON bl.id_commande = cmd.id_commande
                WHERE c.statut_actuel = %s AND cmd.id_departement = %s
                ORDER BY c.id_colis DESC
            """, (statut, id_departement))
            rows = cursor.fetchall()
            return [Colis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_en_attente_by_departement(self, id_departement):
        """Retourne les colis attendus d'un departement."""
        return self.find_by_statut_and_departement('attendu', id_departement)
    
    def find_a_distribuer_by_departement(self, id_departement):
        """Retourne les colis a distribuer d'un departement."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.* 
                FROM colis c
                JOIN bon_livraison bl ON c.id_bl = bl.id_bl
                JOIN commande cmd ON bl.id_commande = cmd.id_commande
                WHERE c.statut_actuel IN ('recu', 'en_distribution') AND cmd.id_departement = %s
                ORDER BY c.id_colis
            """, (id_departement,))
            rows = cursor.fetchall()
            return [Colis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_tracking(self, num_suivi):
        """Retourne un colis par son numero de suivi (exact)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM colis WHERE num_suivi_transporteur = %s", (num_suivi,))
            row = cursor.fetchone()
            return Colis(row) if row else None
        finally:
            cursor.close()
            conn.close()
    
    def search_by_tracking(self, query):
        """Recherche les colis dont le numero de suivi contient la requete."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM colis WHERE num_suivi_transporteur LIKE %s ORDER BY id_colis DESC",
                (f'%{query}%',)
            )
            rows = cursor.fetchall()
            return [Colis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def search_by_tracking_and_departement(self, query, id_departement):
        """Recherche les colis d'un departement par numero de suivi."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.* 
                FROM colis c
                JOIN bon_livraison bl ON c.id_bl = bl.id_bl
                JOIN commande cmd ON bl.id_commande = cmd.id_commande
                WHERE c.num_suivi_transporteur LIKE %s AND cmd.id_departement = %s
                ORDER BY c.id_colis DESC
            """, (f'%{query}%', id_departement))
            rows = cursor.fetchall()
            return [Colis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_en_attente(self):
        """Retourne les colis attendus (pas encore arrives)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM colis WHERE statut_actuel = 'attendu' ORDER BY id_colis")
            rows = cursor.fetchall()
            return [Colis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_a_distribuer(self):
        """Retourne les colis a distribuer (recus ou en cours)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM colis WHERE statut_actuel IN ('recu', 'en_distribution') ORDER BY id_colis"
            )
            rows = cursor.fetchall()
            return [Colis(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def create(self, form):
        """Cree un nouveau colis. Retourne l'ID cree."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """INSERT INTO colis (id_bl, num_suivi_transporteur, nom_transporteur, statut_actuel, lieu_stockage, notes) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (form.get('id_bl'), form.get('num_suivi_transporteur'), form.get('nom_transporteur'),
                 form.get('statut_actuel', 'attendu'), form.get('lieu_stockage'), form.get('notes'))
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
        """Met a jour un colis existant."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            fields = []
            values = []
            for key in ['id_bl', 'num_suivi_transporteur', 'nom_transporteur', 'statut_actuel', 'lieu_stockage', 'notes']:
                if key in form:
                    fields.append(f"{key} = %s")
                    values.append(form[key] if form[key] != '' else None)
            values.append(id)
            cursor.execute(f"UPDATE colis SET {', '.join(fields)} WHERE id_colis = %s", values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def update_statut(self, id, statut, lieu=None):
        """Met a jour le statut d'un colis avec gestion des dates."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            if statut == 'recu':
                cursor.execute(
                    "UPDATE colis SET statut_actuel = %s, lieu_stockage = %s, date_reception = NOW() WHERE id_colis = %s",
                    (statut, lieu, id)
                )
            elif statut == 'livre':
                cursor.execute(
                    "UPDATE colis SET statut_actuel = %s, lieu_stockage = NULL, date_livraison = NOW() WHERE id_colis = %s",
                    (statut, id)
                )
            else:
                cursor.execute("UPDATE colis SET statut_actuel = %s WHERE id_colis = %s", (statut, id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def delete(self, id):
        """Supprime un colis."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM colis WHERE id_colis = %s", (id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def count_by_statut(self):
        """Retourne le nombre de colis par statut (pour le dashboard)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT statut_actuel, COUNT(*) as count FROM colis GROUP BY statut_actuel")
            rows = cursor.fetchall()
            return {row['statut_actuel']: row['count'] for row in rows}
        finally:
            cursor.close()
            conn.close()
    
    def count_by_statut_and_departement(self, id_departement):
        """Retourne le nombre de colis par statut pour un departement.
        
        Jointure : colis -> bon_livraison -> commande -> departement
        """
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.statut_actuel, COUNT(*) as count 
                FROM colis c
                JOIN bon_livraison bl ON c.id_bl = bl.id_bl
                JOIN commande cmd ON bl.id_commande = cmd.id_commande
                WHERE cmd.id_departement = %s
                GROUP BY c.statut_actuel
            """, (id_departement,))
            rows = cursor.fetchall()
            return {row['statut_actuel']: row['count'] for row in rows}
        finally:
            cursor.close()
            conn.close()
    
    def count_total(self):
        """Retourne le nombre total de colis."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as count FROM colis")
            result = cursor.fetchone()
            return result['count'] if result else 0
        finally:
            cursor.close()
            conn.close()
    
    def get_departement_id(self, id_colis):
        """Retourne l'ID du departement d'un colis."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT cmd.id_departement
                FROM colis c
                JOIN bon_livraison bl ON c.id_bl = bl.id_bl
                JOIN commande cmd ON bl.id_commande = cmd.id_commande
                WHERE c.id_colis = %s
            """, (id_colis,))
            row = cursor.fetchone()
            return row['id_departement'] if row else None
        finally:
            cursor.close()
            conn.close()

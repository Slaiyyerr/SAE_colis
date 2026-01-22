"""DAO pour la table commande (bons de commande).

Gere les operations CRUD sur les commandes.
Une commande est liee a un fournisseur, un departement et un demandeur.
"""

from app.dao.DatabaseConnection import db
from app.models.Commande import Commande


class CommandeDAO:
    
    def _base_query_with_joins(self):
        """Requete de base avec jointures pour fournisseur et departement."""
        return """
            SELECT c.*, 
                   f.nom_societe as fournisseur_nom,
                   d.nom_departement as departement_nom,
                   CONCAT(u.prenom, ' ', u.nom) as demandeur_nom
            FROM commande c
            LEFT JOIN fournisseur f ON c.id_fournisseur = f.id_fournisseur
            LEFT JOIN departement d ON c.id_departement = d.id_departement
            LEFT JOIN utilisateur u ON c.id_demandeur = u.id_utilisateur
        """
    
    def find_all(self):
        """Retourne toutes les commandes (plus recentes en premier)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(self._base_query_with_joins() + " ORDER BY c.date_creation DESC")
            rows = cursor.fetchall()
            return [Commande(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_id(self, id):
        """Retourne une commande par son ID, ou None."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(self._base_query_with_joins() + " WHERE c.id_commande = %s", (id,))
            row = cursor.fetchone()
            return Commande(row) if row else None
        finally:
            cursor.close()
            conn.close()
    
    def find_by_numero(self, numero_bc):
        """Retourne une commande par son numero BC."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(self._base_query_with_joins() + " WHERE c.numero_bc = %s", (numero_bc,))
            row = cursor.fetchone()
            return Commande(row) if row else None
        finally:
            cursor.close()
            conn.close()
    
    def find_by_statut(self, statut):
        """Retourne les commandes ayant un statut specifique."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                self._base_query_with_joins() + " WHERE c.statut_global = %s ORDER BY c.date_creation DESC",
                (statut,)
            )
            rows = cursor.fetchall()
            return [Commande(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_departement(self, id_departement):
        """Retourne les commandes d'un departement."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                self._base_query_with_joins() + " WHERE c.id_departement = %s ORDER BY c.date_creation DESC",
                (id_departement,)
            )
            rows = cursor.fetchall()
            return [Commande(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_fournisseur(self, id_fournisseur):
        """Retourne les commandes passees a un fournisseur."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                self._base_query_with_joins() + " WHERE c.id_fournisseur = %s ORDER BY c.date_creation DESC",
                (id_fournisseur,)
            )
            rows = cursor.fetchall()
            return [Commande(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def create(self, form):
        """Cree une nouvelle commande. Retourne l'ID cree."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """INSERT INTO commande 
                   (numero_bc, id_fournisseur, id_departement, id_demandeur, date_livraison_prevue, notes, fichier_bc) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (form.get('numero_bc'), form.get('id_fournisseur'), form.get('id_departement'),
                 form.get('id_demandeur'), form.get('date_livraison_prevue') or None,
                 form.get('notes'), form.get('fichier_bc'))
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
        """Met a jour une commande existante (champs dynamiques)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            fields = []
            values = []
            # Liste des champs modifiables (incluant id_demandeur)
            for key in ['numero_bc', 'id_fournisseur', 'id_departement', 'id_demandeur',
                        'date_livraison_prevue', 'statut_global', 'notes', 'fichier_bc']:
                if key in form:
                    fields.append(f"{key} = %s")
                    values.append(form[key] if form[key] != '' else None)
            if not fields:
                return
            values.append(id)
            cursor.execute(f"UPDATE commande SET {', '.join(fields)} WHERE id_commande = %s", values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def delete(self, id):
        """Supprime une commande (CASCADE sur BL et colis)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM commande WHERE id_commande = %s", (id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def count_by_statut(self):
        """Retourne le nombre de commandes par statut (pour le dashboard)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT statut_global, COUNT(*) as count FROM commande GROUP BY statut_global")
            rows = cursor.fetchall()
            return {row['statut_global']: row['count'] for row in rows}
        finally:
            cursor.close()
            conn.close()
    
    def count_by_statut_and_departement(self, id_departement):
        """Retourne le nombre de commandes par statut pour un departement."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT statut_global, COUNT(*) as count FROM commande WHERE id_departement = %s GROUP BY statut_global",
                (id_departement,)
            )
            rows = cursor.fetchall()
            return {row['statut_global']: row['count'] for row in rows}
        finally:
            cursor.close()
            conn.close()

"""DAO pour la table utilisateur.

Gere les utilisateurs autorises a se connecter.
L'email est l'identifiant unique.
"""

from app.dao.DatabaseConnection import db
from app.models.Utilisateur import Utilisateur


class UtilisateurDAO:
    
    def find_all(self):
        """Retourne tous les utilisateurs."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM utilisateur ORDER BY nom, prenom")
            rows = cursor.fetchall()
            return [Utilisateur(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_id(self, id):
        """Retourne un utilisateur par son ID, ou None."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM utilisateur WHERE id_utilisateur = %s", (id,))
            row = cursor.fetchone()
            return Utilisateur(row) if row else None
        finally:
            cursor.close()
            conn.close()
    
    def find_by_email(self, email):
        """Retourne un utilisateur par son email."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM utilisateur WHERE email = %s", (email,))
            row = cursor.fetchone()
            return Utilisateur(row) if row else None
        finally:
            cursor.close()
            conn.close()
    
    def find_by_role(self, role):
        """Retourne tous les utilisateurs actifs ayant un role specifique (avec nom departement)."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT u.*, d.nom_departement 
                   FROM utilisateur u
                   LEFT JOIN departement d ON u.id_departement = d.id_departement
                   WHERE u.role = %s AND u.est_actif = TRUE 
                   ORDER BY u.nom, u.prenom""",
                (role,)
            )
            rows = cursor.fetchall()
            return [Utilisateur(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_by_departement(self, id_departement):
        """Retourne tous les utilisateurs d'un departement."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM utilisateur WHERE id_departement = %s ORDER BY nom, prenom",
                (id_departement,)
            )
            rows = cursor.fetchall()
            return [Utilisateur(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def find_actifs(self):
        """Retourne tous les utilisateurs actifs."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM utilisateur WHERE est_actif = TRUE ORDER BY nom, prenom")
            rows = cursor.fetchall()
            return [Utilisateur(row) for row in rows]
        finally:
            cursor.close()
            conn.close()
    
    def create(self, form):
        """Cree un nouvel utilisateur. Retourne l'ID cree."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            # Mot de passe par defaut si non fourni
            mot_de_passe = form.get('mot_de_passe', 'password')
            cursor.execute(
                """INSERT INTO utilisateur (email, mot_de_passe, nom, prenom, role, id_departement) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (form.get('email'), mot_de_passe, form.get('nom'), form.get('prenom'),
                 form.get('role', 'demandeur'), form.get('id_departement'))
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
        """Met a jour un utilisateur existant."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            fields = []
            values = []
            for key in ['email', 'mot_de_passe', 'nom', 'prenom', 'role', 'id_departement']:
                if key in form and form[key] is not None:
                    fields.append(f"{key} = %s")
                    values.append(form[key] if form[key] != '' else None)
            if not fields:
                return
            values.append(id)
            cursor.execute(f"UPDATE utilisateur SET {', '.join(fields)} WHERE id_utilisateur = %s", values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def set_actif(self, id, est_actif):
        """Active ou desactive un utilisateur."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE utilisateur SET est_actif = %s WHERE id_utilisateur = %s", (est_actif, id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def delete(self, id):
        """Supprime definitivement un utilisateur."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM utilisateur WHERE id_utilisateur = %s", (id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

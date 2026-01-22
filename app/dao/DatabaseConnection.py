"""Gestion de la connexion a la base de donnees MySQL.

Utilise un pool de connexions pour gerer les requetes simultanees.
La connexion est configuree en UTF-8 pour supporter les accents.

Usage dans les DAOs :
    conn = db.get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ...")
        result = cursor.fetchall()
        conn.commit()  # Si modification
        return result
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()  # Remet la connexion dans le pool
"""

import mysql.connector
from mysql.connector import pooling


class DatabaseConnection:
    """Gestionnaire de connexion MySQL avec pool de connexions."""
    
    def __init__(self):
        self.pool = None
        self.config = None
    
    def init_app(self, app):
        """Initialise la connexion avec la config Flask.
        
        Appele une fois au demarrage de l'application.
        """
        self.config = {
            'host': app.config.get('DB_HOST', 'localhost'),
            'port': app.config.get('DB_PORT', 3306),
            'database': app.config.get('DB_NAME', 'suivi_colis'),
            'user': app.config.get('DB_USER', 'root'),
            'password': app.config.get('DB_PASSWORD', ''),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'use_unicode': True,
            'autocommit': False
        }
        
        # Pool de 5 connexions pour gerer les requetes simultanees
        self.pool = pooling.MySQLConnectionPool(
            pool_name="suivi_colis_pool",
            pool_size=5,
            pool_reset_session=True,
            **self.config
        )
    
    def get_connection(self):
        """Recupere une connexion du pool.
        
        IMPORTANT : La connexion doit etre fermee apres usage avec conn.close()
        Cela la remet dans le pool (ne ferme pas vraiment la connexion).
        """
        return self.pool.get_connection()


# Instance globale utilisee par tous les DAOs
db = DatabaseConnection()

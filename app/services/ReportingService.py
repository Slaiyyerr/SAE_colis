"""Service de reporting et statistiques.

Fournit les donnees pour le dashboard admin et les rapports.

Fonctionnalites :
- Compteurs par statut (commandes, colis)
- Statistiques par fournisseur
- Statistiques par departement
- Activite recente
"""

from app.dao.CommandeDAO import CommandeDAO
from app.dao.ColisDAO import ColisDAO
from app.dao.HistoriqueColisDAO import HistoriqueColisDAO
from app.dao.DatabaseConnection import db


class ReportingService:
    def __init__(self):
        self.commande_dao = CommandeDAO()
        self.colis_dao = ColisDAO()
        self.historique_dao = HistoriqueColisDAO()
    
    def getDashboardData(self):
        """Retourne toutes les donnees pour le dashboard.
        
        Returns:
            dict avec :
            - total_commandes, total_colis
            - commandes_par_statut, colis_par_statut
            - colis_en_attente, colis_a_distribuer, colis_probleme
            - activite_recente (10 derniers evenements)
        """
        commandes = self.commande_dao.find_all()
        colis = self.colis_dao.find_all()
        
        # Comptage des commandes par statut
        commandes_par_statut = {
            'en_attente': 0,
            'validee': 0,
            'non_validee': 0,
            'en_cours': 0,
            'recue': 0,
            'annulee': 0
        }
        for cmd in commandes:
            statut = cmd.statut_global or 'en_attente'
            if statut in commandes_par_statut:
                commandes_par_statut[statut] += 1
        
        # Comptage des colis par statut
        colis_par_statut = {
            'attendu': 0,
            'recu': 0,
            'en_distribution': 0,
            'livre': 0,
            'probleme': 0
        }
        for c in colis:
            statut = c.statut_actuel or 'attendu'
            if statut in colis_par_statut:
                colis_par_statut[statut] += 1
        
        return {
            'total_commandes': len(commandes),
            'total_colis': len(colis),
            'commandes_par_statut': commandes_par_statut,
            'colis_par_statut': colis_par_statut,
            'colis_en_attente': colis_par_statut['attendu'],
            'colis_a_distribuer': colis_par_statut['recu'] + colis_par_statut['en_distribution'],
            'colis_probleme': colis_par_statut['probleme'],
            'activite_recente': self._get_activite_recente(10)
        }
    
    def _get_activite_recente(self, limit=10):
        """Retourne les N derniers evenements de l'historique."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT h.*, c.num_suivi_transporteur, u.prenom, u.nom
                FROM historique_colis h
                LEFT JOIN colis c ON h.id_colis = c.id_colis
                LEFT JOIN utilisateur u ON h.id_utilisateur = u.id_utilisateur
                ORDER BY h.date_heure DESC
                LIMIT %s
            """, (limit,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    def getStatsFournisseurs(self):
        """Statistiques des commandes par fournisseur."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    f.id_fournisseur,
                    f.nom_societe,
                    COUNT(c.id_commande) as nb_commandes,
                    SUM(CASE WHEN c.statut_global IN ('en_attente','validee','en_cours') THEN 1 ELSE 0 END) as en_cours
                FROM fournisseur f
                LEFT JOIN commande c ON f.id_fournisseur = c.id_fournisseur
                GROUP BY f.id_fournisseur, f.nom_societe
                ORDER BY nb_commandes DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    def getStatsDepartements(self):
        """Statistiques des colis par departement."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    d.id_departement,
                    d.nom_departement,
                    COUNT(DISTINCT col.id_colis) as nb_colis
                FROM departement d
                LEFT JOIN commande c ON d.id_departement = c.id_departement
                LEFT JOIN bon_livraison bl ON c.id_commande = bl.id_commande
                LEFT JOIN colis col ON bl.id_bl = col.id_bl
                GROUP BY d.id_departement, d.nom_departement
                ORDER BY nb_colis DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    def getStatsCommandesDepartements(self):
        """Statistiques des commandes par departement."""
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    d.id_departement,
                    d.nom_departement,
                    COUNT(c.id_commande) as nb_commandes
                FROM departement d
                LEFT JOIN commande c ON d.id_departement = c.id_departement
                GROUP BY d.id_departement, d.nom_departement
                ORDER BY nb_commandes DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

"""Service pour la gestion des colis.

Contient la logique metier du suivi des colis :
- Changements de statut avec historique
- Notifications automatiques aux demandeurs
- Recherche et filtrage
"""

from app.dao.ColisDAO import ColisDAO
from app.dao.HistoriqueColisDAO import HistoriqueColisDAO
from app.services.NotificationService import NotificationService


class ColisService:
    def __init__(self):
        self.dao = ColisDAO()
        self.historique_dao = HistoriqueColisDAO()
        self.notif_service = NotificationService()
    
    def getAll(self):
        """Retourne tous les colis."""
        return self.dao.find_all()
    
    def getById(self, id):
        """Retourne un colis par ID."""
        return self.dao.find_by_id(id)
    
    def getByStatut(self, statut):
        """Retourne les colis ayant un statut specifique."""
        return self.dao.find_by_statut(statut)
    
    def getByDepartement(self, id_departement):
        """Retourne tous les colis d'un departement."""
        return self.dao.find_by_departement(id_departement)
    
    def getByStatutAndDepartement(self, statut, id_departement):
        """Retourne les colis d'un statut pour un departement."""
        return self.dao.find_by_statut_and_departement(statut, id_departement)
    
    def getByTracking(self, num_suivi):
        """Retourne un colis par numero de suivi (exact)."""
        return self.dao.find_by_tracking(num_suivi)
    
    def getEnAttente(self):
        """Retourne les colis en attente d'arrivee."""
        return self.dao.find_en_attente()
    
    def getEnAttenteByDepartement(self, id_departement):
        """Retourne les colis en attente d'un departement."""
        return self.dao.find_en_attente_by_departement(id_departement)
    
    def getADistribuer(self):
        """Retourne les colis a distribuer (recus ou en distribution)."""
        return self.dao.find_a_distribuer()
    
    def getADistribuerByDepartement(self, id_departement):
        """Retourne les colis a distribuer d'un departement."""
        return self.dao.find_a_distribuer_by_departement(id_departement)
    
    def search(self, query):
        """Recherche les colis par numero de suivi (partiel)."""
        return self.dao.search_by_tracking(query)
    
    def searchByDepartement(self, query, id_departement):
        """Recherche les colis d'un departement par numero de suivi."""
        return self.dao.search_by_tracking_and_departement(query, id_departement)
    
    def getHistorique(self, id_colis):
        """Retourne l'historique complet d'un colis."""
        return self.historique_dao.find_by_colis(id_colis)
    
    def countByStatut(self):
        """Retourne le nombre de colis par statut (pour le dashboard)."""
        return self.dao.count_by_statut()
    
    def countByStatutAndDepartement(self, id_departement):
        """Retourne le nombre de colis par statut pour un departement."""
        return self.dao.count_by_statut_and_departement(id_departement)
    
    def getDepartementId(self, id_colis):
        """Retourne l'ID du departement d'un colis."""
        return self.dao.get_departement_id(id_colis)
    
    def create(self, form):
        """Cree un nouveau colis."""
        return self.dao.create(form)
    
    def update(self, id, form):
        """Met a jour un colis."""
        return self.dao.update(id, form)
    
    def receptionner(self, id_colis, id_utilisateur, lieu='Reprographie'):
        """Marque un colis comme recu a la reprographie.
        
        - Change le statut en 'recu'
        - Enregistre la date de reception
        - Cree une entree dans l'historique
        - Notifie le demandeur
        """
        self.dao.update_statut(id_colis, 'recu', lieu)
        self.historique_dao.log_reception(id_colis, id_utilisateur)
        self.notif_service.notifierChangementStatutColis(id_colis, 'attendu', 'recu')
    
    def mettreEnDistribution(self, id_colis, id_utilisateur):
        """Met un colis en distribution vers le departement.
        
        - Change le statut en 'en_distribution'
        - Cree une entree dans l'historique
        - Notifie le demandeur
        """
        colis = self.dao.find_by_id(id_colis)
        ancien = colis.statut_actuel if colis else 'recu'
        self.dao.update_statut(id_colis, 'en_distribution')
        self.historique_dao.log_changement_statut(id_colis, id_utilisateur, ancien, 'en_distribution')
        self.notif_service.notifierChangementStatutColis(id_colis, ancien, 'en_distribution')
    
    def livrer(self, id_colis, id_utilisateur, lieu=None):
        """Marque un colis comme livre au destinataire.
        
        - Change le statut en 'livre'
        - Enregistre la date de livraison
        - Cree une entree dans l'historique
        - Notifie le demandeur
        """
        self.dao.update_statut(id_colis, 'livre')
        self.historique_dao.log_livraison(id_colis, id_utilisateur, lieu)
        self.notif_service.notifierChangementStatutColis(id_colis, 'en_distribution', 'livre')
    
    def signalerProbleme(self, id_colis, id_utilisateur, description):
        """Signale un probleme sur un colis.
        
        - Change le statut en 'probleme'
        - Enregistre la description du probleme
        - Notifie le demandeur ET les admins
        """
        colis = self.dao.find_by_id(id_colis)
        ancien = colis.statut_actuel if colis else 'inconnu'
        self.dao.update_statut(id_colis, 'probleme')
        self.historique_dao.create({
            'id_colis': id_colis,
            'id_utilisateur': id_utilisateur,
            'action': f'Probleme: {description}',
            'ancien_statut': ancien,
            'nouveau_statut': 'probleme'
        })
        self.notif_service.notifierChangementStatutColis(id_colis, ancien, 'probleme')
    
    def resoudreProbleme(self, id_colis, id_utilisateur, nouveau_statut='recu'):
        """Resout un probleme sur un colis et le remet dans le circuit.
        
        - Change le statut vers le nouveau statut choisi (recu par defaut)
        - Cree une entree dans l'historique
        - Notifie le demandeur
        """
        colis = self.dao.find_by_id(id_colis)
        if not colis or colis.statut_actuel != 'probleme':
            raise ValueError("Ce colis n'est pas en statut probleme")
        
        self.dao.update_statut(id_colis, nouveau_statut)
        self.historique_dao.log_resolution_probleme(id_colis, id_utilisateur, nouveau_statut)
        self.notif_service.notifierChangementStatutColis(id_colis, 'probleme', nouveau_statut)
    
    def delete(self, id):
        """Supprime un colis."""
        return self.dao.delete(id)

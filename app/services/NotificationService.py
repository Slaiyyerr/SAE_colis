"""Service pour la gestion des notifications.

Gere l'envoi automatique de notifications aux utilisateurs
lors des changements de statut des colis.

Notifications envoyees :
- Au demandeur : quand son colis change de statut
- Aux admins : quand un probleme est signale
- Aux responsables colis : quand une nouvelle commande est creee
"""

from app.dao.NotificationDAO import NotificationDAO
from app.dao.UtilisateurDAO import UtilisateurDAO
from app.dao.CommandeDAO import CommandeDAO
from app.dao.ColisDAO import ColisDAO


class NotificationService:
    def __init__(self):
        self.dao = NotificationDAO()
        self.utilisateur_dao = UtilisateurDAO()
        self.commande_dao = CommandeDAO()
        self.colis_dao = ColisDAO()
    
    def getByUtilisateur(self, id_utilisateur, limit=50):
        """Retourne les notifications d'un utilisateur."""
        return self.dao.find_by_utilisateur(id_utilisateur, limit)
    
    def getNonLues(self, id_utilisateur):
        """Retourne les notifications non lues."""
        return self.dao.find_non_lues(id_utilisateur)
    
    def countNonLues(self, id_utilisateur):
        """Compte les notifications non lues (pour le badge navbar)."""
        return self.dao.count_non_lues(id_utilisateur)
    
    def marquerLue(self, id_notification):
        """Marque une notification comme lue."""
        return self.dao.marquer_lue(id_notification)
    
    def marquerToutesLues(self, id_utilisateur):
        """Marque toutes les notifications comme lues."""
        return self.dao.marquer_toutes_lues(id_utilisateur)
    
    def creer(self, id_utilisateur, titre, message, lien=None):
        """Cree une nouvelle notification."""
        return self.dao.create({
            'id_utilisateur': id_utilisateur,
            'titre': titre,
            'message': message,
            'lien': lien
        })
    
    def notifierChangementStatutColis(self, id_colis, ancien_statut, nouveau_statut):
        """Notifie le demandeur quand son colis change de statut.
        
        Remonte la chaine : colis -> BL -> commande -> demandeur
        Si le nouveau statut est 'probleme', notifie aussi les admins.
        """
        colis = self.colis_dao.find_by_id(id_colis)
        if not colis or not colis.id_bl:
            return
        
        # Remonter : colis -> bon_livraison -> commande -> demandeur
        from app.dao.BonLivraisonDAO import BonLivraisonDAO
        bl_dao = BonLivraisonDAO()
        bl = bl_dao.find_by_id(colis.id_bl)
        if not bl:
            return
        
        commande = self.commande_dao.find_by_id(bl.id_commande)
        if not commande or not commande.id_demandeur:
            return
        
        # Messages selon le statut
        messages = {
            'recu': 'Votre colis est arrive a la reprographie',
            'en_distribution': 'Votre colis est en cours de distribution',
            'livre': 'Votre colis a ete livre',
            'probleme': 'Un probleme a ete signale sur votre colis'
        }
        
        titre = f'Colis {colis.num_suivi_transporteur or "#" + str(id_colis)}'
        message = messages.get(nouveau_statut, f'Statut mis a jour: {nouveau_statut}')
        lien = f'/colis/{id_colis}'
        
        # Notifier le demandeur
        self.creer(commande.id_demandeur, titre, message, lien)
        
        # Si probleme, notifier aussi les admins
        if nouveau_statut == 'probleme':
            admins = self.utilisateur_dao.find_by_role('admin')
            for admin in admins:
                self.creer(admin.id_utilisateur, f'[ALERTE] {titre}', message, lien)
    
    def notifierNouvelleCommande(self, id_commande):
        """Notifie les responsables colis d'une nouvelle commande."""
        commande = self.commande_dao.find_by_id(id_commande)
        if not commande:
            return
        
        responsables = self.utilisateur_dao.find_by_role('responsable_colis')
        for resp in responsables:
            self.creer(
                resp.id_utilisateur,
                f'Nouvelle commande {commande.numero_bc}',
                'Une nouvelle commande a ete enregistree',
                f'/commandes/{id_commande}'
            )
    
    def notifierColisEnAttente(self, id_colis, jours):
        """Notifie les admins d'un colis en attente trop longtemps.
        
        A appeler via un script cron pour detecter les retards.
        """
        colis = self.colis_dao.find_by_id(id_colis)
        if not colis:
            return
        
        admins = self.utilisateur_dao.find_by_role('admin')
        for admin in admins:
            self.creer(
                admin.id_utilisateur,
                f'[RETARD] Colis en attente depuis {jours} jours',
                f'Colis {colis.num_suivi_transporteur or "#" + str(id_colis)} en attente',
                f'/colis/{id_colis}'
            )

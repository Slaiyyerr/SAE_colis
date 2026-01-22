"""Controller de la page d'accueil (dashboard).

Affiche un tableau de bord personnalisé selon le rôle de l'utilisateur.

Tableaux de bord par rôle :
- demandeur : Mes colis, mes commandes, notifications
- editeur : Commandes à valider, stats fournisseurs
- responsable_colis : Colis à traiter, incidents
- admin : Stats globales, gestion système
"""

from flask import render_template, session
from app import app
from app.controllers.AuthController import require_login, can_see_all_departments, get_user_department_id
from app.services.ColisService import ColisService
from app.services.CommandeService import CommandeService
from app.services.HistoriqueColisService import HistoriqueColisService
from app.services.NotificationService import NotificationService
from app.services.FournisseurService import FournisseurService
from app.services.DepartementService import DepartementService
from app.services.UtilisateurService import UtilisateurService
from app.services.ReportingService import ReportingService

colis_service = ColisService()
commande_service = CommandeService()
historique_service = HistoriqueColisService()
notif_service = NotificationService()
fournisseur_service = FournisseurService()
departement_service = DepartementService()
user_service = UtilisateurService()
reporting_service = ReportingService()


@app.route('/')
@require_login
def home():
    """Dashboard principal - redirige vers le bon tableau de bord selon le rôle."""
    role = session['user']['role']
    
    if role == 'demandeur':
        return dashboard_demandeur()
    elif role == 'editeur':
        return dashboard_editeur()
    elif role == 'responsable_colis':
        return dashboard_responsable()
    elif role == 'admin':
        return dashboard_admin()
    else:
        # Fallback sur le dashboard générique
        return dashboard_generique()


def dashboard_demandeur():
    """Tableau de bord pour les demandeurs.
    
    Affiche :
    - Statistiques personnelles (colis, commandes)
    - Liste des colis en cours
    - Commandes récentes
    - Notifications
    """
    user_id = session['user']['id']
    user_dept_id = get_user_department_id()
    
    # Statistiques
    colis_par_statut = colis_service.countByStatutAndDepartement(user_dept_id) if user_dept_id else {}
    commandes_par_statut = commande_service.countByStatutAndDepartement(user_dept_id) if user_dept_id else {}
    
    # Colis en cours (non livrés)
    colis_en_cours = []
    if user_dept_id:
        all_colis = colis_service.getByDepartement(user_dept_id)
        colis_en_cours = [c for c in all_colis if c.statut_actuel in ['attendu', 'recu', 'en_distribution']][:5]
    
    # Commandes récentes
    commandes_recentes = []
    if user_dept_id:
        all_commandes = commande_service.getByDepartement(user_dept_id)
        commandes_recentes = sorted(all_commandes, key=lambda x: x.date_creation or '', reverse=True)[:5]
    
    # Notifications
    notifications_recentes = notif_service.getByUtilisateur(user_id)[:5]
    
    stats = {
        'total_colis': sum(colis_par_statut.values()) if colis_par_statut else 0,
        'total_commandes': sum(commandes_par_statut.values()) if commandes_par_statut else 0,
        'colis_en_attente': colis_par_statut.get('attendu', 0),
        'colis_livres': colis_par_statut.get('livre', 0),
        'colis_en_cours': colis_en_cours,
        'commandes_recentes': commandes_recentes,
        'notifications_recentes': notifications_recentes
    }
    
    return render_template('home/dashboard_demandeur.html', stats=stats)


def dashboard_editeur():
    """Tableau de bord pour les éditeurs.
    
    Affiche :
    - Statistiques commandes (total, à valider, validées)
    - Commandes en attente de validation
    - Stats par fournisseur
    - Commandes récentes
    """
    # Statistiques commandes
    commandes_par_statut = commande_service.countByStatut()
    
    # Commandes à valider
    commandes_a_valider = commande_service.getByStatut('en_attente')[:10]
    for cmd in commandes_a_valider:
        # Récupérer les noms
        fournisseur = fournisseur_service.getById(cmd.id_fournisseur)
        departement = departement_service.getById(cmd.id_departement)
        cmd.fournisseur_nom = fournisseur.nom_societe if fournisseur else None
        cmd.departement_nom = departement.nom_departement if departement else None
    
    # Stats fournisseurs
    stats_fournisseurs = reporting_service.getStatsFournisseurs()[:5]
    
    # Commandes récentes
    all_commandes = commande_service.getAll()
    commandes_recentes = sorted(all_commandes, key=lambda x: x.date_creation or '', reverse=True)[:10]
    for cmd in commandes_recentes:
        fournisseur = fournisseur_service.getById(cmd.id_fournisseur)
        cmd.fournisseur_nom = fournisseur.nom_societe if fournisseur else None
    
    stats = {
        'total_commandes': sum(commandes_par_statut.values()) if commandes_par_statut else 0,
        'commandes_en_attente': commandes_par_statut.get('en_attente', 0),
        'commandes_validees': commandes_par_statut.get('validee', 0),
        'commandes_non_validees': commandes_par_statut.get('non_validee', 0),
        'total_fournisseurs': len(fournisseur_service.getAll()),
        'commandes_a_valider': commandes_a_valider,
        'stats_fournisseurs': stats_fournisseurs,
        'commandes_recentes': commandes_recentes
    }
    
    return render_template('home/dashboard_editeur.html', stats=stats)


def dashboard_responsable():
    """Tableau de bord pour les responsables colis.
    
    Affiche :
    - Statistiques colis (total, à réceptionner, à distribuer, incidents)
    - Colis à réceptionner
    - Colis à distribuer
    - Incidents en cours
    - Activité récente
    """
    # Statistiques colis
    colis_par_statut = colis_service.countByStatut()
    
    # Colis à réceptionner (attendus)
    colis_a_receptionner = colis_service.getByStatut('attendu')[:10]
    for c in colis_a_receptionner:
        dept_id = colis_service.getDepartementId(c.id_colis)
        dept = departement_service.getById(dept_id) if dept_id else None
        c.departement_nom = dept.nom_departement if dept else None
    
    # Colis à distribuer (reçus ou en distribution)
    colis_a_distribuer = colis_service.getADistribuer()[:10]
    for c in colis_a_distribuer:
        dept_id = colis_service.getDepartementId(c.id_colis)
        dept = departement_service.getById(dept_id) if dept_id else None
        c.departement_nom = dept.nom_departement if dept else None
    
    # Incidents
    colis_incidents = colis_service.getByStatut('probleme')[:5]
    
    # Activité récente
    activite_recente = historique_service.getRecent(10)
    
    stats = {
        'total_colis': sum(colis_par_statut.values()) if colis_par_statut else 0,
        'colis_attendus': colis_par_statut.get('attendu', 0),
        'colis_recus': colis_par_statut.get('recu', 0),
        'colis_en_distribution': colis_par_statut.get('en_distribution', 0),
        'colis_probleme': colis_par_statut.get('probleme', 0),
        'colis_a_receptionner': colis_a_receptionner,
        'colis_a_distribuer': colis_a_distribuer,
        'colis_incidents': colis_incidents,
        'activite_recente': activite_recente
    }
    
    return render_template('home/dashboard_responsable.html', stats=stats)


def dashboard_admin():
    """Tableau de bord pour les administrateurs.
    
    Affiche :
    - Statistiques globales (commandes, colis, utilisateurs)
    - Stats par département
    - Stats par fournisseur
    - Accès rapide à la gestion
    - Activité récente
    """
    # Statistiques globales
    colis_par_statut = colis_service.countByStatut()
    commandes_par_statut = commande_service.countByStatut()
    
    # Stats par département et fournisseur
    stats_departements = reporting_service.getStatsDepartements()
    stats_fournisseurs = reporting_service.getStatsFournisseurs()[:5]
    
    # Comptages
    all_users = user_service.getAll()
    users_actifs = [u for u in all_users if u.est_actif]
    all_departements = departement_service.getAll()
    
    # Activité récente
    activite_recente = historique_service.getRecent(10)
    
    stats = {
        'total_commandes': sum(commandes_par_statut.values()) if commandes_par_statut else 0,
        'total_colis': sum(colis_par_statut.values()) if colis_par_statut else 0,
        'colis_en_attente': colis_par_statut.get('attendu', 0),
        'colis_a_distribuer': colis_par_statut.get('recu', 0) + colis_par_statut.get('en_distribution', 0),
        'colis_probleme': colis_par_statut.get('probleme', 0),
        'total_utilisateurs': len(users_actifs),
        'total_departements': len(all_departements),
        'stats_departements': stats_departements,
        'stats_fournisseurs': stats_fournisseurs,
        'activite_recente': activite_recente
    }
    
    return render_template('home/dashboard_admin.html', stats=stats)


def dashboard_generique():
    """Tableau de bord générique (fallback)."""
    user_dept_id = get_user_department_id()
    see_all = can_see_all_departments()
    
    if see_all:
        colis_par_statut = colis_service.countByStatut()
        commandes_par_statut = commande_service.countByStatut()
        activite_recente = historique_service.getRecent(10)
    else:
        colis_par_statut = colis_service.countByStatutAndDepartement(user_dept_id) if user_dept_id else {}
        commandes_par_statut = commande_service.countByStatutAndDepartement(user_dept_id) if user_dept_id else {}
        activite_recente = historique_service.getRecentByDepartement(user_dept_id, 10) if user_dept_id else []
    
    stats = {
        'total_colis': sum(colis_par_statut.values()) if colis_par_statut else 0,
        'total_commandes': sum(commandes_par_statut.values()) if commandes_par_statut else 0,
        'colis_en_attente': colis_par_statut.get('attendu', 0),
        'colis_a_distribuer': colis_par_statut.get('recu', 0) + colis_par_statut.get('en_distribution', 0),
        'colis_probleme': colis_par_statut.get('probleme', 0),
        'colis_par_statut': colis_par_statut,
        'commandes_par_statut': commandes_par_statut,
        'activite_recente': activite_recente
    }
    
    return render_template('home/dashboard.html', stats=stats)

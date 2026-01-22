"""Controller des colis.

Gere le suivi des colis de la reception a la livraison.

Routes :
- /colis : Liste des colis (avec filtre par statut)
- /colis/<id> : Detail d'un colis
- /colis/search : Recherche par numero de suivi
- /colis/en-attente : Colis en attente
- /colis/a-distribuer : Colis a distribuer
- /colis/incidents : Gestion des incidents (colis problematiques)
- /bons-livraison/<id>/colis/new : Creer un colis pour un BL

Actions (responsable_colis, admin) :
- /colis/<id>/receptionner : Marquer comme recu
- /colis/<id>/distribuer : Mettre en distribution
- /colis/<id>/livrer : Marquer comme livre
- /colis/<id>/probleme : Signaler un probleme
- /colis/<id>/resoudre : Resoudre un probleme

Acces par role :
- demandeur : voit uniquement les colis de son departement
- responsable_colis, admin : voient tous les colis + actions
- editeur : pas d'acces aux colis
"""

from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.controllers.AuthController import require_login, require_role, can_see_all_departments, get_user_department_id, is_demandeur
from app.services.ColisService import ColisService
from app.dao.BonLivraisonDAO import BonLivraisonDAO
from app.dao.DepartementDAO import DepartementDAO
from app.dao.UtilisateurDAO import UtilisateurDAO
from app.services.CommandeService import CommandeService

colis_service = ColisService()
bl_dao = BonLivraisonDAO()
commande_service = CommandeService()
departement_dao = DepartementDAO()
utilisateur_dao = UtilisateurDAO()


# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def get_destination_info(colis):
    """Recupere les infos de destination d'un colis."""
    if not colis.id_bl:
        return None
    
    bl = bl_dao.find_by_id(colis.id_bl)
    if not bl:
        return None
    
    commande = commande_service.getById(bl.id_commande)
    if not commande:
        return None
    
    departement = departement_dao.find_by_id(commande.id_departement)
    demandeur = None
    if commande.id_demandeur:
        demandeur = utilisateur_dao.find_by_id(commande.id_demandeur)
    
    return {
        'departement': departement.nom_departement if departement else 'Inconnu',
        'lieu': departement.lieu_livraison if departement else 'Non renseigne',
        'demandeur': f"{demandeur.prenom} {demandeur.nom}" if demandeur else None,
        'commande': commande.numero_bc,
        'id_departement': commande.id_departement
    }


def can_access_colis(colis):
    """Verifie si l'utilisateur peut acceder a ce colis."""
    if can_see_all_departments():
        return True
    
    user_dept_id = get_user_department_id()
    if not user_dept_id:
        return False
    
    # Utiliser la methode optimisee du service
    colis_dept_id = colis_service.getDepartementId(colis.id_colis)
    return colis_dept_id == user_dept_id


# =============================================================================
# ROUTES - LISTE ET RECHERCHE
# =============================================================================

@app.route('/colis')
@require_role(['demandeur', 'responsable_colis', 'admin'])
def colis_list():
    """Liste des colis avec filtre optionnel par statut."""
    statut = request.args.get('statut')
    user_dept_id = get_user_department_id()
    see_all = can_see_all_departments()
    
    # Utiliser les methodes optimisees SQL
    if statut:
        if see_all:
            colis = colis_service.getByStatut(statut)
        else:
            colis = colis_service.getByStatutAndDepartement(statut, user_dept_id) if user_dept_id else []
    else:
        if see_all:
            colis = colis_service.getAll()
        else:
            colis = colis_service.getByDepartement(user_dept_id) if user_dept_id else []
    
    for c in colis:
        c.destination = get_destination_info(c)
    return render_template('colis/list.html', colis=colis)


@app.route('/colis/en-attente')
@require_role(['demandeur', 'responsable_colis', 'admin'])
def colis_en_attente():
    """Liste des colis en attente d'arrivee."""
    user_dept_id = get_user_department_id()
    see_all = can_see_all_departments()
    
    if see_all:
        colis = colis_service.getEnAttente()
    else:
        colis = colis_service.getEnAttenteByDepartement(user_dept_id) if user_dept_id else []
    
    for c in colis:
        c.destination = get_destination_info(c)
    return render_template('colis/list.html', colis=colis, titre='Colis en attente')


@app.route('/colis/a-distribuer')
@require_role(['demandeur', 'responsable_colis', 'admin'])
def colis_a_distribuer():
    """Liste des colis a distribuer (recus ou en distribution)."""
    user_dept_id = get_user_department_id()
    see_all = can_see_all_departments()
    
    if see_all:
        colis = colis_service.getADistribuer()
    else:
        colis = colis_service.getADistribuerByDepartement(user_dept_id) if user_dept_id else []
    
    for c in colis:
        c.destination = get_destination_info(c)
    return render_template('colis/list.html', colis=colis, titre='Colis à distribuer')


@app.route('/colis/incidents')
@require_role(['responsable_colis', 'admin'])
def colis_incidents():
    """Page de gestion des incidents (colis problematiques)."""
    colis_problemes = colis_service.getByStatut('probleme')
    
    for c in colis_problemes:
        c.destination = get_destination_info(c)
    
    return render_template('colis/incidents.html', colis_problemes=colis_problemes)


@app.route('/colis/<int:id>')
@require_role(['demandeur', 'responsable_colis', 'admin'])
def colis_detail(id):
    """Detail d'un colis."""
    colis = colis_service.getById(id)
    if not colis:
        flash('Colis non trouvé.', 'error')
        return redirect(url_for('colis_list'))
    
    # Verifier l'acces pour les demandeurs
    if not can_access_colis(colis):
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('colis_list'))
    
    historique = colis_service.getHistorique(id)
    
    bl = None
    commande = None
    departement = None
    demandeur = None
    
    if colis.id_bl:
        bl = bl_dao.find_by_id(colis.id_bl)
        if bl:
            commande = commande_service.getById(bl.id_commande)
            if commande:
                departement = departement_dao.find_by_id(commande.id_departement)
                if commande.id_demandeur:
                    demandeur = utilisateur_dao.find_by_id(commande.id_demandeur)
    
    return render_template('colis/detail.html',
        colis=colis,
        historique=historique,
        bl=bl,
        commande=commande,
        departement=departement,
        demandeur=demandeur)


@app.route('/colis/search')
@require_role(['demandeur', 'responsable_colis', 'admin'])
def colis_search():
    """Recherche un colis par numero de suivi."""
    query = request.args.get('q', '')
    results = []
    
    if query:
        user_dept_id = get_user_department_id()
        see_all = can_see_all_departments()
        
        if see_all:
            results = colis_service.search(query)
        else:
            results = colis_service.searchByDepartement(query, user_dept_id) if user_dept_id else []
        
        for c in results:
            c.destination = get_destination_info(c)
    
    return render_template('colis/search.html', query=query, results=results)


@app.route('/colis/scan')
@require_role(['responsable_colis', 'admin'])
def colis_scan():
    """Interface de scan des colis."""
    return render_template('colis/scan.html')


# =============================================================================
# ROUTES - CREATION
# =============================================================================

@app.route('/bons-livraison/<int:id_bl>/colis/new', methods=['GET', 'POST'])
@require_role(['responsable_colis', 'admin'])
def colis_create(id_bl):
    """Creer un nouveau colis pour un bon de livraison."""
    bl = bl_dao.find_by_id(id_bl)
    if not bl:
        flash('Bon de livraison non trouvé.', 'error')
        return redirect(url_for('commandes_list'))
    
    commande = commande_service.getById(bl.id_commande)
    
    if request.method == 'POST':
        form = {
            'id_bl': id_bl,
            'num_suivi_transporteur': request.form.get('num_suivi_transporteur'),
            'nom_transporteur': request.form.get('nom_transporteur'),
            'statut_actuel': 'attendu',
            'notes': request.form.get('notes')
        }
        try:
            id_colis = colis_service.create(form)
            flash('Colis créé.', 'success')
            return redirect(url_for('colis_detail', id=id_colis))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    return render_template('colis/form.html', bl=bl, commande=commande)


# =============================================================================
# ACTIONS SUR LES COLIS (responsable_colis et admin uniquement)
# =============================================================================

@app.route('/colis/<int:id>/receptionner', methods=['POST'])
@require_role(['responsable_colis', 'admin'])
def colis_receptionner(id):
    """Marquer un colis comme recu a la reprographie."""
    lieu = request.form.get('lieu', 'Reprographie')
    try:
        colis_service.receptionner(id, session['user']['id'], lieu)
        flash('Colis réceptionné.', 'success')
    except Exception as e:
        flash(f'Erreur: {e}', 'error')
    return redirect(url_for('colis_detail', id=id))


@app.route('/colis/<int:id>/distribuer', methods=['POST'])
@require_role(['responsable_colis', 'admin'])
def colis_distribuer(id):
    """Mettre un colis en distribution."""
    try:
        colis_service.mettreEnDistribution(id, session['user']['id'])
        flash('Colis mis en distribution.', 'success')
    except Exception as e:
        flash(f'Erreur: {e}', 'error')
    return redirect(url_for('colis_detail', id=id))


@app.route('/colis/<int:id>/livrer', methods=['POST'])
@require_role(['responsable_colis', 'admin'])
def colis_livrer(id):
    """Marquer un colis comme livre au destinataire."""
    lieu = request.form.get('lieu')
    try:
        colis_service.livrer(id, session['user']['id'], lieu)
        flash('Colis livré.', 'success')
    except Exception as e:
        flash(f'Erreur: {e}', 'error')
    return redirect(url_for('colis_detail', id=id))


@app.route('/colis/<int:id>/probleme', methods=['POST'])
@require_role(['responsable_colis', 'admin'])
def colis_probleme(id):
    """Signaler un probleme sur un colis."""
    description = request.form.get('description', 'Problème non spécifié')
    try:
        colis_service.signalerProbleme(id, session['user']['id'], description)
        flash('Problème signalé.', 'warning')
    except Exception as e:
        flash(f'Erreur: {e}', 'error')
    return redirect(url_for('colis_detail', id=id))


@app.route('/colis/<int:id>/resoudre', methods=['POST'])
@require_role(['responsable_colis', 'admin'])
def colis_resoudre(id):
    """Resoudre un probleme sur un colis et le remettre dans le circuit."""
    nouveau_statut = request.form.get('nouveau_statut', 'recu')
    
    # Valider le statut choisi
    statuts_valides = ['attendu', 'recu', 'en_distribution']
    if nouveau_statut not in statuts_valides:
        flash('Statut invalide.', 'error')
        return redirect(url_for('colis_detail', id=id))
    
    try:
        colis_service.resoudreProbleme(id, session['user']['id'], nouveau_statut)
        flash('Problème résolu, colis remis en circuit.', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    except Exception as e:
        flash(f'Erreur: {e}', 'error')
    return redirect(url_for('colis_detail', id=id))

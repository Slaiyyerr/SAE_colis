"""Controller d'administration.

Reserve aux utilisateurs avec le role 'admin'.
Gere les referentiels et le reporting.

Routes :
- /admin : Redirige vers le dashboard unifie (home)
- /admin/reporting : Statistiques detaillees par fournisseur/departement
- /admin/utilisateurs : Gestion des utilisateurs
- /admin/departements : Gestion des departements
"""

from flask import render_template, request, redirect, url_for, flash
from app import app
from app.controllers.AuthController import require_role
from app.services.UtilisateurService import UtilisateurService
from app.services.DepartementService import DepartementService
from app.services.ReportingService import ReportingService


user_service = UtilisateurService()
departement_service = DepartementService()
reporting_service = ReportingService()


# =============================================================================
# DASHBOARD & REPORTING
# =============================================================================

@app.route('/admin')
@require_role(['admin'])
def admin_dashboard():
    """Redirige vers le dashboard unifie pour eviter la confusion."""
    return redirect(url_for('home'))


@app.route('/admin/reporting')
@require_role(['admin'])
def admin_reporting():
    """Statistiques detaillees pour pilotage."""
    data = reporting_service.getDashboardData()
    stats_fournisseurs = reporting_service.getStatsFournisseurs()
    stats_departements = reporting_service.getStatsDepartements()
    return render_template('admin/reporting.html',
        data=data,
        stats_fournisseurs=stats_fournisseurs,
        stats_departements=stats_departements)


# =============================================================================
# GESTION DES UTILISATEURS
# =============================================================================

@app.route('/admin/utilisateurs')
@require_role(['admin'])
def admin_utilisateurs():
    """Liste de tous les utilisateurs."""
    return render_template('admin/utilisateurs.html', utilisateurs=user_service.getAll())


@app.route('/admin/utilisateurs/new', methods=['GET', 'POST'])
@require_role(['admin'])
def admin_utilisateur_create():
    """Ajouter un nouvel utilisateur."""
    if request.method == 'POST':
        form = {
            'email': request.form.get('email'),
            'mot_de_passe': request.form.get('mot_de_passe') or 'password',
            'nom': request.form.get('nom'),
            'prenom': request.form.get('prenom'),
            'role': request.form.get('role'),
            'id_departement': request.form.get('id_departement') or None
        }
        try:
            user_service.create(form)
            flash('Utilisateur créé. Mot de passe par défaut: password', 'success')
            return redirect(url_for('admin_utilisateurs'))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    return render_template('admin/utilisateur_form.html',
        departements=departement_service.getAll())


@app.route('/admin/utilisateurs/<int:id>/edit', methods=['GET', 'POST'])
@require_role(['admin'])
def admin_utilisateur_edit(id):
    """Modifier un utilisateur (role, departement)."""
    utilisateur = user_service.getById(id)
    if not utilisateur:
        flash('Utilisateur non trouvé', 'error')
        return redirect(url_for('admin_utilisateurs'))
    
    if request.method == 'POST':
        form = {
            'email': request.form.get('email'),
            'nom': request.form.get('nom'),
            'prenom': request.form.get('prenom'),
            'role': request.form.get('role'),
            'id_departement': request.form.get('id_departement') or None
        }
        # Mot de passe optionnel (ne change que si rempli)
        mdp = request.form.get('mot_de_passe')
        if mdp:
            form['mot_de_passe'] = mdp
        try:
            user_service.update(id, form)
            flash('Utilisateur mis à jour.', 'success')
            return redirect(url_for('admin_utilisateurs'))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    return render_template('admin/utilisateur_form.html',
        utilisateur=utilisateur,
        departements=departement_service.getAll())


@app.route('/admin/utilisateurs/<int:id>/toggle', methods=['POST'])
@require_role(['admin'])
def admin_utilisateur_toggle(id):
    """Activer/désactiver un utilisateur."""
    utilisateur = user_service.getById(id)
    if utilisateur:
        try:
            if utilisateur.est_actif:
                user_service.desactiver(id)
            else:
                user_service.activer(id)
            flash('Statut modifié', 'success')
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    return redirect(url_for('admin_utilisateurs'))


# =============================================================================
# GESTION DES DEPARTEMENTS
# =============================================================================

@app.route('/admin/departements')
@require_role(['admin'])
def admin_departements():
    """Liste des départements de l'IUT."""
    return render_template('admin/departements.html',
        departements=departement_service.getAll())


@app.route('/admin/departements/new', methods=['GET', 'POST'])
@require_role(['admin'])
def admin_departement_create():
    """Créer un nouveau département"""
    if request.method == 'POST':
        form = {
            'nom_departement': request.form.get('nom_departement'),
            'lieu_livraison': request.form.get('lieu_livraison')
        }
        try:
            departement_service.create(form)
            flash('Département créé.', 'success')
            return redirect(url_for('admin_departements'))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    return render_template('admin/departement_form.html')


@app.route('/admin/departements/<int:id>/edit', methods=['GET', 'POST'])
@require_role(['admin'])
def admin_departement_edit(id):
    """Modifier un departement."""
    departement = departement_service.getById(id)
    if not departement:
        flash('Département non trouvé.', 'error')
        return redirect(url_for('admin_departements'))
    
    if request.method == 'POST':
        form = {
            'nom_departement': request.form.get('nom_departement'),
            'lieu_livraison': request.form.get('lieu_livraison')
        }
        try:
            departement_service.update(id, form)
            flash('Département mis à jour.', 'success')
            return redirect(url_for('admin_departements'))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    return render_template('admin/departement_form.html', departement=departement)


@app.route('/admin/departements/<int:id>/delete', methods=['GET', 'POST'])
@require_role(['admin'])
def admin_departement_delete(id):
    """Supprimer un departement."""
    departement = departement_service.getById(id)
    if not departement:
        flash('Département non trouvé.', 'error')
        return redirect(url_for('admin_departements'))
    
    if request.method == 'POST':
        try:
            departement_service.delete(id)
            flash('Département supprimé.', 'success')
            return redirect(url_for('admin_departements'))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
            return redirect(url_for('admin_departements'))
    
    return render_template('admin/confirm_delete.html',
        titre='Supprimer le département',
        message=f'Voulez-vous vraiment supprimer le département "{departement.nom_departement}" ?',
        warning='Les utilisateurs rattachés à ce département seront dissociés.',
        cancel_url=url_for('admin_departements'))

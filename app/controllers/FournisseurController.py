"""Controller des fournisseurs.

Gere les operations CRUD sur les fournisseurs.

Routes :
- /fournisseurs : Liste des fournisseurs
- /fournisseurs/<id> : Detail d'un fournisseur avec ses commandes
- /fournisseurs/new : Creer un fournisseur (editeur, admin)
- /fournisseurs/<id>/edit : Modifier un fournisseur (editeur, admin)
- /fournisseurs/<id>/delete : Supprimer un fournisseur (admin)

Acces par role :
- editeur, admin : acces complet
- demandeur, responsable_colis : pas d'acces
"""

from flask import render_template, request, redirect, url_for, flash
from app import app
from app.controllers.AuthController import require_role
from app.services.FournisseurService import FournisseurService
from app.services.CommandeService import CommandeService

fournisseur_service = FournisseurService()
commande_service = CommandeService()


@app.route('/fournisseurs')
@require_role(['editeur', 'admin'])
def fournisseurs_list():
    """Liste de tous les fournisseurs."""
    fournisseurs = fournisseur_service.getAll()
    return render_template('fournisseurs/list.html', fournisseurs=fournisseurs)


@app.route('/fournisseurs/<int:id>')
@require_role(['editeur', 'admin'])
def fournisseur_detail(id):
    """Detail d'un fournisseur avec la liste de ses commandes."""
    fournisseur = fournisseur_service.getById(id)
    if not fournisseur:
        flash('Fournisseur non trouvé.', 'error')
        return redirect(url_for('fournisseurs_list'))
    
    # Récupérer les commandes de ce fournisseur
    commandes = commande_service.getByFournisseur(id)
    
    return render_template('fournisseurs/detail.html', 
        fournisseur=fournisseur,
        commandes=commandes)


@app.route('/fournisseurs/new', methods=['GET', 'POST'])
@require_role(['editeur', 'admin'])
def fournisseur_create():
    """Creer un nouveau fournisseur."""
    if request.method == 'POST':
        form = {
            'nom_societe': request.form.get('nom_societe'),
            'contact_nom': request.form.get('contact_nom'),
            'telephone': request.form.get('telephone'),
            'email': request.form.get('email'),
            'notes_internes': request.form.get('notes_internes')
        }
        try:
            fournisseur_service.create(form)
            flash('Fournisseur créé.', 'success')
            return redirect(url_for('fournisseurs_list'))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    return render_template('fournisseurs/form.html')


@app.route('/fournisseurs/<int:id>/edit', methods=['GET', 'POST'])
@require_role(['editeur', 'admin'])
def fournisseur_edit(id):
    """Modifier un fournisseur existant."""
    fournisseur = fournisseur_service.getById(id)
    if not fournisseur:
        flash('Fournisseur non trouvé.', 'error')
        return redirect(url_for('fournisseurs_list'))
    
    if request.method == 'POST':
        form = {
            'nom_societe': request.form.get('nom_societe'),
            'contact_nom': request.form.get('contact_nom'),
            'telephone': request.form.get('telephone'),
            'email': request.form.get('email'),
            'notes_internes': request.form.get('notes_internes')
        }
        try:
            fournisseur_service.update(id, form)
            flash('Fournisseur mis à jour.', 'success')
            return redirect(url_for('fournisseur_detail', id=id))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    return render_template('fournisseurs/form.html', fournisseur=fournisseur)


@app.route('/fournisseurs/<int:id>/delete', methods=['GET', 'POST'])
@require_role(['admin'])
def fournisseur_delete(id):
    """Supprimer un fournisseur (avec page de confirmation)."""
    fournisseur = fournisseur_service.getById(id)
    if not fournisseur:
        flash('Fournisseur non trouvé.', 'error')
        return redirect(url_for('fournisseurs_list'))
    
    if request.method == 'POST':
        try:
            fournisseur_service.delete(id)
            flash('Fournisseur supprimé.', 'success')
            return redirect(url_for('fournisseurs_list'))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
            return redirect(url_for('fournisseurs_list'))
    
    return render_template('admin/confirm_delete.html',
        titre='Supprimer le fournisseur',
        message=f'Voulez-vous vraiment supprimer "{fournisseur.nom_societe}" ?',
        warning='Toutes les commandes associées seront également supprimées.',
        cancel_url=url_for('fournisseur_detail', id=id))

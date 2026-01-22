"""Controller des bons de livraison.

Gere les BL recus des fournisseurs.

Routes :
- /bons-livraison/<id> : Detail d'un BL
- /commandes/<id>/bons-livraison/new : Creer un BL pour une commande
- /bons-livraison/<id>/edit : Modifier un BL
- /bons-livraison/<id>/delete : Supprimer un BL

Acces par role :
- demandeur : voit les BL de son departement (lecture seule)
- editeur : voit tous les BL (lecture seule)
- responsable_colis : voit tous les BL + CRUD
- admin : acces complet
"""

from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.controllers.AuthController import require_login, require_role, can_see_all_departments, get_user_department_id
from app.dao.BonLivraisonDAO import BonLivraisonDAO
from app.dao.ColisDAO import ColisDAO
from app.services.CommandeService import CommandeService
from app.utils.upload import save_file, delete_file, get_file_url

bl_dao = BonLivraisonDAO()
colis_dao = ColisDAO()
commande_service = CommandeService()


def can_access_bon_livraison(bl):
    """Verifie si l'utilisateur peut acceder a ce BL."""
    if can_see_all_departments():
        return True
    
    user_dept_id = get_user_department_id()
    if not user_dept_id:
        return False
    
    # Recuperer la commande pour avoir le departement
    commande = commande_service.getById(bl.id_commande)
    if commande and commande.id_departement == user_dept_id:
        return True
    
    return False


@app.route('/bons-livraison/<int:id>')
@require_login
def bon_livraison_detail(id):
    """Detail d'un bon de livraison avec ses colis."""
    bl = bl_dao.find_by_id(id)
    if not bl:
        flash('Bon de livraison non trouv\u00e9.', 'error')
        return redirect(url_for('commandes_list'))
    
    # Verifier l'acces pour les demandeurs
    if not can_access_bon_livraison(bl):
        flash('Acc\u00e8s non autoris\u00e9.', 'error')
        return redirect(url_for('commandes_list'))
    
    commande = commande_service.getById(bl.id_commande)
    colis_list = colis_dao.find_by_bl(id)
    bl.fichier_bl_url = get_file_url(bl.fichier_bl) if bl.fichier_bl else None
    
    return render_template('bons_livraison/detail.html', bl=bl, commande=commande, colis_list=colis_list)


@app.route('/commandes/<int:id_commande>/bons-livraison/new', methods=['GET', 'POST'])
@require_role(['responsable_colis', 'admin'])
def bon_livraison_create(id_commande):
    """Creer un nouveau BL pour une commande.
    
    Permet aussi de creer les colis associes en meme temps.
    Met a jour le statut de la commande en 'en_cours'.
    """
    commande = commande_service.getById(id_commande)
    if not commande:
        flash('Commande non trouv\u00e9e.', 'error')
        return redirect(url_for('commandes_list'))
    
    if request.method == 'POST':
        # Upload du fichier BL
        fichier_bl = None
        if 'fichier_bl' in request.files:
            file = request.files['fichier_bl']
            if file and file.filename:
                try:
                    fichier_bl = save_file(file, 'bl')
                except ValueError as e:
                    flash(str(e), 'error')
                    return render_template('bons_livraison/form.html', commande=commande)
        
        form = {
            'id_commande': id_commande,
            'num_bl_fournisseur': request.form.get('num_bl_fournisseur'),
            'date_bl': request.form.get('date_bl') or None,
            'fichier_bl': fichier_bl
        }
        
        try:
            id_bl = bl_dao.create(form)
            
            # Creer les colis associes
            nb_colis = int(request.form.get('nb_colis', 1))
            for i in range(nb_colis):
                num_suivi = request.form.get(f'num_suivi_{i}')
                transporteur = request.form.get(f'transporteur_{i}')
                if num_suivi or transporteur:
                    colis_dao.create({
                        'id_bl': id_bl,
                        'num_suivi_transporteur': num_suivi,
                        'nom_transporteur': transporteur,
                        'statut_actuel': 'attendu'
                    })
            
            # Mettre a jour le statut de la commande
            commande_service.update(id_commande, {'statut_global': 'en_cours'})
            
            flash('Bon de livraison cr\u00e9\u00e9.', 'success')
            return redirect(url_for('bon_livraison_detail', id=id_bl))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    return render_template('bons_livraison/form.html', commande=commande)


@app.route('/bons-livraison/<int:id>/edit', methods=['GET', 'POST'])
@require_role(['responsable_colis', 'admin'])
def bon_livraison_edit(id):
    """Modifier un bon de livraison."""
    bl = bl_dao.find_by_id(id)
    if not bl:
        flash('Bon de livraison non trouv\u00e9.', 'error')
        return redirect(url_for('commandes_list'))
    
    commande = commande_service.getById(bl.id_commande)
    
    if request.method == 'POST':
        # Gestion du fichier BL
        fichier_bl = bl.fichier_bl
        if 'fichier_bl' in request.files:
            file = request.files['fichier_bl']
            if file and file.filename:
                try:
                    if bl.fichier_bl:
                        delete_file(bl.fichier_bl)
                    fichier_bl = save_file(file, 'bl')
                except ValueError as e:
                    flash(str(e), 'error')
                    bl.fichier_bl_url = get_file_url(bl.fichier_bl) if bl.fichier_bl else None
                    return render_template('bons_livraison/form.html', bl=bl, commande=commande)
        
        form = {
            'num_bl_fournisseur': request.form.get('num_bl_fournisseur'),
            'date_bl': request.form.get('date_bl') or None,
            'fichier_bl': fichier_bl
        }
        
        try:
            bl_dao.update(id, form)
            flash('Bon de livraison mis \u00e0 jour.', 'success')
            return redirect(url_for('bon_livraison_detail', id=id))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    bl.fichier_bl_url = get_file_url(bl.fichier_bl) if bl.fichier_bl else None
    return render_template('bons_livraison/form.html', bl=bl, commande=commande)


@app.route('/bons-livraison/<int:id>/delete', methods=['GET', 'POST'])
@require_role(['admin'])
def bon_livraison_delete(id):
    """Supprimer un bon de livraison (avec page de confirmation)."""
    bl = bl_dao.find_by_id(id)
    if not bl:
        flash('Bon de livraison non trouv\u00e9.', 'error')
        return redirect(url_for('commandes_list'))
    
    if request.method == 'POST':
        try:
            if bl.fichier_bl:
                delete_file(bl.fichier_bl)
            id_commande = bl.id_commande
            bl_dao.delete(id)
            flash('Bon de livraison supprim\u00e9.', 'success')
            return redirect(url_for('commande_detail', id=id_commande))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
            return redirect(url_for('bon_livraison_detail', id=id))
    
    return render_template('admin/confirm_delete.html',
        titre='Supprimer le bon de livraison',
        message=f'Voulez-vous vraiment supprimer le BL "{bl.num_bl_fournisseur}" ?',
        warning='Tous les colis associ\u00e9s seront \u00e9galement supprim\u00e9s.',
        cancel_url=url_for('bon_livraison_detail', id=id))

"""Controller des commandes (bons de commande).

Gere les operations CRUD sur les commandes.

Routes :
- /commandes : Liste des commandes (avec filtre par statut)
- /commandes/<id> : Detail d'une commande
- /commandes/new : Creer une commande (editeur, admin)
- /commandes/<id>/edit : Modifier une commande (editeur, admin)
- /commandes/<id>/delete : Supprimer une commande (admin)

Acces par role :
- demandeur : voit uniquement les commandes de son departement (lecture seule)
- editeur : voit toutes les commandes + CRUD
- responsable_colis : voit toutes les commandes (lecture seule)
- admin : acces complet
"""

from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.controllers.AuthController import require_login, require_role, can_see_all_departments, get_user_department_id
from app.services.CommandeService import CommandeService
from app.services.FournisseurService import FournisseurService
from app.services.DepartementService import DepartementService
from app.services.NotificationService import NotificationService
from app.services.UtilisateurService import UtilisateurService
from app.utils.upload import save_file, delete_file, get_file_url

commande_service = CommandeService()
fournisseur_service = FournisseurService()
departement_service = DepartementService()
notif_service = NotificationService()
utilisateur_service = UtilisateurService()


# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def filter_commandes_by_department(commandes):
    """Filtre les commandes par departement pour les demandeurs."""
    if can_see_all_departments():
        return commandes
    
    user_dept_id = get_user_department_id()
    if not user_dept_id:
        return []
    
    return [c for c in commandes if c.id_departement == user_dept_id]


def can_access_commande(commande):
    """Verifie si l'utilisateur peut acceder a cette commande."""
    if can_see_all_departments():
        return True
    
    user_dept_id = get_user_department_id()
    return commande.id_departement == user_dept_id


def get_demandeurs():
    """Retourne la liste des demandeurs actifs pour le formulaire."""
    return utilisateur_service.getByRole('demandeur')


# =============================================================================
# ROUTES - LISTE ET DETAIL
# =============================================================================

@app.route('/commandes')
@require_login
def commandes_list():
    """Liste des commandes avec filtre optionnel par statut."""
    statut = request.args.get('statut')
    commandes = commande_service.getByStatut(statut) if statut else commande_service.getAll()
    
    # Filtrer par departement pour les demandeurs
    commandes = filter_commandes_by_department(commandes)
    
    return render_template('commandes/list.html', commandes=commandes)


@app.route('/commandes/<int:id>')
@require_login
def commande_detail(id):
    """Detail d'une commande avec ses lignes et bons de livraison."""
    commande = commande_service.getById(id)
    if not commande:
        flash('Commande non trouvée.', 'error')
        return redirect(url_for('commandes_list'))
    
    # Verifier l'acces pour les demandeurs
    if not can_access_commande(commande):
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('commandes_list'))
    
    lignes = commande_service.getLignes(id)
    bons_livraison = commande_service.getBonsLivraison(id)
    
    # Ajouter l'URL du fichier BC pour l'affichage
    commande.fichier_bc_url = get_file_url(commande.fichier_bc) if commande.fichier_bc else None
    
    return render_template('commandes/detail.html', commande=commande, lignes=lignes, bons_livraison=bons_livraison)


# =============================================================================
# ROUTES - CREATION ET MODIFICATION (editeur, admin)
# =============================================================================

@app.route('/commandes/new', methods=['GET', 'POST'])
@require_role(['editeur', 'admin'])
def commande_create():
    """Creer une nouvelle commande."""
    if request.method == 'POST':
        # Upload du fichier BC
        fichier_bc = None
        if 'fichier_bc' in request.files:
            file = request.files['fichier_bc']
            if file and file.filename:
                try:
                    fichier_bc = save_file(file, 'bc')
                except ValueError as e:
                    flash(str(e), 'error')
                    return render_template('commandes/form.html',
                        fournisseurs=fournisseur_service.getAll(),
                        departements=departement_service.getAll(),
                        demandeurs=get_demandeurs())
        
        # Recuperer id_demandeur du formulaire (peut etre vide)
        id_demandeur = request.form.get('id_demandeur')
        if id_demandeur == '' or id_demandeur is None:
            id_demandeur = None
        else:
            id_demandeur = int(id_demandeur)
        
        # Donnees de la commande
        form = {
            'numero_bc': request.form.get('numero_bc'),
            'id_fournisseur': request.form.get('id_fournisseur'),
            'id_departement': request.form.get('id_departement'),
            'id_demandeur': id_demandeur,
            'date_livraison_prevue': request.form.get('date_livraison_prevue'),
            'notes': request.form.get('notes'),
            'fichier_bc': fichier_bc
        }
        
        # Lignes de commande (articles)
        lignes = []
        refs = request.form.getlist('ref_produit[]')
        designations = request.form.getlist('designation[]')
        quantites = request.form.getlist('quantite[]')
        for i in range(len(designations)):
            if designations[i]:
                lignes.append({
                    'ref_produit': refs[i] if i < len(refs) else '',
                    'designation': designations[i],
                    'quantite': int(quantites[i]) if i < len(quantites) and quantites[i] else 1
                })
        
        try:
            id_commande = commande_service.create(form, lignes)
            flash('Commande créée.', 'success')
            notif_service.notifierNouvelleCommande(id_commande)
            return redirect(url_for('commande_detail', id=id_commande))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    return render_template('commandes/form.html',
        fournisseurs=fournisseur_service.getAll(),
        departements=departement_service.getAll(),
        demandeurs=get_demandeurs())


@app.route('/commandes/<int:id>/edit', methods=['GET', 'POST'])
@require_role(['editeur', 'admin'])
def commande_edit(id):
    """Modifier une commande existante."""
    commande = commande_service.getById(id)
    if not commande:
        flash('Commande non trouvée.', 'error')
        return redirect(url_for('commandes_list'))
    
    if request.method == 'POST':
        # Gestion du fichier BC (remplacement si nouveau fichier)
        fichier_bc = commande.fichier_bc
        if 'fichier_bc' in request.files:
            file = request.files['fichier_bc']
            if file and file.filename:
                try:
                    if commande.fichier_bc:
                        delete_file(commande.fichier_bc)
                    fichier_bc = save_file(file, 'bc')
                except ValueError as e:
                    flash(str(e), 'error')
                    lignes = commande_service.getLignes(id)
                    return render_template('commandes/form.html',
                        commande=commande, lignes=lignes,
                        fournisseurs=fournisseur_service.getAll(),
                        departements=departement_service.getAll(),
                        demandeurs=get_demandeurs())
        
        # Recuperer id_demandeur du formulaire
        id_demandeur = request.form.get('id_demandeur')
        if id_demandeur == '' or id_demandeur is None:
            id_demandeur = None
        else:
            id_demandeur = int(id_demandeur)
        
        form = {
            'numero_bc': request.form.get('numero_bc'),
            'id_fournisseur': request.form.get('id_fournisseur'),
            'id_departement': request.form.get('id_departement'),
            'id_demandeur': id_demandeur,
            'date_livraison_prevue': request.form.get('date_livraison_prevue'),
            'statut_global': request.form.get('statut_global'),
            'notes': request.form.get('notes'),
            'fichier_bc': fichier_bc
        }
        
        try:
            commande_service.update(id, form)
            flash('Commande mise à jour.', 'success')
            return redirect(url_for('commande_detail', id=id))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    lignes = commande_service.getLignes(id)
    commande.fichier_bc_url = get_file_url(commande.fichier_bc) if commande.fichier_bc else None
    return render_template('commandes/form.html',
        commande=commande, lignes=lignes,
        fournisseurs=fournisseur_service.getAll(),
        departements=departement_service.getAll(),
        demandeurs=get_demandeurs())


@app.route('/commandes/<int:id>/delete', methods=['GET', 'POST'])
@require_role(['admin'])
def commande_delete(id):
    """Supprimer une commande (avec page de confirmation)."""
    commande = commande_service.getById(id)
    if not commande:
        flash('Commande non trouvée.', 'error')
        return redirect(url_for('commandes_list'))
    
    if request.method == 'POST':
        try:
            if commande.fichier_bc:
                delete_file(commande.fichier_bc)
            commande_service.delete(id)
            flash('Commande supprimée.', 'success')
            return redirect(url_for('commandes_list'))
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
            return redirect(url_for('commandes_list'))
    
    return render_template('admin/confirm_delete.html',
        titre='Supprimer la commande',
        message=f'Voulez-vous vraiment supprimer la commande "{commande.numero_bc}" ?',
        warning='Tous les bons de livraison et colis associés seront également supprimés.',
        cancel_url=url_for('commande_detail', id=id))

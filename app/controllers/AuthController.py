"""Controller d'authentification.

Gere la connexion/deconnexion par email + mot de passe.

Routes :
- /login : Page de connexion
- /login (POST) : Traitement du formulaire
- /logout : Deconnexion
- /unauthorized : Page d'erreur acces refuse

Decorateurs fournis :
- @require_login : Verifie que l'utilisateur est connecte
- @require_role(['admin', 'editeur']) : Verifie le role

Fonctions helpers :
- can_see_all_departments() : True si l'utilisateur voit tous les departements
- get_user_department_id() : Retourne l'ID du departement de l'utilisateur
"""

from functools import wraps
from flask import render_template, redirect, url_for, session, request, flash
from app import app
from app.services.UtilisateurService import UtilisateurService

user_service = UtilisateurService()


# =============================================================================
# FONCTIONS HELPERS POUR LA GESTION DES ACCES
# =============================================================================

def can_see_all_departments():
    """Verifie si l'utilisateur peut voir tous les departements.
    
    Retourne True pour : admin, responsable_colis, editeur
    Retourne False pour : demandeur
    """
    if 'user' not in session:
        return False
    role = session['user'].get('role')
    return role in ['admin', 'responsable_colis', 'editeur']


def get_user_department_id():
    """Retourne l'ID du departement de l'utilisateur connecte.
    
    Retourne None si l'utilisateur n'est pas connecte ou n'a pas de departement.
    """
    if 'user' not in session:
        return None
    return session['user'].get('id_departement')


def get_current_user():
    """Retourne les informations de l'utilisateur connecte."""
    return session.get('user')


def is_demandeur():
    """Verifie si l'utilisateur est un demandeur."""
    if 'user' not in session:
        return False
    return session['user'].get('role') == 'demandeur'


def is_admin():
    """Verifie si l'utilisateur est un admin."""
    if 'user' not in session:
        return False
    return session['user'].get('role') == 'admin'


def is_responsable_colis():
    """Verifie si l'utilisateur est responsable colis."""
    if 'user' not in session:
        return False
    return session['user'].get('role') == 'responsable_colis'


def is_editeur():
    """Verifie si l'utilisateur est editeur."""
    if 'user' not in session:
        return False
    return session['user'].get('role') == 'editeur'


# =============================================================================
# DECORATEURS
# =============================================================================

def require_login(f):
    """Decorateur : redirige vers /login si non connecte."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            session['next_url'] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def require_role(roles):
    """Decorateur : verifie que l'utilisateur a un des roles autorises.
    
    Usage : @require_role(['admin', 'editeur'])
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user' not in session:
                session['next_url'] = request.url
                return redirect(url_for('login'))
            if session['user'].get('role') not in roles:
                return redirect(url_for('unauthorized'))
            return f(*args, **kwargs)
        return decorated
    return decorator


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion avec formulaire email + mot de passe"""
    if 'user' in session:
        # Rediriger les admins vers /admin, les autres vers /home
        if session['user'].get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            flash('Email et mot de passe requis', 'error')
            return render_template('auth/login.html')
        
        # Verifier que l'utilisateur existe
        user = user_service.getByEmail(email)
        if not user:
            flash('Email ou mot de passe incorrect', 'error')
            return render_template('auth/login.html')
        
        # Verifier le mot de passe (comparaison simple pour demo)
        # En production, utiliser bcrypt.check_password_hash()
        if user.mot_de_passe != password:
            flash('Email ou mot de passe incorrect', 'error')
            return render_template('auth/login.html')
        
        # Verifier que le compte est actif
        if not user.est_actif:
            flash('Compte d\u00e9sactiv\u00e9', 'error')
            return render_template('auth/login.html')
        
        # Creer la session
        session['user'] = {
            'id': user.id_utilisateur,
            'email': user.email,
            'nom': user.nom,
            'prenom': user.prenom,
            'role': user.role,
            'id_departement': user.id_departement
        }
        flash(f'Bienvenue {user.prenom} !', 'success')
        
        # Rediriger selon le r\u00f4le : admin vers /admin, autres vers /home
        if user.role == 'admin':
            return redirect(session.pop('next_url', None) or url_for('admin_dashboard'))
        return redirect(session.pop('next_url', None) or url_for('home'))
    
    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    """Deconnexion : vide la session."""
    session.clear()
    flash('D\u00e9connect\u00e9', 'info')
    return redirect(url_for('login'))


@app.route('/unauthorized')
def unauthorized():
    """Page d'erreur : acces refuse (role insuffisant)."""
    return render_template('auth/unauthorized.html')

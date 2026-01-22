"""Controller des notifications.

Gere l'affichage et le marquage des notifications utilisateur.

Routes :
- /notifications : Liste des notifications
- /notifications/<id>/lire : Marquer une notification comme lue
- /notifications/tout-lire : Marquer toutes comme lues
- /api/notifications/count : API JSON pour le badge (AJAX)
"""

from flask import render_template, redirect, url_for, flash, session, jsonify
from app import app
from app.controllers.AuthController import require_login
from app.services.NotificationService import NotificationService

notif_service = NotificationService()


@app.route('/notifications')
@require_login
def notifications_list():
    """Liste des notifications de l'utilisateur connecte."""
    notifications = notif_service.getByUtilisateur(session['user']['id'])
    return render_template('notifications/list.html', notifications=notifications)


@app.route('/notifications/<int:id>/lire', methods=['POST'])
@require_login
def notification_lire(id):
    """Marque une notification comme lue."""
    notif_service.marquerLue(id)
    return redirect(url_for('notifications_list'))


@app.route('/notifications/tout-lire', methods=['POST'])
@require_login
def notifications_tout_lire():
    """Marque toutes les notifications comme lues."""
    notif_service.marquerToutesLues(session['user']['id'])
    flash('Toutes les notifications marquees comme lues.', 'success')
    return redirect(url_for('notifications_list'))


@app.route('/api/notifications/count')
@require_login
def api_notifications_count():
    """API JSON : retourne le nombre de notifications non lues.
    
    Utilise pour mettre a jour le badge en AJAX.
    """
    count = notif_service.countNonLues(session['user']['id'])
    return jsonify({'count': count})


@app.context_processor
def inject_notifications_count():
    """Injecte le compteur de notifications dans tous les templates.
    
    Permet d'afficher le badge dans la navbar sans modifier chaque controller.
    Usage dans template : {{ notifications_count }}
    """
    if 'user' in session:
        try:
            count = notif_service.countNonLues(session['user']['id'])
            return {'notifications_count': count}
        except Exception:
            return {'notifications_count': 0}
    return {'notifications_count': 0}

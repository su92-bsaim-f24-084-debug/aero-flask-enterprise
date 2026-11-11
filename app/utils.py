from functools import wraps
from flask import session, redirect, url_for, flash, request, g
from app.models import User

def load_logged_in_user():
    """Loads logged-in user from session before each request."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id, is_deleted=False).first()

def login_required(view):
    """Ensures user is authenticated in session."""
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    """Ensures user has admin privileges."""
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please sign in with administrator credentials.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        if not g.user.is_admin():
            flash("Administrator privileges required to access this resource.", "danger")
            return redirect(url_for('main.index'))
        return view(**kwargs)
    return wrapped_view

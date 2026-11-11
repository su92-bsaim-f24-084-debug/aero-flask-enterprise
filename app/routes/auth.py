from flask import Blueprint, render_template, redirect, url_for, flash, request, session, g
from app.models import db, User, UserProfile
from app.forms import LoginForm, RegisterForm, ProfileForm
from app.utils import login_required

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Server-side validated user registration using WTForms."""
    if g.user:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            role='customer'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()  # populate user.id

        # Create linked profile
        profile = UserProfile(
            user_id=user.id,
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip()
        )
        db.session.add(profile)
        db.session.commit()

        # Set session & cookie (Post-Redirect-Get)
        session.clear()
        session['user_id'] = user.id
        session.permanent = True
        flash(f"Welcome aboard, {user.username}! Your account has been created.", "success")
        return redirect(url_for('main.index'))

    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User authentication with session state management."""
    if g.user:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.username_or_email.data.strip()
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower()),
            User.is_deleted == False
        ).first()

        if user and user.check_password(form.password.data):
            session.clear()
            session['user_id'] = user.id
            session.permanent = bool(form.remember_me.data)
            flash(f"Welcome back, {user.username}!", "success")

            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('main.index'))

        flash("Invalid username/email or password. Please verify your credentials.", "danger")

    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    """Clears user session and cookies."""
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for('main.index'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management."""
    form = ProfileForm()
    user_prof = g.user.profile

    if form.validate_on_submit():
        if not user_prof:
            user_prof = UserProfile(user_id=g.user.id)
            db.session.add(user_prof)

        user_prof.first_name = form.first_name.data.strip()
        user_prof.last_name = form.last_name.data.strip()
        user_prof.phone_number = form.phone_number.data.strip() if form.phone_number.data else None
        user_prof.nationality = form.nationality.data.strip() if form.nationality.data else None
        user_prof.passport_number = form.passport_number.data.strip() if form.passport_number.data else None
        db.session.commit()

        flash("Profile updated successfully!", "success")
        return redirect(url_for('auth.profile'))

    elif request.method == 'GET' and user_prof:
        form.first_name.data = user_prof.first_name
        form.last_name.data = user_prof.last_name
        form.phone_number.data = user_prof.phone_number
        form.nationality.data = user_prof.nationality
        form.passport_number.data = user_prof.passport_number

    return render_template('auth/profile.html', form=form, profile=user_prof)

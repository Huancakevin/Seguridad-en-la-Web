from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from blueprintapp.app import db
from blueprintapp.auth.models import User

bp_auth = Blueprint('bp_auth', __name__, template_folder='templates')

@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('bp_core.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Bienvenido de nuevo, ' + user.username + '!', 'success')
            return redirect(url_for('bp_core.index'))
        flash('Usuario o contraseña incorrecta.', 'danger')

    return render_template('auth/login.html')

@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('bp_core.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not username or not email or not password:
            flash('Completa todos los campos.', 'warning')
        elif password != password2:
            flash('Las contraseñas no coinciden.', 'warning')
        elif User.query.filter((User.username == username) | (User.email == email)).first():
            flash('El nombre de usuario o el email ya está en uso.', 'warning')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Cuenta creada correctamente. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('bp_auth.login'))

    return render_template('auth/register.html')

@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('bp_core.index'))

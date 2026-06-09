from flask import request, render_template, redirect, url_for, Blueprint
from flask_login import current_user
from blueprintapp.app import db
from blueprintapp.miembros.models import Miembro

bp_miembro = Blueprint('bp_miembro', __name__, template_folder='templates')

@bp_miembro.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('bp_auth.login'))

@bp_miembro.route("/")
def index():
    miembros = Miembro.query.all()
    return render_template('miembro/index.html', miembros=miembros)

@bp_miembro.route("/create",methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('miembro/create.html')
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        miembro = Miembro(nombre=nombre,email=email)
        db.session.add(miembro)
        db.session.commit()
        return redirect(url_for('bp_miembro.index'))

@bp_miembro.route("/edit/<int:miembro_id>",methods=['GET','POST'])
def edit(miembro_id):
    miembro = Miembro.query.get_or_404(miembro_id)
    if request.method == 'GET':
        return render_template('miembro/edit.html', miembro=miembro)
    elif request.method == 'POST':
        miembro.nombre = request.form.get('nombre')
        miembro.email = request.form.get('email')
        db.session.commit()
        return redirect(url_for('bp_miembro.index'))

@bp_miembro.route("/delete/<int:miembro_id>",methods=['POST'])
def delete(miembro_id):
    miembro = Miembro.query.get_or_404(miembro_id)
    db.session.delete(miembro)
    db.session.commit()
    return redirect(url_for('bp_miembro.index'))

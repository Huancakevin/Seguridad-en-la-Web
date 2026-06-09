from flask import request, render_template, redirect, url_for, Blueprint
from flask_login import current_user
from blueprintapp.app import db
from blueprintapp.tareas.models import Tarea

bp_tarea = Blueprint('bp_tarea', __name__, template_folder='templates')

@bp_tarea.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('bp_auth.login'))

@bp_tarea.route("/")
def index():
    tareas = Tarea.query.all()
    return render_template('tareas/index.html', tareas=tareas)

@bp_tarea.route("/create",methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('tareas/create.html')
    elif request.method == 'POST':
        descripcion = request.form.get('descripcion')
        completado = True if 'completado' in request.form.keys() else False
        tarea = Tarea(descripcion=descripcion,completado=completado)
        db.session.add(tarea)
        db.session.commit()
        return redirect(url_for('bp_tarea.index'))

@bp_tarea.route("/edit/<int:tarea_id>",methods=['GET','POST'])
def edit(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    if request.method == 'GET':
        return render_template('tareas/edit.html', tarea=tarea)
    elif request.method == 'POST':
        tarea.descripcion = request.form.get('descripcion')
        tarea.completado = True if 'completado' in request.form.keys() else False
        db.session.commit()
        return redirect(url_for('bp_tarea.index'))

@bp_tarea.route("/delete/<int:tarea_id>",methods=['POST'])
def delete(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    db.session.delete(tarea)
    db.session.commit()
    return redirect(url_for('bp_tarea.index'))

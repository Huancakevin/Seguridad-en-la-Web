import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    os.makedirs(app.instance_path, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'bd_equipo.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['LOGIN_VIEW'] = 'bp_auth.login'
    app.config['LOGIN_MESSAGE_CATEGORY'] = 'warning'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from blueprintapp.auth.models import User
    from blueprintapp.auth.routes import bp_auth
    from blueprintapp.miembros.routes import bp_miembro
    from blueprintapp.core.routes import bp_core
    from blueprintapp.tareas.routes import bp_tarea

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'bp_auth.login'

    app.register_blueprint(bp_auth, url_prefix='')
    app.register_blueprint(bp_miembro, url_prefix='/miembros')
    app.register_blueprint(bp_core, url_prefix='/')
    app.register_blueprint(bp_tarea, url_prefix='/tareas')

    with app.app_context():
        db.create_all()

    return app
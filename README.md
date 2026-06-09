# Autenticación con Flask-Login

Este README documenta la implementación de autenticación en este proyecto, usando `Flask-Login` y `werkzeug.security`.

Resumen
-------

Se añadieron las funcionalidades básicas:
- Registro de usuario
- Inicio y cierre de sesión
- Protección de rutas (redirección a login si no está autenticado)

Instalación rápida
-------------------

Instala dependencias y ejecuta la aplicación:

```bash
pip install -r requirements.txt
python run.py
```

Rutas principales
------------------

- `GET /login`  — Formulario de inicio de sesión
- `POST /login` — Procesa inicio de sesión
- `GET /register` — Formulario de registro
- `POST /register` — Crea nuevo usuario
- `GET /logout` — Cierra la sesión actual

Archivos relevantes
-------------------

- `blueprintapp/auth/models.py` — Modelo `User` (hereda `UserMixin`) con `set_password()` y `check_password()`.
- `blueprintapp/auth/routes.py` — Lógica de `login`, `register`, `logout` y uso de `login_user`/`logout_user`.
- `blueprintapp/app.py` — Inicializa `LoginManager`, define `user_loader` y registra el blueprint de autenticación.
- `blueprintapp/templates/base.html` — Navbar y mensajes que muestran el estado de `current_user`.
- `blueprintapp/miembros/routes.py` y `blueprintapp/tareas/routes.py` — Requieren autenticación vía `before_request`.

Configuración importante
------------------------

- `SECRET_KEY` se define en `blueprintapp/app.py`. En entornos de producción exporta `SECRET_KEY` como variable de entorno.
- `LOGIN_VIEW` está configurado para redirigir a la ruta de login cuando sea necesario.

Crear un usuario (rápido)
-------------------------

Opción A — web:

1. Ejecuta la app: `python run.py`
2. Abre `http://localhost:5000/register` y crea la cuenta.

Opción B — shell Python:

```python
from blueprintapp.app import create_app, db
from blueprintapp.auth.models import User

app = create_app()
with app.app_context():
    u = User(username='admin', email='admin@example.com')
    u.set_password('tu_contraseña_segura')
    db.session.add(u)
    db.session.commit()
```

Verificaciones rápidas
----------------------

- Acceder a `/miembros` o `/tareas` sin iniciar sesión debe redirigir a `/login`.
- Después de iniciar sesión, la barra de navegación muestra el nombre de usuario y el botón `Cerrar sesión`.

siguiente paso
----------------------------------

- Nunca usar el `SECRET_KEY` por defecto en producción; configúralo mediante variable de entorno.
- Usar HTTPS y habilitar headers de seguridad (HSTS, CSP) en producción.
- Considerar: verificación por email, restablecimiento de contraseña, bloqueo por intentos fallidos y logging de accesos.

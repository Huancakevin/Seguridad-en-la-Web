# Flask-Login (Integración en este proyecto)

Este README describe únicamente la parte de autenticación implementada con Flask-Login.

## Resumen

Se añadió autenticación básica con inicio de sesión, registro y cierre de sesión. El sistema usa `Flask-Login` para manejar la sesión del usuario y `werkzeug.security` para hashear contraseñas.

## Archivos clave (implementación)

- [blueprintapp/auth/models.py](blueprintapp/auth/models.py) — Modelo `User` con `UserMixin`, `set_password()` y `check_password()`.
- [blueprintapp/auth/routes.py](blueprintapp/auth/routes.py) — Rutas `login`, `register`, `logout` usando `login_user`, `logout_user`, `current_user`, `login_required`.
- [blueprintapp/app.py](blueprintapp/app.py) — Inicialización de `LoginManager`, `load_user` y registro del blueprint `bp_auth`.
- [blueprintapp/templates/base.html](blueprintapp/templates/base.html) — Mostrar enlaces de `Iniciar sesión`/`Registrarse` y `Cerrar sesión`; muestra `current_user.username` cuando existe.
- [blueprintapp/miembros/routes.py](blueprintapp/miembros/routes.py) y [blueprintapp/tareas/routes.py](blueprintapp/tareas/routes.py) — Antes de cada petición requieren que `current_user.is_authenticated` (redirección al login si no lo está).

## Dependencias

Asegúrate de instalar `Flask-Login` (ya añadido a `requirements.txt`):

```
pip install -r requirements.txt
```

## Configuración relevante

- `SECRET_KEY` se configura en `blueprintapp/app.py`. En producción, exporta una variable de entorno `SECRET_KEY` segura.
- `LOGIN_VIEW` está configurado como `bp_auth.login` (ruta a la página de login).

## Cómo crear un usuario inicial (rápido)

1. Ejecuta la app (por ejemplo `python run.py`).
2. Ve a `/register` y crea una cuenta.

Alternativa (desde Flask shell):

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

## Comprobaciones rápidas

- Intentar acceder a `/miembros` o `/tareas` sin iniciar sesión debe redirigir a `/login`.
- Tras iniciar sesión, el navbar muestra el nombre de usuario y el enlace `Cerrar sesión`.

## Notas y próximos pasos sugeridos

- Para producción: usar HTTPS, cambiar `SECRET_KEY`, y considerar limitación de intentos de login.
- Si quieres, puedo añadir confirmación por email o restablecimiento de contraseña.

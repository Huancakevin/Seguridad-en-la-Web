
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

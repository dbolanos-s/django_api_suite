# django_api_suite — Backend Data Server

Backend construido con Django y Django Rest Framework que expone una API REST
para las operaciones CRUD sobre una colección almacenada en Firebase Realtime
Database, usando el Firebase Admin Python SDK como capa de acceso a datos.

## Aplicaciones

- **homepage**: sitio renderizado en el servidor (SSR) con plantillas y archivos estáticos.
- **demo_rest_api**: API REST de demostración con datos en memoria.
- **landing_api**: pasarela de comunicación con Firebase Realtime Database.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Página de inicio (SSR) |
| GET/POST | `/demo/rest/api/` | Colección en memoria |
| PUT/PATCH/DELETE | `/demo/rest/api/<id>/` | Elemento de la colección |
| GET/POST | `/landing/api/index/` | Colección en Firebase |
| GET/PUT/PATCH/DELETE | `/landing/api/index/<id>/` | Documento en Firebase |

## Configuración de PythonAnywhere

- Usuario: `dbolanos`
- GitHub: `dbolanos-s`
- Dominio: `https://dbolanos.pythonanywhere.com/`

## Ejecución local

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

Requiere `secrets/landing-key.json` con la clave privada del SDK de Firebase Admin.
El archivo no se versiona y debe cargarse manualmente en PythonAnywhere.
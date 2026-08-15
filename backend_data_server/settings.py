"""
Django settings for backend_data_server project.
"""

from pathlib import Path
import os

import firebase_admin
from firebase_admin import credentials

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-++0$(!7*s8lu9$o$oq_v$t(98e=xg&e5b^-*+lrg34x+nus=7w",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".github.dev",                     # Codespaces
    "<USUARIO-PYTHONANYWHERE>.pythonanywhere.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.github.dev",
    "https://<USUARIO-PYTHONANYWHERE>.pythonanywhere.com",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "firebase_admin",
    "rest_framework",
    "homepage",
    "demo_rest_api",
    "landing_api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend_data_server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend_data_server.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-ec"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = "assets/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Firebase Admin Python SDK -------------------------------------------
# Coloque la ruta relativa al archivo con la clave privada
FIREBASE_CREDENTIALS_PATH = credentials.Certificate("secrets/landing-key.json")

# Inicialice la conexión con el Realtime Database con la clave privada y la URL
if not firebase_admin._apps:
    firebase_admin.initialize_app(FIREBASE_CREDENTIALS_PATH, {
        "databaseURL": "https://landing-2de01-default-rtdb.firebaseio.com/"
    })
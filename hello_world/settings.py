"""
Django settings for hello_world project.
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = config("SECRET_KEY", default='django-insecure-sua-chave-secreta-aqui')
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_browser_reload",
    "app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "hello_world.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hello_world.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Modelo de Utilizador Personalizado
AUTH_USER_MODEL = 'app.Usuario'

# Redirecionamento de Login
LOGIN_URL = 'app:login'

# --- SOLUÇÃO DEFINITIVA PARA FICHEIROS ESTÁTICOS ---
# A URL para aceder aos ficheiros estáticos no navegador.
STATIC_URL = "static/"

# Esta é a correção mais importante. Diz ao Django para procurar
# uma pasta chamada 'static' diretamente dentro da sua pasta 'app'.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "app/static"),
]

# Esta linha é usada para deployment e pode ser mantida.
STATIC_ROOT = BASE_DIR / "staticfiles"
# --- FIM DA SOLUÇÃO ---

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
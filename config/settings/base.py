import os
from pathlib import Path
from datetime import timedelta
import environ

# 1) Tell django‐environ where your .env lives
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
# 2) Actually read the .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')
# pull in env vars or sensible defaults
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG')
HOST = env('HOST', default='https://savangel.com')
EMAIL_BACKEND = env('EMAIL_BACKEND')


print("⚙️  Loaded .env:", {
    "DEBUG": env.bool("DEBUG", default=None),
    "EMAIL_BACKEND": env("EMAIL_BACKEND", default=None),
    "HOST": env("HOST", default=None),
})

# Applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # your apps
    "accounts",

    # third-party
    "rest_framework",
    "drf_yasg",
    "rest_framework_simplejwt.token_blacklist",
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

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# Templates (DRF’s swagger needs request in context)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# Database (all env-driven)
DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.postgresql",
        "NAME":     env('DATABASE_NAME'),
        "USER":     env('DATABASE_USER'),
        "PASSWORD": env('DATABASE_PASSWORD'),
        "HOST":     env('DATABASE_HOST', default='127.0.0.1'),
        "PORT":     env('DATABASE_PORT', default='5432'),
    }
}

AUTH_USER_MODEL = 'accounts.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'public' / 'static'

# REST framework + JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
      'Bearer': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header',
        'description': 'JWT “Bearer <token>”',
      }
    },
    'USE_SESSION_AUTH': False,
}

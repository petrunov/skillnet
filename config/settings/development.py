from .base import *

# Development overrides
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Console email backend for dev
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@localhost'

# Enable CORS for your React frontend
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

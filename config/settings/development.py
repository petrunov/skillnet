from .base import *
# Console email backend for dev
# EMAIL_HOST           = env('EMAIL_HOST')
# EMAIL_PORT           = int(env('EMAIL_PORT'))
# EMAIL_HOST_USER      = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD  = env('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS        = env('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL   = env('DEFAULT_FROM_EMAIL')

# Enable CORS for your React frontend
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

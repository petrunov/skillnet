import os
from .base import *

# Production overrides
DEBUG = True
DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.mysql",
        "NAME":     env('DATABASE_NAME'),
        "USER":     env('DATABASE_USER'),
        "PASSWORD": '%$S$Qz-=+8bV&uDH',
        "HOST":     env('DATABASE_HOST', default='localhost'),
        "PORT":     env('DATABASE_PORT', default='3306'),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Use real SMTP settings in production
# EMAIL_BACKEND        = os.environ['EMAIL_BACKEND']
# EMAIL_HOST           = os.environ['EMAIL_HOST']
# EMAIL_PORT           = int(os.environ.get('EMAIL_PORT', 587))
# EMAIL_HOST_USER      = os.environ['EMAIL_HOST_USER']
# EMAIL_HOST_PASSWORD  = os.environ['EMAIL_HOST_PASSWORD']
# EMAIL_USE_TLS        = os.environ.get('EMAIL_USE_TLS') == 'True'
# DEFAULT_FROM_EMAIL   = os.environ['DEFAULT_FROM_EMAIL']

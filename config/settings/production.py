import os
from .base import *

# Production overrides
DEBUG = False
DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.mysql",
        "NAME":     env('DATABASE_NAME'),
        "USER":     env('DATABASE_USER'),
        "PASSWORD": env('DATABASE_PASSWORD'),
        "HOST":     env('DATABASE_HOST', default='localhost'),
        "PORT":     env('DATABASE_PORT', default='3306'),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Use real SMTP settings in production
EMAIL_HOST           = env('EMAIL_HOST')
EMAIL_PORT           = int(env('EMAIL_PORT'))
EMAIL_HOST_USER      = 'noreply@savangel.com' #env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD  = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS        = env.bool('EMAIL_USE_TLS')
EMAIL_USE_SSL        = env.bool('EMAIL_USE_SSL')
DEFAULT_FROM_EMAIL   = env('DEFAULT_FROM_EMAIL')

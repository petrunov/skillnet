import os, sys

# 1. Add your project root to sys.path
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 2. Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# 3. Get the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
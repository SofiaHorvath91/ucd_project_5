# ASGI config for ucd_project_5 project

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ucd_project_5.settings')

application = get_asgi_application()

import os
from django.core.wsgi import get_wsgi_application
from .routing import application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'universal_store.settings')

application = get_wsgi_application()

application = application
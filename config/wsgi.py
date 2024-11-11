import os

from django.core.wsgi import get_wsgi_application
print("WSGI is attempting to load settings module.")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

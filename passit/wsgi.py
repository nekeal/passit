"""
WSGI config for passit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""
import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

env_path = Path(".env")
load_dotenv(dotenv_path=env_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "passit.settings.local")

application = get_wsgi_application()

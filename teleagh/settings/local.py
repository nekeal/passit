from .base import *

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'teleagh'),
        'USER': os.environ.get('POSTGRES_USER', 'teleagh'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'teleagh'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
    }
}

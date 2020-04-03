import dj_database_url

from .base import *

ALLOWED_HOSTS = ['*']

INSTALLED_APPS.append('silk')
# INSTALLED_APPS.append('django_extensions')
MIDDLEWARE.insert(0, 'silk.middleware.SilkyMiddleware')
SILKY_PYTHON_PROFILER = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'teleagh2'),
        'USER': os.environ.get('POSTGRES_USER', 'teleagh'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'teleagh'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
    }
}
DATABASE_URL = os.environ.get('DATABASE_URL')
db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=False)
DATABASES['default'].update(db_from_env)

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'rest_framework_simplejwt.authentication.JWTAuthentication',
    'rest_framework.authentication.SessionAuthentication',
)

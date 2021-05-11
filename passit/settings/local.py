import dj_database_url

from .base import *

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS.append("silk")
MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")
SILKY_PYTHON_PROFILER = True

# ------------- DATABASES -------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "passit"),
        "USER": os.environ.get("POSTGRES_USER", "passit"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "passit"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
    }
}
DATABASE_URL = os.environ.get("DATABASE_URL")
db_from_env = dj_database_url.config(
    default=DATABASE_URL, conn_max_age=500, ssl_require=False
)
DATABASES["default"].update(db_from_env)

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
    "rest_framework_simplejwt.authentication.JWTAuthentication",
    "rest_framework.authentication.SessionAuthentication",
)

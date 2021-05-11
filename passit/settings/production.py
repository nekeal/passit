import dj_database_url
from dotenv import load_dotenv

from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

env_path = Path(".env")
load_dotenv(dotenv_path=env_path)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console_info": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        }
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console_info"],
        }
    },
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "postgres"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
    }
}
DATABASE_URL = os.environ.get("DATABASE_URL")
db_from_env = dj_database_url.config(
    default=DATABASE_URL, conn_max_age=500, ssl_require=True
)
DATABASES["default"].update(db_from_env)

STATIC_ROOT = os.path.join(BASE_DIR, "public")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

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
            "level": "ERROR",
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

# ------------- DATABASES -------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
    }
}
DATABASE_URL = os.getenv("DATABASE_URL")
db_from_env = dj_database_url.config(
    default=DATABASE_URL, conn_max_age=500, ssl_require=True
)
DATABASES["default"].update(db_from_env)

STATIC_ROOT = BASE_DIR.joinpath("public")
MEDIA_ROOT = BASE_DIR.joinpath("media")

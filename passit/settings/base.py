"""
Django settings for passit project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta

from pathlib import Path

BASE_DIR = Path(__file__).parents[2]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w-ipd5^0$3f(+e072x3=f*9h1dgqbw8d9a2ggc=l_f!#g3ubo0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'django_filters',
    'webpack_loader',
    'django_extensions',
    'django_celery_results',
    # my apps
    'passit.accounts.apps.AccountsConfig',
    'passit.lecturers.apps.LecturersConfig',
    'passit.subject.apps.SubjectConfig',
    'passit.news.apps.NewsConfig',
    'passit.events.apps.EventsConfig',
    'passit.syllabus',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'passit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'passit.wsgi.application'


JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "Passit Admin",
    # Title on the login screen
    "site_header": "Passit",
    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    "site_logo": "logo.png",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to passit",
    # Copyright on the footer
    # "copyright": "nekeal",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "accounts.CustomUser",
    # Field name on user model that contains avatar image
    "user_avatar": None,
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        # model admin to link to (Permissions checked against model)
        {"model": "accounts.CustomUser"},
        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "subject"},
    ],
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu
    "hide_apps": [],
    # Hide these models when generating side menu
    "hide_models": [],
    # List of apps to base side menu ordering off of
    "order_with_respect_to": ["accounts", "subject", "news"],
    # Custom links to append to app groups, keyed on app name
    "custom_links": {},
    # Custom icons per model in the side menu See https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/
    # for a list of icon classes
    "icons": {
        "auth.Group": "fas fa-users",
        "accounts.CustomUser": "fas fa-user",
        "accounts.UserProfile": "fas fa-user-graduate",
        "subject.Exam": "fas fa-edit",
        "subject.FieldOfStudy": "fas fa-university",
        "subject.FieldOfStudyOfAgeGroup": "fas fa-user-graduate",
        "subject.Subject": "fas fa-book-open",
        "subject.SubjectOfAgeGroup": "fas fa-calendar-week",
        "news.News": "fas fa-rss",
        "lecturers.Lecturer": "fas fa-chalkboard-teacher",
        "lecturers.LecturerOfSubjectOfAgeGroup": "fab fa-mandalorian",
        "shops.Salary": "fas fa-money-bill",
    },
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_LOCATION', "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "passit"
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'accounts.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'passit/frontend/build/static'),
    os.path.join(BASE_DIR, 'passit/frontend/src/assets'),
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# REST FRAMEWORK CONFIGURATION

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    )
}
# WEBPACK LOADER

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'passit/frontend/build/',
        'STATS_FILE': os.path.join(BASE_DIR, 'passit/frontend/config/webpack-stats.json'),
    }
}

# DJOSER

DJOSER = {
    'SERIALIZERS': {
        'current_user': 'passit.accounts.serializers.CustomUserSerializer'
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
}

# CELERY

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", 'redis://localhost:6379/2')
CELERY_RESULT_BACKEND = 'django-db'
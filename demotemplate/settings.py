"""
Django settings for demotemplate project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url
from env_tools import apply_env
from requests_respectful import RespectfulRequester

apply_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'yoursecretkeyhere')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.getenv('DEBUG', '').lower() == 'false' else True

REMOTE = True if os.getenv('REMOTE', '').lower() == 'true' else False

ALLOWED_HOSTS = ['*']

HEROKUCONFIG_APP_NAME = os.getenv('HEROKUCONFIG_APP_NAME', '')

DEFAULT_BASE_URL = ('https://{}.herokuapp.com'.format(HEROKUCONFIG_APP_NAME) if
                    REMOTE else 'http://127.0.0.1:5000')

OPENHUMANS_APP_BASE_URL = os.getenv('APP_BASE_URL', DEFAULT_BASE_URL)
if OPENHUMANS_APP_BASE_URL[-1] == "/":
    OPENHUMANS_APP_BASE_URL = OPENHUMANS_APP_BASE_URL[:-1]

# Open Humans configuration
OPENHUMANS_CLIENT_ID = os.getenv('OH_CLIENT_ID')
OPENHUMANS_CLIENT_SECRET = os.getenv('OH_CLIENT_SECRET')
OH_ACTIVITY_PAGE = os.getenv('OH_ACTIVITY_PAGE')
OPENHUMANS_OH_BASE_URL = 'https://www.openhumans.org'

OH_API_BASE = OPENHUMANS_OH_BASE_URL + '/api/direct-sharing'
OH_DIRECT_UPLOAD = OH_API_BASE + '/project/files/upload/direct/'
OH_DIRECT_UPLOAD_COMPLETE = OH_API_BASE + '/project/files/upload/complete/'
OH_DELETE_FILES = OH_API_BASE + '/project/files/delete/'

MOVES_CLIENT_ID = os.getenv('MOVES_CLIENT_ID')
MOVES_CLIENT_SECRET = os.getenv('MOVES_CLIENT_SECRET')
MOVES_REDIRECT_URI = os.getenv('MOVES_REDIRECT_URI')

# Requests Respectful (rate limiting, waiting)
if REMOTE is True:
    from urllib.parse import urlparse
    url_object = urlparse(os.getenv('REDIS_URL', 'redis://'))
    RespectfulRequester.configure(
        redis={
            "host": url_object.hostname,
            "port": url_object.port,
            "password": url_object.password,
            "database": 0
        },
        safety_threshold=5)

# This creates a Realm called "source" that allows 60 requests per minute maximum.
rr = RespectfulRequester()
rr.register_realm("moves", max_requests=60, timespan=60)

# Applications installed
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps. Update these if you add or change app names!
    'datauploader.apps.DatauploaderConfig',
    'open_humans.apps.OpenHumansConfig',
    'main.apps.MainConfig'
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

MIDDLEWARE_CLASSES = [
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'demotemplate.urls'

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

WSGI_APPLICATION = 'demotemplate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# https://devcenter.heroku.com/articles/django-app-configuration


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]

# Configure logging to print Django logs to the console.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

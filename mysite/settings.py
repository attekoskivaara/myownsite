"""
Django settings for mysite project.
Generated by 'django-admin startproject' using Django 2.1.7.
For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from decouple import config
import boto3
from botocore.exceptions import ClientError
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from pathlib import Path
import os
import subprocess
import ast


def get_environ_vars():
    completed_process = subprocess.run(
        ['/opt/elasticbeanstalk/bin/get-config', 'environment'],
        stdout=subprocess.PIPE,
        text=True,
        check=True
    )

    return ast.literal_eval(completed_process.stdout)

def get_secret():

    secret_name = "SECRET_KEY"
    region_name = "eu-north-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Your code goes here.


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

PLOTLY_DASH = {

    # Route used for the message pipe websocket connection
    "ws_routcde" :   "dpd/ws/channel",

    # Route used for direct http insertion of pipe messages
    "http_route" : "dpd/views",

    # Flag controlling existince of http poke endpoint
    "http_poke_enabled" : True,

    # Insert data for the demo when migrating
    "insert_demo_migrations" : False,

    # Timeout for caching of initial arguments in seconds
    "cache_timeout_initial_arguments": 60,

    # Name of view wrapping function
    "view_decorator": None,

    # Flag to control location of initial argument storage
    "cache_arguments": True,

    # Flag controlling local serving of assets
    "serve_locally": False,
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = get_secret()


# SECURITY WARNING: don't run with debug turned on in production!

if 'PRODUCTION' in os.environ:
    SECRET_KEY = config('SECRET_KEY')
    DEBUG = False
else:
    DEBUG = True
    SECRET_KEY = config('SECRET_KEY')


ALLOWED_HOSTS = ['*']

# SECURE_CONTENT_TYPE_NOSNIFF = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# SECURE_SSL_REDIRECT = True

# SESSION_COOKIE_SECURE = True

# CSRF_COOKIE_SECURE = True

# SECURE_HSTS_PRELOAD = True

# SECURE_HSTS_SECONDS = 60
# SECURE_HSTS_SECONDS = 31536000 # --vuosi sekunteina--
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'taggit',
    'blog',
    'crispy_forms',
    'django_summernote',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'channels',
    'channels_redis',
]

INSTALLED_APPS += ( 'django.contrib.sitemaps',)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
#    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',
    'django_plotly_dash.middleware.ExternalRedirectionMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config('RDS_DB_NAME'),
            'USER': config('RDS_USERNAME'),
            'PASSWORD': config('RDS_PASSWORD'),
            'HOST': config('RDS_HOSTNAME'),
            'PORT': config('RDS_PORT'),
#            'PORT': config('DB_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/



# Location of static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]

STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")

STATIC_URL = '/static/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

ASGI_APPLICATION = 'mysite.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379), ],
        }
    }
}

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    'django_plotly_dash.finders.DashAppDirectoryFinder',
]

PLOTLY_COMPONENTS = [

    'dash_core_components',
    'dash_html_components',
    'dash_renderer',
    'dpd_components',
    'dpd_static_support',

#   'dash_bootstrap_components'
]
X_FRAME_OPTIONS = 'SAMEORIGIN'
# X_FRAME_OPTIONS = 'DENY'

# Media paths

# Base url to serve media files
MEDIA_URL = '/media/'

# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media/')
import os
import sys

from constants import LOCAL_ENV
from .base import BaseSettings


class ENV_VARS:
    DJANGO_SETTINGS_MODULE = os.environ['DJANGO_SETTINGS_MODULE']

    SECRET_KEY = os.environ['SECRET_KEY']
    ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS']

    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_NAME = os.environ['DB_NAME']


class LocalSettings(BaseSettings):
    ENV_NAME = LOCAL_ENV
    SECRET_KEY = 'SECRET_KEY'

    DEBUG = True

    ALLOWED_HOSTS = ['*']

    DATABASES = {
        'default': {
            'ENGINE': 'dj_db_conn_pool.backends.mysql',
            'NAME': ENV_VARS.DB_NAME,
            'USER': ENV_VARS.DB_USER,
            'PASSWORD': ENV_VARS.DB_PASSWORD,
            'HOST': ENV_VARS.DB_HOST,
            'PORT': ENV_VARS.DB_PORT,
            'CONN_MAX_AGE': 0,
            'POOL_OPTIONS': {
                'pool_size': 20,
                'max_overflow': 10
            }
        }
    }

    if 'test' in sys.argv:
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'testing_db'
        }


LocalSettings.load_settings(__name__)

from constants import LOCAL_ENV
from .base import BaseSettings


class LocalSettings(BaseSettings):
    ENV_NAME = LOCAL_ENV
    SECRET_KEY = 'SECRET_KEY'

    DEBUG = True

    ALLOWED_HOSTS = ['*']

    DATABASES = {
        'default': {
            'ENGINE': 'dj_db_conn_pool.backends.mysql',
            'NAME': 'trakkit_db',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '3306',
            'CONN_MAX_AGE': 0,
            'POOL_OPTIONS': {
                'pool_size': 20,
                'max_overflow': 10
            }
        }
    }


LocalSettings.load_settings(__name__)

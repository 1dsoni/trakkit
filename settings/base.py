"""Class based settings for complex settings inheritance."""

import inspect
import sys
from pathlib import Path

from pythonjsonlogger.jsonlogger import JsonFormatter


class BaseSettings(object):
    """
    Class-based settings wrapper.
    Do not use directly.
    Define settings separately for production, staging, local env
    """

    @classmethod
    def load_settings(cls, module_name):
        """
        Export class variables and properties to module namespace.
        This will export and class variable that is all upper case and doesn't
        begin with ``_``. These members will be set as attributes on the module
        ``module_name``.
        """
        self = cls()
        module = sys.modules[module_name]
        for (member, value) in inspect.getmembers(self):
            if member.isupper() and not member.startswith('_'):
                if isinstance(value, property):
                    value = value.fget(self)
                setattr(module, member, value)

    # production, staging, local; set it into the respective settings file
    @property
    def ENV_NAME(self):
        raise NotImplementedError('ENV_NAME not defined')

    @property
    def SECRET_KEY(self):
        # SECURITY WARNING: keep the secret key used in production secret!
        raise NotImplementedError('SECRET_KEY not defined')

    @property
    def DEBUG(self):
        raise NotImplementedError('DEBUG not defined')

    @property
    def ALLOWED_HOSTS(self):
        raise NotImplementedError('ALLOWED_HOSTS not defined')

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    INSTALLED_APPS = [
        'apps.trade.apps.TradeConfig',
    ]

    MIDDLEWARE = [
        'commons.middlewares.LogTraceIdMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'apps.urls'

    WSGI_APPLICATION = 'wsgi.application'

    # Internationalization
    # https://docs.djangoproject.com/en/3.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/

    STATIC_ROOT = Path.joinpath(BASE_DIR, 'static')
    STATIC_URL = '/static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        )
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': JsonFormatter,
                'format': '%(asctime)%(levelname)%(processName)%(threadName)%(name)%(lineno)%(request_trace_id)%(message)'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'json',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        }
    }

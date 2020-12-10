import os

import environ

env = environ.Env()
root_path = environ.Path(__file__) - 2


# -----------------------------------------------------------------------------
# Basic Config
# -----------------------------------------------------------------------------
ENV = env('ENV', default='prod')
assert ENV in ['dev', 'test', 'prod', 'qa']
DEBUG = env.bool('DEBUG', default=False)
BASE_DIR = root_path()
ROOT_URLCONF = 'conf.urls'
WSGI_APPLICATION = 'conf.wsgi.application'

# -----------------------------------------------------------------------------
# Time & Language
# -----------------------------------------------------------------------------
LANGUAGE_CODE = env('LANGUAGE_CODE', default='en-us')
TIME_ZONE = env('TIMEZONE', default='UTC')
USE_I18N = env('USE_I18N', default=True)
USE_L10N = env('USE_L10N', default=True)
USE_TZ = env('USE_TZ', default=True)

# -----------------------------------------------------------------------------
# Emails
# -----------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='')
EMAIL_BACKEND = env(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.smtp.EmailBackend')

# -----------------------------------------------------------------------------
# Security and Users
# -----------------------------------------------------------------------------
SECRET_KEY = env('SECRET_KEY', default='bvta)#d1zny^e7fi+aezp2u(9+**y)r_*)=+brcyihhiy(gek_')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
#AUTH_USER_MODEL = 'users.User'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = env('LOGIN_URL', default='/login/')
LOGIN_REDIRECT_URL = env('LOGIN_REDIRECT_URL', default='/')
ACCOUNT_ACTIVATION_DAYS = env.int('ACCOUNT_ACTIVATION_DAYS', default=7)
REGISTRATION_OPEN = env.bool('REGISTRATION_OPEN', default=True)
REGISTRATION_AUTO_LOGIN = env.bool('REGISTRATION_AUTO_LOGIN', default=True)

# -----------------------------------------------------------------------------
# Databases
# -----------------------------------------------------------------------------
DJANGO_DATABASE_URL = env.db('DATABASE_URL')
DATABASES = {'default': DJANGO_DATABASE_URL}

# -----------------------------------------------------------------------------
# Applications configuration
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    # First party
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party

    # Local
    'apps.misc',
]

if ENV == 'dev':
    INSTALLED_APPS += [
        'django_extensions',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root_path('templates')
        ],
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

# -----------------------------------------------------------------------------
# Celery
# -----------------------------------------------------------------------------
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://cache')
CELERY_TASK_ALWAYS_EAGER = env('CELERY_TASK_ALWAYS_EAGER', default=False)

# -----------------------------------------------------------------------------
# Static & Media Files
# -----------------------------------------------------------------------------
STATIC_URL = env('STATIC_URL', default='/static/')
STATIC_ROOT = root_path('static')

MEDIA_URL = env('MEDIA_URL', default='/media/')
MEDIA_ROOT = env('MEDIA_ROOT', default=root_path('media'))
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
LOGS_ROOT = env('LOGS_ROOT', default=root_path('logs'))
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_format': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file_format': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_format'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_ROOT, 'django.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'file_format',
        },
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'apps': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False,
        }

    }
}

USE_SENTRY = env.bool('USE_SENTRY', default=False)

if USE_SENTRY:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        environment=ENV
    )

from pathlib import Path
import os

from django.utils.translation import ugettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = 'django-insecure-+a((73_0@@hk6yic)s_xhup75k)w6x825!c3m!ok7-sz+wvcx!'


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_cleanup.apps.CleanupConfig',
    'mathfilters',
    'django_inlinecss'
]

OWN_APPS = [
    'internships'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + OWN_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath('templates')
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


WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'heisemployers',
        'USER': 'suadminuser',
        'PASSWORD': '34jfp4!ktgm$fcV',
        'HOST': 'localhost',
        'PORT': 5432
    }
}


AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


LANGUAGE_CODE = 'en-us'

LOCALE_PATHS = (
    BASE_DIR.joinpath('locale'),
)


DATE_FORMAT = 'd/m/Y'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR.joinpath('static_base')
]

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR.joinpath('media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = '/login'

LOGIN_REDIRECT_URL = '/'


EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.yandex.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'noreply@work4practice.com'

EMAIL_HOST_PASSWORD = 'hWfZxisynhYubGG4Su'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

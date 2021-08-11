from django.utils.translation import ugettext_lazy as _

from config.settings.base import *


SITE_ID = 1

ROOT_URLCONF = 'config.urls_main'


LANGUAGES = (
    ('en-us', _('English')),
    ('ru', _('Russia')),
)

DEFAULT_LANGUAGE = 1

LANGUAGE_CODE = 'en-us' 


STATICFILES_DIRS += [
    BASE_DIR.joinpath('static_main')
]

STATIC_ROOT = BASE_DIR.joinpath('static_main_prod')

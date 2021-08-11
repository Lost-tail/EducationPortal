from django.utils.translation import ugettext_lazy as _

from config.settings.base import *


SITE_ID = 2

ROOT_URLCONF = 'config.urls_admin'

LANGUAGES = (
    ('en-us', _('English')),
)

STATICFILES_DIRS += [
    BASE_DIR.joinpath('static_admin'),
]

STATIC_ROOT = BASE_DIR.joinpath('static_admin_prod')

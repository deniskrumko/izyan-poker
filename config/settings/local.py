import dj_database_url

from .common import *  # noqa

SECRET_KEY = 'example'

DEBUG = True

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://postgres:@localhost:5432/izyan'
    )
}

AUTH_PASSWORD_VALIDATORS = []

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Shell plus pre imports
SHELL_PLUS_PRE_IMPORTS = [('{}.factories'.format(app), '*')
                          for app in INSTALLED_APPS]  # noqa

WEBSITE_URL = 'http://127.0.0.1:8000/'

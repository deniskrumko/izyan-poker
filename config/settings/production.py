import dj_database_url
from decouple import config

from .common import *  # noqa

DEBUG = False

SECRET_KEY = config('DJANGO_SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

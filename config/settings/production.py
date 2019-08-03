import dj_database_url
from decouple import config

from .common import *  # noqa

SECRET_KEY = config('DJANGO_SECRET_KEY')

DEBUG = False

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

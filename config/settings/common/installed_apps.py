INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
]

LOCAL_APPS = [
    'apps.poker',
    'apps.users',
]

INSTALLED_APPS += LOCAL_APPS

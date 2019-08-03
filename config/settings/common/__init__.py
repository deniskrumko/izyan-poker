from .auth import *  # noqa
from .installed_apps import *  # noqa
from .locales import *  # noqa
from .logging import *  # noqa
from .middleware import *  # noqa
from .paths import *  # noqa
from .static import *  # noqa
from .templates import *  # noqa

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ALLOWED_HOSTS = ['*']

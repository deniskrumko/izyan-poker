from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    """Configuration for ``Users`` app."""

    name = 'apps.users'
    verbose_name = _('Users')

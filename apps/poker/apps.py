from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PokerConfig(AppConfig):
    """Configuration for ``Poker`` app."""

    name = 'apps.poker'
    verbose_name = _('Poker')

    def ready(self):
        """Ready app."""
        from . import signals  # noqa

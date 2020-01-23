from core.views import BaseView

from ..models import (
    PokerRoom,
    PokerRound,
)


class IndexView(BaseView):
    """View for index page."""

    template_name = 'index.html'

    def get_context_data(self):
        """Get context data."""
        return {
            'available_rooms': PokerRoom.objects.filter(
                members__user=self.user
            ),
            'cards': PokerRound.CARDS,
        }

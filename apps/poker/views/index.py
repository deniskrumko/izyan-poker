from ..models import (
    PokerRoom,
    PokerRound,
)
from .base import BaseView


class IndexView(BaseView):
    """View for index page."""

    template_name = 'index.html'

    def get(self, request):
        """Get index view."""
        self.create_session()
        return super().get(request)

    def get_context_data(self):
        """Get context data."""
        return {
            'available_rooms': PokerRoom.objects.filter(
                members__session=self.session_key
            ),
            'cards': PokerRound.CARDS,
        }

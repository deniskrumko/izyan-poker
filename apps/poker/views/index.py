from core.views import BaseView

from ..models import PokerRoom, PokerRound


class IndexView(BaseView):
    """View for index page."""

    template_name = 'index.html'

    def get_context_data(self):
        """Get context data."""
        room_ids = self.user.members.filter(
            is_active=True
        ).values_list('room_id', flat=True) if self.user else ()
        return {
            'available_rooms': PokerRoom.objects.filter(id__in=room_ids),
            'cards': PokerRound.CARDS,
        }

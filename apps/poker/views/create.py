from ..models import (
    PokerMemberRecentRoom,
    PokerRoom,
)
from .base import BaseView


class CreateRoomView(BaseView):
    """View for creating new room."""

    template_name = 'create.html'

    def post(self, request):
        """Create new room."""
        name = request.POST.get('name')
        room = PokerRoom.objects.create(name=name)
        if self.session_key:
            PokerMemberRecentRoom.objects.get_or_create(
                room=room,
                session=self.session_key,
            )
        return self.redirect('poker:room', args=(room.token,))

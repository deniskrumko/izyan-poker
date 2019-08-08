from ..models import (
    PokerMember,
    PokerRoom,
)
from .base import BaseView


class SettingsView(BaseView):

    template_name = 'settings.html'

    def post(self, request, token):
        room_name = request.POST.get('room_name')
        member_name = request.POST.get('member_name')
        if room_name:
            self.room.name = room_name
            self.room.save()

        if member_name:
            self.member.name = member_name
            self.member.save()

        return self.redirect('poker:settings', args=(token,))

    def get_context_data(self, *args, **kwargs):
        """Get context data."""
        return {
            'room': self.room,
            'member': self.member,
        }

    def dispatch(self, *args, **kwargs):
        """Dispatch request."""
        self.room = self.get_object_or_404(PokerRoom, token=kwargs['token'])
        self.poker_round = self.room.get_poker_round()
        self.member = PokerMember.objects.filter(
            room=self.room,
            session=self.session_key,
        ).first() if self.session_key else None
        return super().dispatch(*args, **kwargs)

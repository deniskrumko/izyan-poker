from core.views import (
    BaseView,
    LoginRequiredMixin,
)

from ..models import (
    PokerMember,
    PokerRoom,
)


class SettingsView(LoginRequiredMixin, BaseView):

    template_name = 'settings.html'

    def get(self, request, token):
        """Handle GET request."""
        if not self.member:
            return self.redirect('poker:room', args=(token,))

        return super().get(request, token)

    def post(self, request, token):
        """Handle POST request."""
        # Exit room
        if '_exit' in request.POST:
            self.member.is_active = False
            self.member.save()
            return self.redirect('poker:index')

        room_name = request.POST.get('room_name')
        member_name = request.POST.get('member_name')
        use_time = request.POST.get('use_time')

        self.room.name = room_name
        self.room.use_time = bool(int(use_time))
        self.member.name = member_name

        self.room.save()
        self.member.save()

        return self.redirect('poker:room', args=(token,))

    def get_context_data(self, *args, **kwargs):
        """Get context data."""
        return {
            'room': self.room,
            'member': self.member,
        }

    def dispatch(self, *args, **kwargs):
        """Dispatch request."""
        self.user = (
            self.request.user if self.request.user.is_authenticated else None
        )
        self.room = self.get_object_or_404(PokerRoom, token=kwargs['token'])
        self.poker_round = self.room.get_poker_round()
        self.member = PokerMember.objects.filter(
            room=self.room,
            user=self.user,
            is_active=True,
        ).first()
        return super().dispatch(*args, **kwargs)

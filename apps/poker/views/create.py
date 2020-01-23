from core.views import (
    BaseView,
    LoginRequiredMixin,
)

from ..models import PokerRoom


class CreateRoomView(LoginRequiredMixin, BaseView):
    """View for creating new room."""

    template_name = 'create.html'

    def post(self, request):
        """Create new room."""
        name = request.POST.get('name')
        room = PokerRoom.objects.create(name=name)
        return self.redirect('poker:room', args=(room.token,))

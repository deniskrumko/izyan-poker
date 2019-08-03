from ..models import (
    PokerMember,
    PokerRoom,
)
from .base import BaseView


class MemberView(BaseView):
    """View for editing member data."""

    template_name = 'member.html'

    def get(self, request, token):
        self.create_session()
        context = self.get_context_data()
        context['token'] = token
        return self.render_to_response(context)

    def post(self, request, token):
        name = request.POST.get('name')
        room = self.get_object_or_404(PokerRoom, token=token)
        PokerMember.objects.get_or_create(
            room=room,
            name=name,
            session=self.session_key,
        )
        return self.redirect('poker:room', args=(token,))

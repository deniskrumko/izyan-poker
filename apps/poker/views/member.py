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
        room = self.get_object_or_404(PokerRoom, token=token)
        member = PokerMember.objects.filter(
            room=room,
            session=self.session_key,
        ).first()
        context = {
            'member_name': member.name if member else '',
            'room': room,
            'token': token,
        }
        return self.render_to_response(context)

    def post(self, request, token):
        name = request.POST.get('name')
        room = self.get_object_or_404(PokerRoom, token=token)
        PokerMember.objects.update_or_create(
            room=room,
            session=self.session_key,
            defaults={'name': name},
        )
        return self.redirect('poker:room', args=(token,))

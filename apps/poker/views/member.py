from core.views import BaseView, LoginRequiredMixin

from ..models import PokerMember, PokerRoom


class MemberView(LoginRequiredMixin, BaseView):
    """View for editing member data."""

    template_name = 'member.html'

    def get(self, request, token):
        room = self.get_object_or_404(PokerRoom, token=token)
        member = PokerMember.objects.filter(
            room=room,
            user=self.user,
            is_active=True,
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
            user=self.user,
            defaults={
                'name': name,
                'is_active': True,
            },
        )
        return self.redirect('poker:room', args=(token,))

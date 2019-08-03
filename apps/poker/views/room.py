from ..models import (
    PokerMember,
    PokerMemberVote,
    PokerRoom,
    PokerRound,
)
from .base import BaseView


class RoomView(BaseView):

    template_name = 'room.html'

    def get(self, request, token):
        if not self.member:
            return self.redirect('poker:member', args=(token,))

        return super().get(request, token)

    def post(self, request, token):
        vote = request.POST.get('vote')
        new_voting = request.POST.get('new')
        end_voting = request.POST.get('end')
        name = request.POST.get('name')
        save = request.POST.get('save')

        for key in request.POST.keys():
            if key.startswith('delete_'):
                member_id = key.replace('delete_', '')
                PokerMember.objects.filter(id=member_id).delete()

        if vote and not self.member.has_voted(self.poker_round):
            PokerMemberVote.objects.create(
                poker_round=self.poker_round,
                member=self.member,
                value=int(vote),
            )

        if new_voting and self.poker_round.completed:
            self.poker_round = PokerRound.objects.create(room=self.room)

        if end_voting and not self.poker_round.completed:
            self.poker_round.completed = True
            self.poker_round.save()

        if name and save and self.poker_round.name != name:
            self.poker_round.name = name
            self.poker_round.save()

        return self.redirect('poker:room', args=(token,))

    def get_context_data(self):
        """Get context data."""
        return {
            'room': self.room,
            'member': self.member,
            'poker_round': self.poker_round,
            'voted': self.member.has_voted(self.poker_round),
            'cards': [
                ('изян', 1),
                ('изи', 2),
                ('просто', 4),
                ('вроде просто', 6),
                ('норм', 8),
                ('норм так', 12),
                ('хз', 16),
                ('хз как-то', 20),
                ('как-то сложно', 24),
                ('сложно', 30),
                ('очень сложно', 40),
                ('бля', 48),
                ('пиздец', 60),
                ('пиздец какой-то', 80),
                ('вроде изян', 100),
            ]
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

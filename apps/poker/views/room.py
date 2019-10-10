from ..models import (
    PokerMember,
    PokerMemberRecentRoom,
    PokerMemberVote,
    PokerRoom,
    PokerRound,
)
from .base import BaseView


class RoomView(BaseView):
    """View for single poker room."""

    template_name = 'room.html'

    def get(self, request, token):
        """Handle GET request."""
        if not self.member:
            return self.redirect('poker:member', args=(token,))

        return super().get(request, token)

    def post(self, request, token):
        """Handle POST request."""
        vote = request.POST.get('vote')
        new_voting = request.POST.get('new')
        end_voting = request.POST.get('end')
        name = request.POST.get('name')
        save = request.POST.get('save')
        delete = request.POST.get('delete')
        revote = request.POST.get('revote')

        if delete:
            # Delete member
            PokerMember.objects.filter(id=delete).delete()
            if self.session_key:
                PokerMemberRecentRoom.objects.get_or_create(
                    room=self.room,
                    session=self.session_key,
                )

        if revote:
            # Re-vote
            PokerMemberVote.objects.filter(
                poker_round=self.poker_round,
                member=self.member,
            ).delete()

        if vote and self.member and not self.member.has_voted(
            self.poker_round
        ):
            # Count vote
            PokerMemberVote.objects.create(
                poker_round=self.poker_round,
                member=self.member,
                value=int(vote),
            )

        if new_voting and self.poker_round.completed:
            # Start new voting
            self.poker_round = PokerRound.objects.create(room=self.room)

        if end_voting and not self.poker_round.completed:
            # End current voting
            self.poker_round.completed = True
            self.poker_round.save()

        if name and save and self.poker_round.name != name:
            # Change poker round name
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
            'cards': self.poker_round.cards,
            'last_one': self.member.is_last_one(self.poker_round),
        }

    def dispatch(self, *args, **kwargs):
        """Dispatch request."""
        token = kwargs['token']
        self.room = self.get_object_or_404(PokerRoom, token=token)
        self.poker_round = self.room.get_poker_round()
        self.member = PokerMember.objects.filter(
            room=self.room,
            session=self.session_key,
        ).first() if self.session_key else None
        return super().dispatch(*args, **kwargs)

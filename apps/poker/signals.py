from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import PokerMember, PokerMemberVote, PokerRound


@receiver((post_save, post_delete), sender=PokerMember)
@receiver((post_save, post_delete), sender=PokerMemberVote)
@receiver(post_save, sender=PokerRound)
def update_poker_room(instance, *args, **kwargs):
    """Update poker room `updated` value."""
    sender = kwargs['sender']

    if sender == PokerMemberVote:
        instance.poker_round.room.save()
    if sender in (PokerRound, PokerMember):
        instance.room.save()


@receiver(post_delete, sender=PokerMember)
@receiver(post_save, sender=PokerMemberVote)
def complete_poker_round_signal(instance, *args, **kwargs):
    """Complete poker round on last vote."""
    sender = kwargs['sender']

    if sender == PokerMemberVote:
        poker_round = instance.poker_round
    elif sender == PokerMember:
        poker_round = instance.room.get_poker_round()

    if poker_round.all_voted and not poker_round.completed:
        poker_round.completed = True
        poker_round.save()

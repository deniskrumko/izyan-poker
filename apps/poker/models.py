from secrets import token_urlsafe

from django.db import models
from django.utils.translation import ugettext_lazy as _


def generate_room_token(nbytes=20):
    """Generate unique token for room."""
    return token_urlsafe(nbytes)


class PokerRoom(models.Model):
    """Model for poker room."""

    name = models.CharField(
        blank=False,
        max_length=255,
        verbose_name=_('Name'),
    )
    token = models.CharField(
        blank=False,
        default=generate_room_token,
        max_length=127,
        unique=True,
        verbose_name=_('Token'),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created'),
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        ordering = ('created',)

    @property
    def status(self):
        """Get room status.

        Used for auto refreshing pages.

        """
        return f'last_updated_{self.updated.timestamp()}'

    def get_poker_round(self):
        """Get or create latest poker round."""
        return (
            PokerRound.objects.filter(room=self).last()
            or PokerRound.objects.create(room=self)
        )


class PokerRound(models.Model):
    """Model for vote rounds in room."""

    room = models.ForeignKey(
        PokerRoom,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name='rounds',
        verbose_name=_('Room'),
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('name'),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created'),
    )
    completed = models.BooleanField(
        default=False,
        verbose_name=_('Completed'),
    )

    def __str__(self):
        return f'{self.id} {self.created}'

    class Meta:
        verbose_name = _('Round')
        verbose_name_plural = _('Rounds')
        ordering = ('created',)

    @property
    def result_score(self) -> int:
        """Get result score."""
        votes = self.votes.values_list('value', flat=True)
        if not votes or not self.completed:
            return 0

        return (sum(votes) / len(votes)) if votes else 0

    @property
    def all_voted(self) -> bool:
        """Return True if all members have voted."""
        return all(m.has_voted(self) for m in self.room.members.all())

    @property
    def member_votes(self) -> list:
        """Get list of member votes."""
        return [
            (member, self.votes.filter(member=member).first())
            for member in self.room.members.all()
        ]


class PokerMember(models.Model):
    """Model for poker members."""

    room = models.ForeignKey(
        PokerRoom,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name=_('Room'),
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        verbose_name=_('Name'),
    )
    session = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        verbose_name=_('Session'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')
        unique_together = ('room', 'session')
        ordering = ('name',)

    def has_voted(self, poker_round):
        """Return True if member voted in specified round."""
        return self.votes.filter(poker_round=poker_round).exists()


class PokerMemberVote(models.Model):
    """Model for vote of a single poker member."""

    poker_round = models.ForeignKey(
        PokerRound,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name=_('Poker round'),
    )
    member = models.ForeignKey(
        PokerMember,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name=_('Member'),
    )
    value = models.IntegerField(
        null=True,
        blank=False,
        default=0,
        verbose_name=_('Value'),
    )

    def __str__(self):
        return f'Member "{self.member}" voted "{self.value}"'

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
        ordering = ('member',)

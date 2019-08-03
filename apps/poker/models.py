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
    last_entry = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last entry time'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        ordering = ('-created',)


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
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created'),
    )
    completed = models.BooleanField(
        default=False,
        verbose_name=_('Completed'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Round')
        verbose_name_plural = _('Rounds')
        ordering = ('-created',)


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
        verbose_name=_('name'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')
        ordering = ('name',)
        unique_together = ('name', 'room')


class PockerMemberVote(models.Model):
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
        return f'{self.member}: {self.value}'

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
        ordering = ('member',)

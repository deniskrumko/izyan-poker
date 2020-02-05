from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import (
    Count,
    Sum,
)
from django.utils.translation import ugettext_lazy as _

from apps.poker.models import PokerMemberVote


class User(AbstractUser):
    """Model for app user."""

    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True
    )

    def __str__(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'.strip()

        return self.email

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('email',)

    @property
    def full_name(self):
        """Get full name of user."""
        return f'{self.first_name} {self.last_name}'

    @property
    def total_votes(self):
        """Get total votes count."""
        try:
            return PokerMemberVote.objects.filter(member__user=self).count()
        except Exception:
            return '?'

    @property
    def total_voted_values(self):
        """Get sum of all votes."""
        try:
            return PokerMemberVote.objects.filter(
                member__user=self
            ).aggregate(sum_votes=Sum('value'))['sum_votes']
        except Exception:
            return '?'

    @property
    def favourite_vote(self):
        """Get value (and count) of favourite vote."""
        try:
            votes_count = PokerMemberVote.objects.filter(
                member__user=self
            ).values('value').annotate(count=Count('value'))
            return max(votes_count, key=lambda y: y['count'])
        except Exception:
            return {
                'value': '?',
                'count': '?',
            }

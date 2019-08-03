from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """Model for app user."""

    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('email',)

    @property
    def full_name(self):
        """Get full name of user."""
        return f'{self.first_name} {self.last_name}'

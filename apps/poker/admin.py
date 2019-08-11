from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


class PokerMemberInline(admin.TabularInline):
    """Inline class for ``PokerMember`` model."""

    readonly_fields = ('session',)
    model = models.PokerMember
    extra = 0


class PokerRoundInline(admin.TabularInline):
    """Inline class for ``PokerRound`` model."""
    fields = (
        'completed',
        'name',
        'score',
        'all_voted',
    )
    show_change_link = True
    readonly_fields = fields
    model = models.PokerRound
    extra = 0


class PokerMemberVoteInline(admin.TabularInline):
    """Inline class for ``PokerMemberVote`` model."""

    autocomplete_fields = (
        'member',
    )
    model = models.PokerMemberVote
    extra = 0


@admin.register(models.PokerRoom)
class PokerRoomAdmin(admin.ModelAdmin):
    """Admin class for ``PokerRoom`` model."""

    fieldsets = (
        (_('Main'), {
            'fields': (
                'name',
                'token',
                'created',
            )
        }),
    )
    list_display = (
        'name',
        'token',
        'members',
        'created',
    )
    readonly_fields = (
        'created',
    )
    ordering = (
        '-created',
    )
    inlines = (
        PokerMemberInline,
        PokerRoundInline,
    )

    def members(self, obj):
        return ', '.join(member.name for member in obj.members.all())

    members.short_description = _('Members')


@admin.register(models.PokerMember)
class PokerMemberAdmin(admin.ModelAdmin):
    """Admin class for ``PokerMember`` model."""

    search_fields = (
        'name',
    )


@admin.register(models.PokerRound)
class PokerRoundAdmin(admin.ModelAdmin):
    """Admin class for ``PokerRound`` model."""

    fieldsets = (
        (_('Main'), {
            'fields': (
                'room',
                'created',
                'completed',
            )
        }),
    )
    list_display = (
        'id',
        'room',
        'created',
        'completed',
    )
    readonly_fields = (
        'room',
        'created',
    )
    inlines = (
        PokerMemberVoteInline,
    )

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from . import models


class PokerMemberInline(admin.TabularInline):
    """Inline class for ``PokerMember`` model."""

    readonly_fields = ('user',)
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
    actions = (
        'remove_empty_rounds',
    )

    def members(self, obj):
        """Get list of members."""
        return ', '.join(member.name for member in obj.members.all())

    members.short_description = _('Members')

    def remove_empty_rounds(self, request, queryset):
        """Action to remove empty rounds."""
        result = 0
        for room in queryset:
            for poker_round in room.rounds.filter(completed=True):
                if not poker_round._score:
                    result += 1
                    poker_round.delete()

        return messages.add_message(request, messages.INFO, _(
            'Removed rounds count is {}'
        ).format(result))

    remove_empty_rounds.short_description = _('Remove empty rounds')


@admin.register(models.PokerMember)
class PokerMemberAdmin(admin.ModelAdmin):
    """Admin class for ``PokerMember`` model."""

    search_fields = (
        'name',
    )
    list_display = (
        'name',
        'user',
        'is_active',
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

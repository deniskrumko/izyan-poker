from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from ..models import PokerRoom


class StatusView(View):
    """View for room status."""

    def get(self, request, token):
        room = get_object_or_404(PokerRoom, token=token)
        return JsonResponse({'status': room.status})

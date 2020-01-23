from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.shortcuts import (
    get_object_or_404,
    reverse,
)

__all__ = ('BaseView', 'LoginRequiredMixin')


class BaseView(TemplateView):
    """Base class for views."""

    def dispatch(self, request, *args, **kwargs):
        """Add user to view instance."""
        self.user = request.user if request.user.is_authenticated else None
        return super().dispatch(request, *args, **kwargs)

    def redirect(self, url, use_reverse=True, args=None):
        """Make redirect to provided URL."""
        url = reverse(url, args=args) if use_reverse else url
        return HttpResponseRedirect(url)

    def get_object_or_404(self, *args, **kwargs):
        """Get object or redirect to 404 page."""
        return get_object_or_404(*args, **kwargs)

from hashlib import blake2b
from typing import Optional

from django.http.response import HttpResponseRedirect
from django.shortcuts import (
    get_object_or_404,
    reverse,
)
from django.views.generic.base import TemplateView


class BaseView(TemplateView):
    """Base template view."""

    @property
    def session_key(self) -> Optional[str]:
        """Get session key."""
        key = self.request.session.session_key
        return blake2b(key.encode()).hexdigest() if key else None

    def create_session(self):
        """Create new session if it doesn't exist yet."""
        if not self.request.session.session_key:
            self.request.session.save()

    def redirect(self, url, args):
        """Redirect to provided url."""
        return HttpResponseRedirect(reverse(url, args=args))

    def get_object_or_404(self, *args, **kwargs):
        """Get object or redirect to 404 page."""
        return get_object_or_404(*args, **kwargs)

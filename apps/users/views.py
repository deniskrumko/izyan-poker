import re

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import (
    RedirectView,
    TemplateView,
)

from core.views import (
    BaseView,
    LoginRequiredMixin,
)

from .models import User


class LoginView(BaseView):
    """View for users to log in."""

    template_name = 'login.html'

    def post(self, request):
        """Get username and password to authenticate user."""
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,  # they are same
            password=password,
        )

        if user is not None:
            login(request, user)
            next_redirect = self.request.GET.get('next')
            return HttpResponseRedirect(
                next_redirect if next_redirect else reverse('poker:index')
            )

        messages.add_message(request, messages.ERROR, _(
            'User not found or password is incorrect'
        ))
        return HttpResponseRedirect(reverse('users:login'))


class SignUpView(TemplateView):
    """View for user to sign up.

    Currently this view is not used.

    """

    template_name = 'signup.html'

    def post(self, request):
        """Get all user params to create user."""
        email = request.POST.get('email')

        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')

        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not email:
            return HttpResponseRedirect(reverse('users:signup'))

        email_regexp = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        if not re.match(email_regexp, email):
            messages.add_message(request, messages.ERROR, _(
                'Incorrect email format'
            ))
            return HttpResponseRedirect(reverse('users:signup'))

        if User.objects.filter(
            Q(username=email) | Q(email=email)
        ).exists():
            messages.add_message(request, messages.ERROR, _(
                'User with such email already exists'
            ))
            return HttpResponseRedirect(reverse('users:signup'))

        if password != password2:
            messages.add_message(request, messages.ERROR, _(
                'Passwords do not match'
            ))
            return HttpResponseRedirect(reverse('users:signup'))

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=firstname,
            last_name=lastname,
        )

        return HttpResponseRedirect(reverse('users:login'))


class LogoutView(RedirectView):
    """View for users to log out."""

    url = '/'

    def get(self, request):
        """Log out current user."""
        logout(request)
        return super().get(request)


class UserView(LoginRequiredMixin, BaseView):
    """View for user settings."""

    template_name = 'user.html'

    def post(self, request):
        """Get all user params to create user."""
        request.user.first_name = request.POST.get('firstname', '')
        request.user.last_name = request.POST.get('lastname', '')
        request.user.save()

        messages.add_message(request, messages.SUCCESS, _(
            'Changes successfully saved'
        ))

        return HttpResponseRedirect('/user')

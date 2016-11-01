from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView


class UserProfileView(TemplateView):
    template_name = 'user_profile.html'

    def profile_user(self):
        return get_object_or_404(User, username=self.kwargs['username'])

from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from .serializers import UserSerializer, GroupSerializer
from rest_framework import viewsets


class UserProfileView(TemplateView):
    template_name = 'registration/user_profile.html'

    def profile_user(self):
        return get_object_or_404(User, username=self.kwargs['username'])


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
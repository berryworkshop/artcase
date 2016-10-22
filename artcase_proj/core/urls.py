from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User, Group
from rest_framework import routers, serializers, viewsets

from .views import UserProfileView
from artcase.views import IndexView


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# Routers provide automatic determination of the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='home'),
    
    url(r'^', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^', include('artcase.urls', namespace='artcase')),
    url(r'^api/', include(router.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^(?P<username>[-\w.@\+]+)/profile$', UserProfileView.as_view(), name='user_profile'),
]

 
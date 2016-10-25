from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from .views import UserProfileView, UserViewSet, GroupViewSet
from artcase.views import IndexView


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

    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'^(?P<username>[-\w.@\+]+)/profile$', UserProfileView.as_view(), name='user_profile'),
]

 
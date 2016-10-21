from django.conf.urls import include, url
from django.contrib import admin

from .views import UserProfileView
from artcase.views import IndexView

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='home'),
    
    url(r'^', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^', include('artcase.urls', namespace='artcase')),

    url(r'^(?P<username>[-\w.@\+]+)/profile$', UserProfileView.as_view(), name='user_profile'),
]

 
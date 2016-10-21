from django.conf.urls import include, url
from django.contrib import admin

from artcase.views import IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='home'),
    
    url(r'^', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^', include('artcase.urls', namespace='artcase')),
]

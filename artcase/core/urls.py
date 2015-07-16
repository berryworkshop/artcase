from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from artcase.views import HomeView
from artcase import urls as artcase_urls

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^collection/', include(artcase_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

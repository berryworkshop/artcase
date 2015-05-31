from django.conf.urls import include, url
from django.contrib import admin
from .views import (
    HomeView,
    ArtifactView,
    ArtifactListView,
    CreatorView,
    CreatorListView
)

urlpatterns = [

    # "collection/artifacts/PP_0123"
    url(r'^artifacts/(?P<code_number>[a-z|A-Z|0-9|_-]+/?)/$', ArtifactView.as_view(), name='artifact'),
    # "collection/artifacts/"
    url(r'^artifacts/$', ArtifactListView.as_view(), name='artifact_list'),

    # "collection/creators/PP_0123"
    url(r'^creators/(?P<slug>[a-z|A-Z|0-9|_-]+/?)/$', CreatorView.as_view(), name='creator'),
    # "collection/creators/"
    url(r'^creators/$', CreatorListView.as_view(), name='creator_list'),

]

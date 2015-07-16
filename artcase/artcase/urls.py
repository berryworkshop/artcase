from django.conf.urls import include, url
from django.contrib import admin
from .views import (
    HomeView,
    ArtifactView,
    ArtifactListView,
    CreatorView,
    CreatorListView,
    OrganizationView,
    OrganizationListView,
    CategoryView,
    CategoryListView,
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

    # "collection/organizations/amazing_org-kiev"
    url(r'^organizations/(?P<slug>[a-z|A-Z|0-9|_-]+/?)/$', OrganizationView.as_view(), name='organization'),
    # "collection/organizations/"
    url(r'^organizations/$', OrganizationListView.as_view(), name='organization_list'),

    # "collection/categories/civwar"
    url(r'^categories/(?P<slug>[a-z|A-Z|0-9|_-]+/?)/$', CategoryView.as_view(), name='category'),
    # "collection/categories/"
    url(r'^categories/$', CategoryListView.as_view(), name='category_list'),

]
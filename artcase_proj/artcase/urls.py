from django.conf.urls import url
from .views import (
    IndexView,
    WorkCreateView,
    WorkUpdateView,
    WorkDeleteView,
    WorkDetailView,
    WorkListView,
    CreatorListView,
    LocationListView,
    ImageListView,
    MediumListView,
    CategoryListView,
    CollectionListView,
)

urlpatterns = [
    url(r'^$',
        IndexView.as_view(), name='index'),

    url(r'^work_create$', 
        WorkCreateView.as_view(), name='work_create'),
    url(r'^work/(?P<slug>[-\w]+)$',
        WorkDetailView.as_view(), name='work_detail'),
    url(r'^work/(?P<slug>[-\w]+)/update$', 
        WorkUpdateView.as_view(), name='work_update'),
    url(r'^work/(?P<slug>[-\w]+)/delete$', 
        WorkDeleteView.as_view(), name='work_delete'),

    url(r'^work_list$',
        WorkListView.as_view(), name='work_list'),
    url(r'^creator_list$',
        CreatorListView.as_view(), name='creator_list'),
    url(r'^location_list$',
        LocationListView.as_view(), name='location_list'),
    url(r'^image_list$',
        ImageListView.as_view(), name='image_list'),
    url(r'^medium_list$',
        MediumListView.as_view(), name='medium_list'),
    url(r'^category_list$',
        CategoryListView.as_view(), name='category_list'),
    url(r'^collection_list$',
        CollectionListView.as_view(), name='collection_list'),
]

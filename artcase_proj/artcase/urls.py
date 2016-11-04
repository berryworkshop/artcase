from django.conf.urls import url
from .views import (
    IndexView,
    WorkDetailView,
    WorkListView,
    WorkCreateView,
    WorkUpdateView,
    WorkDeleteView,
    CreatorDetailView,
    CreatorListView,
    CreatorCreateView,
    CreatorUpdateView,
    CreatorDeleteView,
    LocationListView,
    ImageListView,
    MediumListView,
    CategoryListView,
    CollectionListView,
)

urlpatterns = [
    url(r'^$',
        IndexView.as_view(), name='index'),

    # works
    url(r'^work/(?P<pk>\d+)$',
        WorkDetailView.as_view(), name='work_detail'),
    url(r'^work_list$',
        WorkListView.as_view(), name='work_list'),
    url(r'^work_create$', 
        WorkCreateView.as_view(), name='work_create'),
    url(r'^work/(?P<pk>\d+)/update$', 
        WorkUpdateView.as_view(), name='work_update'),
    url(r'^work/(?P<pk>\d+)/delete$', 
        WorkDeleteView.as_view(), name='work_delete'),

    # creators
    url(r'^creator/(?P<pk>\d+)$',
        CreatorDetailView.as_view(), name='creator_detail'),
    url(r'^creator_list$',
        CreatorListView.as_view(), name='creator_list'),
    url(r'^creator_create$', 
        CreatorCreateView.as_view(), name='creator_create'),
    url(r'^creator/(?P<pk>\d+)/update$', 
        CreatorUpdateView.as_view(), name='creator_update'),
    url(r'^creator/(?P<pk>\d+)/delete$', 
        CreatorDeleteView.as_view(), name='creator_delete'),

    
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

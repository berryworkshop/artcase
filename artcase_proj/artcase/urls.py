from django.conf.urls import url
from .models import (
    Work, Creator, Location, Image, Medium, Category, Collection)
from .views import (
    IndexView,
    
    ArtcaseDetailView,
    ArtcaseListView,
    ArtcaseCreateView,
    ArtcaseUpdateView,
    ArtcaseDeleteView,

    # WorkDetailView,
    # WorkListView,
    # WorkCreateView,
    # WorkUpdateView,
    # WorkDeleteView,
    
    CreatorDetailView,
    CreatorListView,
    CreatorCreateView,
    CreatorUpdateView,
    CreatorDeleteView,

    LocationDetailView,
    LocationListView,
    LocationCreateView,
    LocationUpdateView,
    LocationDeleteView,
    
    ImageDetailView,
    ImageListView,
    ImageCreateView,
    ImageUpdateView,
    ImageDeleteView,

    MediumDetailView,
    MediumListView,
    MediumCreateView,
    MediumUpdateView,
    MediumDeleteView,
    
    CategoryDetailView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    
    CollectionDetailView,
    CollectionListView,
    CollectionCreateView,
    CollectionUpdateView,
    CollectionDeleteView,
)

urlpatterns = [
    url(r'^$',
        IndexView.as_view(), name='index'),

    # works
    url(r'^work/(?P<pk>\d+)$',
        ArtcaseDetailView.as_view(
            title = 'Work',
            model = Work
        ), name='work_detail'),

    url(r'^work_list$',
        ArtcaseListView.as_view(
            title = 'List of Works',
            model = Work
        ), name='work_list'),
    
    url(r'^work_create$', 
        ArtcaseCreateView.as_view(
            title = 'Create a Work',
            model = Work
        ), name='work_create'),

    url(r'^work/(?P<pk>\d+)/update$', 
        ArtcaseUpdateView.as_view(
            title = 'Update Work',
            model = Work
        ), name='work_update'),

    url(r'^work/(?P<pk>\d+)/delete$', 
        ArtcaseDeleteView.as_view(
            title = 'Delete Work',
            model = Work
        ), name='work_delete'),

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

    #locations
    url(r'^location/(?P<pk>\d+)$',
        LocationDetailView.as_view(), name='location_detail'),
    url(r'^location_list$',
        LocationListView.as_view(), name='location_list'),
    url(r'^location_create$', 
        LocationCreateView.as_view(), name='location_create'),
    url(r'^location/(?P<pk>\d+)/update$', 
        LocationUpdateView.as_view(), name='location_update'),
    url(r'^location/(?P<pk>\d+)/delete$', 
        LocationDeleteView.as_view(), name='location_delete'),
    
    #images
    url(r'^image/(?P<pk>\d+)$',
        ImageDetailView.as_view(), name='image_detail'),
    url(r'^image_list$',
        ImageListView.as_view(), name='image_list'),
    url(r'^image_create$', 
        ImageCreateView.as_view(), name='image_create'),
    url(r'^image/(?P<pk>\d+)/update$', 
        ImageUpdateView.as_view(), name='image_update'),
    url(r'^image/(?P<pk>\d+)/delete$', 
        ImageDeleteView.as_view(), name='image_delete'),
    
    #media
    url(r'^medium/(?P<pk>\d+)$',
        MediumDetailView.as_view(), name='medium_detail'),
    url(r'^medium_list$',
        MediumListView.as_view(), name='medium_list'),
    url(r'^medium_create$', 
        MediumCreateView.as_view(), name='medium_create'),
    url(r'^medium/(?P<pk>\d+)/update$', 
        MediumUpdateView.as_view(), name='medium_update'),
    url(r'^medium/(?P<pk>\d+)/delete$', 
        MediumDeleteView.as_view(), name='medium_delete'),
    
    #categories
    url(r'^category/(?P<pk>\d+)$',
        CategoryDetailView.as_view(), name='category_detail'),
    url(r'^category_list$',
        CategoryListView.as_view(), name='category_list'),
    url(r'^category_create$', 
        CategoryCreateView.as_view(), name='category_create'),
    url(r'^category/(?P<pk>\d+)/update$', 
        CategoryUpdateView.as_view(), name='category_update'),
    url(r'^category/(?P<pk>\d+)/delete$', 
        CategoryDeleteView.as_view(), name='category_delete'),
    
    #collections
    url(r'^collection/(?P<pk>\d+)$',
        CollectionDetailView.as_view(), name='collection_detail'),
    url(r'^collection_list$',
        CollectionListView.as_view(), name='collection_list'),
    url(r'^collection_create$', 
        CollectionCreateView.as_view(), name='collection_create'),
    url(r'^collection/(?P<pk>\d+)/update$', 
        CollectionUpdateView.as_view(), name='collection_update'),
    url(r'^collection/(?P<pk>\d+)/delete$', 
        CollectionDeleteView.as_view(), name='collection_delete'),
]

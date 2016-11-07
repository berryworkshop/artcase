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
)

urlpatterns = [
    url(r'^$',
        IndexView.as_view(), name='index'),

    # works
    url(r'^work/(?P<pk>\d+)$',
        ArtcaseDetailView.as_view(
            model = Work
        ), name='work_detail'),
    url(r'^work_list$',
        ArtcaseListView.as_view(
            model = Work
        ), name='work_list'),
    url(r'^work_create$', 
        ArtcaseCreateView.as_view(
            model = Work
        ), name='work_create'),
    url(r'^work/(?P<pk>\d+)/update$', 
        ArtcaseUpdateView.as_view(
            model = Work
        ), name='work_update'),
    url(r'^work/(?P<pk>\d+)/delete$', 
        ArtcaseDeleteView.as_view(
            model = Work
        ), name='work_delete'),

    # creators
    url(r'^creator/(?P<pk>\d+)$',
        ArtcaseDetailView.as_view(
            model = Creator
        ), name='creator_detail'),
    url(r'^creator_list$',
        ArtcaseListView.as_view(
            model = Creator
        ), name='creator_list'),
    url(r'^creator_create$', 
        ArtcaseCreateView.as_view(
            model = Creator
        ), name='creator_create'),
    url(r'^creator/(?P<pk>\d+)/update$', 
        ArtcaseUpdateView.as_view(
            model = Creator
        ), name='creator_update'),
    url(r'^creator/(?P<pk>\d+)/delete$', 
        ArtcaseDeleteView.as_view(
            model = Creator
        ), name='creator_delete'),

    #locations
    url(r'^location/(?P<pk>\d+)$',
        ArtcaseDetailView.as_view(
            model = Location
        ), name='location_detail'),
    url(r'^location_list$',
        ArtcaseListView.as_view(
            model = Location
        ), name='location_list'),
    url(r'^location_create$', 
        ArtcaseCreateView.as_view(
            model = Location
        ), name='location_create'),
    url(r'^location/(?P<pk>\d+)/update$', 
        ArtcaseUpdateView.as_view(
            model = Location
        ), name='location_update'),
    url(r'^location/(?P<pk>\d+)/delete$', 
        ArtcaseDeleteView.as_view(
            model = Location
        ), name='location_delete'),
    
    #images
    url(r'^image/(?P<pk>\d+)$',
        ArtcaseDetailView.as_view(
            model = Image
        ), name='image_detail'),
    url(r'^image_list$',
        ArtcaseListView.as_view(
            model = Image
        ), name='image_list'),
    url(r'^image_create$', 
        ArtcaseCreateView.as_view(
            model = Image
        ), name='image_create'),
    url(r'^image/(?P<pk>\d+)/update$', 
        ArtcaseUpdateView.as_view(
            model = Image
        ), name='image_update'),
    url(r'^image/(?P<pk>\d+)/delete$', 
        ArtcaseDeleteView.as_view(
            model = Image
        ), name='image_delete'),
    
    #media
    url(r'^medium/(?P<pk>\d+)$',
        ArtcaseDetailView.as_view(
            model = Medium
        ), name='medium_detail'),
    url(r'^medium_list$',
        ArtcaseListView.as_view(
            model = Medium
        ), name='medium_list'),
    url(r'^medium_create$', 
        ArtcaseCreateView.as_view(
            model = Medium
        ), name='medium_create'),
    url(r'^medium/(?P<pk>\d+)/update$', 
        ArtcaseUpdateView.as_view(
            model = Medium
        ), name='medium_update'),
    url(r'^medium/(?P<pk>\d+)/delete$', 
        ArtcaseDeleteView.as_view(
            model = Medium
        ), name='medium_delete'),
    
    #categories
    url(r'^category/(?P<pk>\d+)$',
        ArtcaseDetailView.as_view(
            model = Category
        ), name='category_detail'),
    url(r'^category_list$',
        ArtcaseListView.as_view(
            model = Category
        ), name='category_list'),
    url(r'^category_create$', 
        ArtcaseCreateView.as_view(
            model = Category
        ), name='category_create'),
    url(r'^category/(?P<pk>\d+)/update$', 
        ArtcaseUpdateView.as_view(
            model = Category
        ), name='category_update'),
    url(r'^category/(?P<pk>\d+)/delete$', 
        ArtcaseDeleteView.as_view(
            model = Category
        ), name='category_delete'),
    
    #collections
    url(r'^collection/(?P<pk>\d+)$',
        ArtcaseDetailView.as_view(
            model = Collection
        ), name='collection_detail'),
    url(r'^collection_list$',
        ArtcaseListView.as_view(
            model = Collection
        ), name='collection_list'),
    url(r'^collection_create$', 
        ArtcaseCreateView.as_view(
            model = Collection
        ), name='collection_create'),
    url(r'^collection/(?P<pk>\d+)/update$', 
        ArtcaseUpdateView.as_view(
            model = Collection
        ), name='collection_update'),
    url(r'^collection/(?P<pk>\d+)/delete$', 
        ArtcaseDeleteView.as_view(
            model = Collection
        ), name='collection_delete'),
]

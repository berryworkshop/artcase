from django.conf.urls import url
from .models import (
    Work,
    Creator,
    Location,
    Image,
    Medium,
    Category,
    Collection,
)
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
]

for model in [Work, Creator, Location, Image, Medium, Category, Collection]:
    name = model._meta.verbose_name
    patterns = [
        url(r'^%s/(?P<pk>\d+)$' % name,
            ArtcaseDetailView.as_view(
                model = model
            ), name='%s_detail' % name),

        url(r'^%s_list$' % name,
            ArtcaseListView.as_view(
                model = model
            ), name='%s_list' % name),

        url(r'^%s_create$' % name, 
            ArtcaseCreateView.as_view(
                model = model
            ), name='%s_create' % name),

        url(r'^%s/(?P<pk>\d+)/update$' % name, 
            ArtcaseUpdateView.as_view(
                model = model
            ), name='%s_update' % name),

        url(r'^%s/(?P<pk>\d+)/delete$' % name, 
            ArtcaseDeleteView.as_view(
                model = model
            ), name='%s_delete' % name),
    ]
    urlpatterns.extend(patterns)
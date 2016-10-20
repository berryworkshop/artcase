from django.conf.urls import url
from .views import IndexView, WorkCreateView, WorkUpdateView, WorkDeleteView, WorkListView, WorkDetailView

urlpatterns = [
    url(r'^$',
        IndexView.as_view(), name='index'),
    url(r'^work_create$', 
        WorkCreateView.as_view(), name='work_create'),
    url(r'^work_list$',
        WorkListView.as_view(), name='work_list'),
    url(r'^work/(?P<slug>[-\w]+)/detail$',
        WorkDetailView.as_view(), name='work_detail'),
    url(r'^work/(?P<slug>[-\w]+)/update$', 
        WorkUpdateView.as_view(), name='work_update'),
    url(r'^work/(?P<slug>[-\w]+)/delete$', 
        WorkDeleteView.as_view(), name='work_delete'),
]

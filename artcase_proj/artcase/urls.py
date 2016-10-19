from django.conf.urls import url
from .views import IndexView, WorkCreateView, WorkListView, WorkDetailView

urlpatterns = [
    url(r'^$',
        IndexView.as_view(), name='index'),
    url(r'^work_create$', 
        WorkCreateView.as_view(), name='work_create'),
    url(r'^work_list$',
        WorkListView.as_view(), name='work_list'),
    url(r'^work_detail/(?P<slug>[-\w]+)$',
        WorkDetailView.as_view(), name='work_detail'),
]

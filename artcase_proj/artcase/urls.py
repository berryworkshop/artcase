from django.conf.urls import url
from .views import IndexView, WorkCreateView, WorkDetailView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^works/create$', 
        WorkCreateView.as_view(), name='work_create'),
    url(r'^works/(?P<slug>[-\w]+)$',
        WorkDetailView.as_view(), name='work_detail'),
]

from django.conf.urls import url
from .views import IndexView, WorkCreateView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^work$', WorkCreateView.as_view(), name='work_create'),
]

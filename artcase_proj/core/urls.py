from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import (
    # password_reset, 
    # password_reset_done,
    # password_reset_confirm, 
    # password_reset_complete,
    # these are the two new imports
    password_change,
    password_change_done,
)

from .views import UserProfileView
from artcase.views import IndexView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^(?P<username>[-\w.@\+]+)/profile$', UserProfileView.as_view(), name='user_profile'),


    # url(r'^api-auth/', include('rest_framework.urls')),
    # url(r'^api/$', include('api.urls', namespace='api')),

    url(r'^artcase/', include('artcase.urls', namespace='artcase')),


    # url(r'^accounts/password_reset/$',
    #     password_reset,
    #     {'template_name': 'registration/password_reset_form.html'},
    #     name="password_reset"),
    # url(r'^accounts/password_reset/done/$',
    #     password_reset_done,
    #     {'template_name': 'registration/password_reset_done.html'},
    #     name="password_reset_done"),
    # url(r'^accounts/password_reset/confirm/$',
    #     password_reset_confirm,
    #     {'template_name': 'registration/password_reset_confirm.html'},
    #     name="password_reset_confirm"),
    # url(r'^accounts/password_reset/complete/$',
    #     password_reset_complete,
    #     {'template_name': 'registration/password_reset_complete.html'},
    #     name="password_reset_complete"),

    # url(r'^accounts/password_change/$', password_change, {
    #     'template_name': 'registration/password_change_form.html'}, 
    #     name='password_change'),
    # url(r'^accounts/password_change/done/$', password_change_done, 
    #     {'template_name': 'registration/password_change_done.html'},
    #     name='password_change_done'),

    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^django-admin/', include(admin.site.urls)),
# 
]



# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from iddacultura.views import user_profile, home_view, ProfileDetailView, ProfileEditView, ProfileListView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^/?$', home_view, name='homepage'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^user_profile/$', user_profile),

    url(r'^users/edit/$', ProfileEditView.as_view(), name='profiles_edit_profile'),
    url(r'^users/(?P<username>[\w.+-]+)/$', ProfileDetailView.as_view(), name='profiles_profile_detail'),
    url(r'^users/$', ProfileListView.as_view()),

    url(r'^provider/', include('iddacultura.provider.urls')),
    url(r'^openid/', include('openid_provider.urls')),
)

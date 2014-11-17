# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from iddacultura.views import user_profile, password_changed_ok, login_after_password_change, HomeView, ProfileDetailView, ProfileEditView, ProfileListView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^/?$', HomeView.as_view(), name='homepage'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/password/change/$', login_after_password_change, name='account_change_password'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^password_changed_ok', password_changed_ok, name='password_changed_ok'),

    url(r'^user_profile/$', user_profile),

    url(r'^users/edit/$', ProfileEditView.as_view(), name='profiles_edit_profile'),
    url(r'^users/(?P<username>[\w.+-]+)/$', ProfileDetailView.as_view(), name='profiles_profile_detail'),
    url(r'^users/$', ProfileListView.as_view()),
    url(r'^openid/', include('openid_provider.urls')),
)

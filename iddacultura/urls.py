# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from registration.views import register
from forms import UserRegistrationForm
from iddacultura.views import user_profile, HomeView, ProfileDetailView, ProfileEditView, ProfileListView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^/?$', HomeView.as_view(), name='homepage'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/logout/$', 'iddacultura.views.logout'),
    url(r'^accounts/register/$', register,
        {'backend': 'iddacultura.regbackend.RegBackend',
            'form_class': UserRegistrationForm},
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^user_profile/$', user_profile),

    url(r'^users/edit', ProfileEditView.as_view(), name='profiles_edit_profile'),
    url(r'^users/(?P<username>[\w.+-]+)/', ProfileDetailView.as_view(), name='profiles_profile_detail'),
    url(r'^users/', ProfileListView.as_view()),

    url(r'^provider/', include('iddacultura.provider.urls')),
)

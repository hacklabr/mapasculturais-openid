# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from registration.views import register
from forms import UserRegistrationForm, UserProfilePublicForm
from iddacultura.views import user_profile

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^user_profile/$', user_profile),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/logout/$', 'iddacultura.views.logout'),
    url(r'^accounts/register/$', register,
        {'backend': 'iddacultura.regbackend.RegBackend',
            'form_class': UserRegistrationForm},
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^users/edit', 'profiles.views.edit_profile',
        {'form_class': UserProfilePublicForm}),
    url(r'^users/', include('profiles.urls')),
    url(r'^provider/', include('iddacultura.provider.urls')),
)

#TODO: por que é necessário colocar isso separado das demais urlpatterns?
urlpatterns += patterns(
    'django.contrib.flatpages.views',
    url(r'^/?$', 'flatpage', {'url': '/'}, name='homepage'),
)

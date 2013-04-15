# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from registration.views import register
from forms import UserRegistrationForm, UserProfilePublicForm
from iddacultura.views import user_profile, occupations

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^user_profile/$', user_profile),
    url(r'^occupations/', occupations),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', register, {'backend': 'iddacultura.regbackend.RegBackend', 'form_class': UserRegistrationForm}, name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profiles/edit', 'profiles.views.edit_profile', {'form_class': UserProfilePublicForm}),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^provider/', include('iddacultura.provider.urls')),
)

#TODO: por que é necessário colocar isso separado das demais urlpatterns?
urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^/?$', 'flatpage', {'url': '/'}, name='homepage'),
)
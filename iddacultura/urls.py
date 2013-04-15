from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
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

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^/?$', 'flatpage', {'url': '/'}, name='homepage'),
)
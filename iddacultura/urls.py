from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from registration.views import register
from forms import UserRegistrationForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name="iddacultura/home.html")),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', register, {'backend': 'iddacultura.regbackend.RegBackend', 'form_class': UserRegistrationForm}, name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profiles/', include('profiles.urls')),
)

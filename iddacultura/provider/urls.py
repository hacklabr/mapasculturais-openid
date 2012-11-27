from django.conf.urls import patterns

urlpatterns = patterns(
    'iddacultura.provider.views',
    (r'^$', 'endpoint'),
    (r'^xrds/$', 'idpXrds'),
    (r'^processTrustResult/$', 'processTrustResult'),
    (r'^trust/$', 'trustPage'),
)

from django.conf.urls import patterns

urlpatterns = patterns(
    'iddacultura.provider.views',
    (r'^$', 'server'),
    (r'^xrds/$', 'idpXrds'),
    (r'^processTrustResult/$', 'processTrustResult'),
    (r'^endpoint/$', 'endpoint'),
    (r'^trust/$', 'trustPage'),
)

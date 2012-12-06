from django.conf.urls import patterns

urlpatterns = patterns(
    'iddacultura.provider.views',
    (r'^$', 'endpoint'),
    (r'^xrds/$', 'opXrds'),
    (r'^xrds/(?P<username>[^/]+)$', 'userXrds'),
    (r'^processTrustResult/$', 'processTrustResult'),
    (r'^trust/$', 'trustPage'),
)

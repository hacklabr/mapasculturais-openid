from django.conf.urls import patterns

urlpatterns = patterns(
    'iddacultura.provider.views',
    (r'^$', 'endpoint'),
    (r'^xrds/$', 'op_xrds'),
    (r'^xrds/(?P<username>[^/]+)$', 'user_xrds'),
    (r'^processTrustResult/$', 'processTrustResult'),
    (r'^trust/$', 'trustPage'),
)

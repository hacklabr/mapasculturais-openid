from django.conf import settings
from django.contrib.sites.models import Site


class MultiSiteMiddleware(object):
    def process_request(self, request):
        host = request.get_host()
        host_part = host.split(':')[0]
        site = Site.objects.get(domain=host_part)
        settings.SITE_ID = site.id
        Site.objects.clear_cache()
        return

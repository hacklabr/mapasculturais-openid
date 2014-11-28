from django.conf import settings
from django.contrib.sites.models import Site


class MultiSiteMiddleware(object):
    def process_request(self, request):
        host = request.get_host()
        host_part = host.split(':')[0]
        try:
            site = Site.objects.get(domain=host_part)
            settings.SITE_ID = site.id
        except Site.DoesNotExist:  # use default if it doesn't exist
            settings.SITE_ID = 1

        Site.objects.clear_cache()
        return

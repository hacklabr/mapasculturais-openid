# coding: utf-8
from .models import SiteConfig
from django.contrib.sites.models import get_current_site


def site_data(request):
    try:
        site_conf = SiteConfig.objects.get(site=get_current_site(request))
    except SiteConfig.DoesNotExist:
        site_conf = None
    return {'site_conf': site_conf}

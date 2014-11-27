# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site


class SiteConfig(models.Model):
    site = models.OneToOneField(Site)
    default_url = models.CharField(max_length=200)
    default_name = models.CharField(max_length=200)
    org_name = models.CharField(max_length=200)
    org_url = models.CharField(max_length=200)
    brand_logo = models.BooleanField()

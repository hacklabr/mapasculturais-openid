# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings
import os
from os.path import join, isdir


THEMES = [fname for fname in os.listdir(settings.THEMES_DIR) if isdir(join(settings.THEMES_DIR, fname))]
THEMES_CHOICES = [(fname, fname) for fname in THEMES]


class SiteConfig(models.Model):
    site = models.OneToOneField(Site)
    default_url = models.CharField(max_length=200)
    default_name = models.CharField(max_length=200)
    org_name = models.CharField(max_length=200)
    org_url = models.CharField(max_length=200)
    brand_logo = models.BooleanField()
    theme = models.CharField(max_length=200, choices=THEMES_CHOICES)

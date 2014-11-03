# -*- coding: utf-8 -*-

from django.db import models


class TrustedRoot(models.Model):
    """
    Lista de trusted root URLs
    """
    url = models.URLField()
    always_trusted = models.BooleanField(u"Confiar sempre", default=False)

    def __unicode__(self):
        return self.url

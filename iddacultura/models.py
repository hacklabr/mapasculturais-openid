# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractUser


class TrustedRoot(models.Model):
    """
    Lista de trusted root URLs
    """
    url = models.URLField()
    always_trusted = models.BooleanField(u"Confiar sempre", default=False)

    def __unicode__(self):
        return self.url


class IDUser(AbstractUser):
    """
    Adiciona campos extras para os usuários
    """

    trusted_roots = models.ManyToManyField(
        TrustedRoot, blank=True, null=True,
        verbose_name="Sites autorizados",
        help_text="Lista de clientes OpenID autorizados.")

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def get_absolute_url(self):
        return reverse(
            'profiles_profile_detail',
            args=[unicode(self.user.username)])

    def trusted_url(self, url):
        """
        Verifica se a URL do consumer está na lista de
        trusted URLs do usuário
        """
        urls = TrustedRoot.objects.filter(url=url)
        if len(urls) == 0:
            # nunca nenhum usuário usou esse OpenID consumer, adiciona ele
            # a lista e retorna false
            TrustedRoot(url=url).save()

        elif urls.filter(always_trusted=True).count() > 0:
            return True

        else:
            for trusted_root in self.trusted_roots.all():
                if url == trusted_root.url:
                    return True
        return False

    def __unicode__(self):
        return self.username

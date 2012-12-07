# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

class TrustedRoot(models.Model):
    """
    Lista de trusted root URLs
    """
    url = models.URLField()

    def __unicode__(self):
        return self.url

class UserProfile(models.Model):
    """
    Adiciona campos extras para os usuários
    """
    
    user = models.OneToOneField(User)
    trusted_roots = models.ManyToManyField(TrustedRoot, blank = True, null = True, help_text = "OpenID consumers URL's trusted by this user")
    cpf = models.CharField(max_length=50)
    
    def get_absolute_url(self):
        return reverse('profiles_profile_detail', args=[unicode(self.user.username)])
    
    def trusted_url(self, url):
        """
        Verifica se a URL do consumer está na lista de
        trusted URLs do usuário
        """
        urls = TrustedRoot.objects.filter(url = url)
        if len(urls) == 0:
            # nunca nenhum usuário usou esse OpenID consumer, adiciona ele a lista e retorna false
            TrustedRoot(url = url).save()
        else:
            for trusted_root in self.trusted_roots.all():
                if url == trusted_root.url:
                    return True
        return False
    
    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

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

class UserOccupation(models.Model):
    """
    Valores possíveis para os diferentes campos
    para definir a ocupação de um usuário de acordo
    com o padrão estabelecido pelo governo federal.
    """
    
    TYPE_CHOICES = (
        ('primary', 'primary'),
        ('secondary', 'secondary'),
        ('tertiary', 'tertiary'),
        ('quartenary', 'quartenary'),
        ('quinary', 'quinary'),
        ('synonymous', 'synonymous')
    )
    
    parent = models.CharField(max_length = 10)
    type = models.CharField(max_length = 10, choices = TYPE_CHOICES)
    code = models.CharField(max_length = 10)
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    """
    Adiciona campos extras para os usuários
    """
    
    user = models.OneToOneField(User)
    cpf = models.CharField(max_length = 50, verbose_name = "CPF", unique = True)
    trusted_roots = models.ManyToManyField(TrustedRoot, blank = True, null = True, verbose_name = "Sites autorizados", help_text = "Lista de clientes OpenID autorizados.")
    
    user_occupation_primary = models.ForeignKey(UserOccupation, limit_choices_to = {'type': 'primary'}, related_name = 'occupation_primary', verbose_name = "Grande grupo", null = True)
    user_occupation_secondary = models.ForeignKey(UserOccupation, limit_choices_to = {'type': 'secondary'}, related_name = 'occupation_secondary', verbose_name = "Sub-grupo principal", null = True)
    user_occupation_tertiary = models.ForeignKey(UserOccupation, limit_choices_to = {'type': 'tertiary'}, related_name = 'occupation_tertiary', verbose_name = "Sub-grupo", null = True)
    user_occupation_quartenary = models.ForeignKey(UserOccupation, limit_choices_to = {'type': 'quartenary'}, related_name = 'occupation_quartenary', verbose_name = "Família", null = True)
    user_occupation_quinary = models.ForeignKey(UserOccupation, limit_choices_to = {'type': 'quinary'}, related_name = 'occupation_quinary', verbose_name = "Ocupação", null = True)
    
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
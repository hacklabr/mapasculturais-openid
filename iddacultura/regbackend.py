# -*- coding: utf-8 -*-

from registration.backends.default import DefaultBackend
from registration import signals
from registration.models import RegistrationProfile

from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from models import UserProfile, UserOccupation

class RegBackend(DefaultBackend):
    """
    Extende a classe DefaultBackend para salvar os campos
    customizados do usuário como o CPF no momento do registro
    de um novo usuário.
    """
    
    def register(self, request, **kwargs):
        """
        Sobrescreve o método original para salvar os campos customizados
        do usuário
        """

        username, email, password = kwargs['username'], kwargs['email'], kwargs['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                    password, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        
        u = UserProfile.objects.get(user_id = new_user.id)
        u.cpf = kwargs['cpf']
        u.user_occupation_primary = UserOccupation.objects.get(id = kwargs['user_occupation_primary'])
        u.user_occupation_secondary = UserOccupation.objects.get(id = kwargs['user_occupation_secondary'])
        u.user_occupation_tertiary = UserOccupation.objects.get(id = kwargs['user_occupation_tertiary'])
        u.user_occupation_quartenary = UserOccupation.objects.get(id = kwargs['user_occupation_quartenary'])
        u.user_occupation_quinary = UserOccupation.objects.get(id = kwargs['user_occupation_quinary'])
        u.save()
        
        return new_user
    
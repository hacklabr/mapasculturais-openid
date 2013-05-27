# -*- coding: utf-8 -*-

from registration.backends.default import DefaultBackend
from registration import signals
from registration.models import RegistrationProfile

from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from models import UserProfile

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

        u = User.objects.get(id = new_user.id)
        u.first_name = kwargs['first_name']
        u.last_name = kwargs['last_name']
        u.save()
        
        u = UserProfile.objects.get(user_id = new_user.id)
        u.cpf = kwargs['cpf']
        u.save()
        
        return new_user
    
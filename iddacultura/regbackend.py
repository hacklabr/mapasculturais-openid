# -*- coding: utf-8 -*-

from registration.backends.simple import SimpleBackend
from django.contrib.auth.models import User
from models import UserProfile


class RegBackend(SimpleBackend):
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

        new_user = super(RegBackend, self).register(request, **kwargs)

        u = User.objects.get(id=new_user.id)
        u.first_name = kwargs['first_name']
        u.last_name = kwargs['last_name']
        u.save()

        u = UserProfile.objects.get(user_id=new_user.id)
        u.cpf = kwargs['cpf']
        u.save()

        return new_user

    def post_registration_redirect(self, request, user):
        """
        Sobrescreve o método original para continuar o processo
        de autenticação OpenID se o usuário estiver criando uma
        conta para autorizar a autenticação em um cliente.
        """
        original = super(RegBackend, self).post_registration_redirect(request, user)

        if 'next' in request.POST:
            return (request.POST['next'], (), {})
        else:
            return original

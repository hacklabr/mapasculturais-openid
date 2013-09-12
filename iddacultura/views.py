# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.contrib import messages


def user_profile(request):
    """
    Redireciona para a pagina do usuario.
    Talvez exista uma maneira de fazer isso diretamente no login.html
    """
    return redirect('/profiles/' + request.user.username + '/')


def logout(request):
    """
    Adiciona mensagem a ser exibida na página de login
    quando o usuário sai do sistema
    """

    messages.add_message(request, messages.INFO,
        'Você acabou de sair de sua conta!')

    return auth_views.logout_then_login(request)

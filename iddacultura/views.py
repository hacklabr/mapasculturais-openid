# -*- coding: utf-8 -*-

import json
from django.shortcuts import redirect
from django.http import HttpResponse
from models import UserOccupation
from django.contrib.auth import views as auth_views
from django.contrib import messages

def user_profile(request):
    """
    Redireciona para a pagina do usuario.
    Talvez exista uma maneira de fazer isso diretamente no login.html
    """
    return redirect('/profiles/' + request.user.username + '/')

def occupations(request):
    """
    Retorna um JSON com a lista de ocupações em um
    nível com base no pai
    """
    occupations = {}
    occupations[u''] = 'Selecione'
    
    parent = UserOccupation.objects.get(id = request.GET['parent'])
    
    for occupation in UserOccupation.objects.filter(parent = parent.code):
        occupations[occupation.id] = occupation.name
    
    return HttpResponse(json.dumps(occupations), content_type="application/json")

def logout(request):
    """
    Adiciona mensagem a ser exibida na página de login
    quando o usuário sai do sistema
    """
    
    messages.add_message(request, messages.INFO, 'Você acabou de sair de sua conta!')
        
    return auth_views.logout_then_login(request)
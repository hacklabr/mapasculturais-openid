# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib import messages
from django.contrib.auth import get_user_model
from braces.views import LoginRequiredMixin


def user_profile(request):
    """
    Redireciona para a pagina do usuario.
    Talvez exista uma maneira de fazer isso diretamente no login.html
    """
    return redirect('/users/' + request.user.username + '/')


def logout(request):
    """
    Adiciona mensagem a ser exibida na página de login
    quando o usuário sai do sistema
    """

    messages.add_message(
        request, messages.INFO,
        'Você acabou de sair de sua conta!')

    return auth_views.logout_then_login(request)


class HomeView(TemplateView):
    template_name = 'iddacultura/home.html'


class ProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'profiles/profile_detail.html'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'profiles/edit_profile.html'

    def get_object(self):
        return self.request.user


class ProfileListView(ListView):
    model = get_user_model()
    template_name = 'profiles/profile_list.html'

# -*- coding: utf-8 -*-

from allauth.account.forms import LoginForm, UserForm

from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
# TODO: Remover
# from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib import messages
from django.contrib.auth import get_user_model

from braces.views import LoginRequiredMixin

from django.template.response import RequestContext
from django.shortcuts import render_to_response

from iddacultura.forms import OpenIDSignupForm


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


def home_view(request):
# TODO: Testar se é possível usar um template_name condicional com o TemplateView
    if (request.user.is_authenticated()):
        return user_autenticated_view(request)
    else:
        return signup_view(request)


# TODO: Mudar para TemplateView
def signup_view(request):
    return render_to_response("account/signup.html", {'form': OpenIDSignupForm}, context_instance=RequestContext(request))


# TODO: Mudar para TemplateView
def user_autenticated_view(request):
    return render_to_response("iddacultura/user_autenticated.html", {'form': None}, context_instance=RequestContext(request))


class ProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'profiles/profile_detail.html'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'profiles/edit_profile.html'
    form_class = UserForm

    def get_object(self):
        return self.request.user


class ProfileListView(ListView):
    model = get_user_model()
    template_name = 'profiles/profile_list.html'


# TODO: Mudar para TemplateView
def login_view(request):
    return render_to_response('iddacultura/login.html', {'form': LoginForm}, context_instance=RequestContext(request))

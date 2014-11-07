# -*- coding: utf-8 -*-

from allauth.account.views import PasswordChangeView

from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

from django.shortcuts import render_to_response
from django.template.response import RequestContext

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


class HomeView(TemplateView):

    def get(self, request, *args, **kwargs):
        return self.get_response(request)

    def post(self, request, *args, **kwargs):
        return self.get_response(request)

    def get_response(self, request):
        if (request.user.is_authenticated()):
            return redirect('/users/' + request.user.username + '/')
        else:
            return render_to_response("account/signup.html", {'form': OpenIDSignupForm}, context_instance=RequestContext(request))


class ProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'profiles/profile_detail.html'


class ProfileEditView(UpdateView):
    model = User
    template_name = 'profiles/edit_profile.html'
    fields = ['first_name', 'last_name', 'email', ]

    def get_object(self):
        return self.request.user


class ProfileListView(ListView):
    model = get_user_model()
    template_name = 'profiles/profile_list.html'


class LoginAfterPasswordChangeView(PasswordChangeView):

    @property
    def success_url(self):
        return reverse_lazy('password_changed_ok')

login_after_password_change = login_required(LoginAfterPasswordChangeView.as_view())


def password_changed_ok(request):
    return render_to_response("iddacultura/password_changed_ok.html", context_instance=RequestContext(request))

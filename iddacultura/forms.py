# -*- coding: utf-8 -*-

from registration.forms import RegistrationFormUniqueEmail
from django.forms import ModelForm
from django import forms
from iddacultura.models import User, UserProfile
from captcha.fields import ReCaptchaField
import settings
from django.core.exceptions import ImproperlyConfigured


class UserRegistrationForm(RegistrationFormUniqueEmail):
    """
    Extende o formulário de registro de usuário para
    mais campos.
    """

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        if not settings.RECAPTCHA_PUBLIC_KEY or not settings.RECAPTCHA_PRIVATE_KEY:
            raise ImproperlyConfigured('É necessário definir as chaves do ReCaptcha no settings_local.py')

    username = forms.RegexField(label="Usuário", max_length=75,regex=r"^[\w.@+-]+$",
                                help_text="Utilize apenas letras e número sem espaços")

    first_name = forms.CharField(label="Nome", help_text='',)
    last_name = forms.CharField(label="Sobrenome", help_text='')
    captcha = ReCaptchaField(attrs={'theme': 'white'})


class UserPublicForm(ModelForm):
    """
    Extende o formulário de edição do perfil do usuário
    para adicionar os campos que são padrão do Django. Utilizado
    apenas na interface pública de edição do perfil.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

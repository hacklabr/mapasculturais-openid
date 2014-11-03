# -*- coding: utf-8 -*-

from django import forms

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from allauth.account.forms import SignupForm

from captcha.fields import ReCaptchaField

recaptcha_not_setup_message = 'É necessário definir as chaves do ReCaptcha no settings_local.py'


class OpenIDSignupForm(SignupForm):
    """
    Extende o formulário de registro de usuário para
    mais campos.
    """

    username = forms.RegexField(label="Usuário", max_length=75, regex=r"^[\w.@+-]+$",
                                help_text="Utilize apenas letras e número sem espaços")

    first_name = forms.CharField(label="Nome", help_text='',)
    last_name = forms.CharField(label="Sobrenome", help_text='')

    captcha = ReCaptchaField(attrs={'theme': 'white'})

    def __init__(self, *args, **kwargs):
        super(OpenIDSignupForm, self).__init__(*args, **kwargs)

        if not (settings.RECAPTCHA_PUBLIC_KEY and settings.RECAPTCHA_PRIVATE_KEY):
            raise ImproperlyConfigured(recaptcha_not_setup_message)

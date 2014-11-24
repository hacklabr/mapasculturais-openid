# -*- coding: utf-8 -*-

from django import forms
from allauth.account.forms import SignupForm
from captcha.fields import ReCaptchaField


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

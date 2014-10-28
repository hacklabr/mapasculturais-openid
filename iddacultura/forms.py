# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from allauth.account.forms import SignupForm
from captcha.fields import ReCaptchaField


class OpenIDSignupForm(SignupForm):
    """
    Extende o formulário de registro de usuário para
    mais campos.
    """

    captcha = ReCaptchaField(attrs={'theme': 'white'})

    def __init__(self, *args, **kwargs):
        super(OpenIDSignupForm, self).__init__(*args, **kwargs)

        if not (settings.RECAPTCHA_PUBLIC_KEY and settings.RECAPTCHA_PRIVATE_KEY):
            raise ImproperlyConfigured('É necessário definir as chaves do ReCaptcha no settings_local.py')

# class UserPublicForm(ModelForm):
#     """
#     Extende o formulário de edição do perfil do usuário
#     para adicionar os campos que são padrão do Django. Utilizado
#     apenas na interface pública de edição do perfil.
#     """

#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')

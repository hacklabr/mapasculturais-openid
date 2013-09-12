# -*- coding: utf-8 -*-

import re
from registration.forms import RegistrationForm
from django.contrib.localflavor.br.forms import BRCPFField
from django.forms import ModelForm, ValidationError
from django import forms
from iddacultura.models import User, UserProfile


class BRCPFFieldUnique(BRCPFField):
    """
    Extende a classe BRCPFField para forçar valores
    únicos para o CPF e também para sempre salvar apenas
    os números na base de dados sem pontos e hífem.

    Usado no UserRegistrationForm que não extende o ModelForm
    e por isso ignora o fato do campo cpf estar marcado como único.
    """

    def clean(self, value):
        # remove pontos e hífem do cpf
        value = re.sub("[-\.]", "", value)

        super(BRCPFFieldUnique, self).clean(value)

        # gera um erro se já houver um cpf com o mesmo valor na base de dados
        if UserProfile.objects.filter(cpf=value).exists():
            raise ValidationError(
                'Já existe um usuário cadastrado com este CPF.')

        return value


class UserRegistrationForm(RegistrationForm):
    """
    Extende o formulário de registro de usuário para
    mais campos.
    """

    first_name = forms.CharField(label="Nome", help_text='',)
    last_name = forms.CharField(label="Sobrenome", help_text='')
    cpf = BRCPFFieldUnique(label="CPF")


class UserProfileForm(ModelForm):
    """
    Extende o formulário de edição do perfil do usuário
    para customizar o comportamento dos campos relacionados
    a ocupação do usuário. Usado no admin como na interface pública
    de edição do perfil do usuário.
    """

    cpf = BRCPFField(label="CPF")


class UserProfilePublicForm(UserProfileForm):
    """
    Extende o formulário de edição do perfil do usuário
    para adicionar os campos que são padrão do Django. Utilizado
    apenas na interface pública de edição do perfil.
    """

    def __init__(self, *args, **kwargs):
        super(UserProfilePublicForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

            self.fields.keyOrder = ['first_name', 'last_name', 'email', 'cpf',
                'trusted_roots']
        except User.DoesNotExist:
            pass

    first_name = forms.CharField(label="Nome", help_text='',)
    last_name = forms.CharField(label="Sobrenome", help_text='')
    email = forms.EmailField(label="E-mail", help_text='')

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def save(self, *args, **kwargs):
        """
        Salva também as informações padrão de um usuário quando salva
        os campos extra do perfil.
        """

        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(UserProfileForm, self).save(*args, **kwargs)

        return profile

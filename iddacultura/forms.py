#coding: utf-8

from registration.forms import RegistrationForm
from django.contrib.localflavor.br.forms import BRCPFField
from django.forms import ModelForm
from django import forms
from iddacultura.models import User, UserProfile

class UserRegistrationForm(RegistrationForm):
    """
    Extende o formulário de registro de usuário para
    adicionar o campo CPF
    """
    
    cpf = BRCPFField()
    

class UserProfileForm(ModelForm):
    """
    Extende o formulário de edição do perfil do usuário
    para adicionar os campos que são padrão do Django.
    """
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass
 
    first_name = forms.CharField(label="Nome",help_text='')
    last_name = forms.CharField(label="Sobrenome",help_text='')
    email = forms.EmailField(label="E-mail",help_text='')
 
    class Meta:
        model = UserProfile
        exclude = ('user',)        
 
    def save(self, *args, **kwargs):
        """
        Update the primary email address on the related User object as well.
        """
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(UserProfileForm, self).save(*args,**kwargs)
        return profile
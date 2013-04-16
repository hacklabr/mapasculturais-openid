# -*- coding: utf-8 -*-

from registration.forms import RegistrationForm
from django.contrib.localflavor.br.forms import BRCPFField
from django.forms import ModelForm
from django import forms
from iddacultura.models import User, UserProfile, UserOccupation

class UserProfileBaseForm(object):
    """
    Funcionalidade básico do formulário com o perfil do 
    usuário compartilhada pelo formulário de registro do usuário
    e pelo formulário de edição do perfil do usuário
    """
    
    def __init__(self, *args, **kwargs):
        super(UserProfileBaseForm, self).__init__(*args, **kwargs)

        try:
            self.populate_occupation_options(kwargs, 'user_occupation_secondary', 'user_occupation_primary')
            self.populate_occupation_options(kwargs, 'user_occupation_tertiary', 'user_occupation_secondary')
            self.populate_occupation_options(kwargs, 'user_occupation_quartenary', 'user_occupation_tertiary')
            self.populate_occupation_options(kwargs, 'user_occupation_quinary', 'user_occupation_quartenary')
            
            # adicionar a classe 'user_occupation' para todos os campos relacionados com a ocupação do usuário
            for key, field in self.fields.iteritems():
                if 'user_occupation_' in key:
                    field.widget.attrs['class'] = 'user_occupation'
        except User.DoesNotExist:
            pass
    
    def populate_occupation_options(self, kwargs, field, parent_field):
        """
        Define as opções disponíveis para cada um dos campos
        de ocupação que o usuário precisa escolher (do segundo nível
        ao quinto nível).
        """
        
        if kwargs.has_key('data') and kwargs['data'].has_key(field):
            child = UserOccupation.objects.get(pk = kwargs['data'][field])
            self.fields[field].choices = [(o.id, str(o)) for o in UserOccupation.objects.filter(parent = child.parent)]
            self.fields[field].initial = kwargs['data'][field]
        elif kwargs.has_key('instance') and getattr(kwargs['instance'], parent_field):
            self.fields[field].choices = [(o.id, str(o)) for o in UserOccupation.objects.filter(parent = getattr(kwargs['instance'], parent_field).code)]
        else:
            self.fields[field].widget.attrs['disabled'] = 'disabled'


class UserRegistrationForm(UserProfileBaseForm, RegistrationForm):
    """
    Extende o formulário de registro de usuário para
    adicionar o campo CPF
    """
    
    first_name = forms.CharField(label="Nome", help_text='',)
    last_name = forms.CharField(label="Sobrenome", help_text='')
    cpf = BRCPFField(label = "CPF")
    choices = [(o.id, str(o)) for o in UserOccupation.objects.filter(type = 'primary')]
    choices.insert(0, (u'', 'Selecione'))
    user_occupation_primary = forms.ChoiceField(label = "Grande grupo", choices = choices)
    user_occupation_secondary = forms.ChoiceField(label = "Sub-grupo principal")
    user_occupation_tertiary = forms.ChoiceField(label = "Sub-grupo")
    user_occupation_quartenary = forms.ChoiceField(label = "Família")
    user_occupation_quinary = forms.ChoiceField(label = "Ocupação")
    

class UserProfileForm(UserProfileBaseForm, ModelForm):
    """
    Extende o formulário de edição do perfil do usuário
    para customizar o comportamento dos campos relacionados
    a ocupação do usuário. Usado no admin como na interface pública
    de edição do perfil do usuário.
    """

    cpf = BRCPFField(label = "CPF")

    
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
            
            self.fields.keyOrder = [
                'first_name', 'last_name', 'email', 'cpf', 'trusted_roots', 'user_occupation_primary',
                'user_occupation_secondary', 'user_occupation_tertiary', 'user_occupation_quartenary',
                'user_occupation_quinary'
            ]
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
        profile = super(UserProfileForm, self).save(*args,**kwargs)
        
        return profile

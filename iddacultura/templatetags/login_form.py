from django import template
from django.contrib.auth.forms import AuthenticationForm
register = template.Library()

@register.inclusion_tag('iddacultura/login_form.html', takes_context = True)
def login_form(context):
    data = {}
    
    if context.has_key('form'):
        data['form'] = context['form']
    else:
        data['form'] = AuthenticationForm 
    
    if context.has_key('next'):
        data['next'] = context['next']
        
    return data
from django import template
from django.contrib.auth.forms import AuthenticationForm
register = template.Library()


@register.inclusion_tag('iddacultura/login_form.html', takes_context=True)
def login_form(context):
    data = {}

    if 'form' in context:
        data['form'] = context['form']
    else:
        data['form'] = AuthenticationForm

    if 'next' in context:
        data['next'] = context['next']

    return data

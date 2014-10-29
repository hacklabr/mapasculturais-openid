from django import template
from iddacultura.forms import LoginForm
register = template.Library()


@register.inclusion_tag('iddacultura/login_form.html', takes_context=True)
def login_form(context):
    data = {}

    if 'form' in context:
        data['form'] = context['form']
    else:
        data['form'] = LoginForm

    if 'next' in context:
        data['next'] = context['next']

    return data

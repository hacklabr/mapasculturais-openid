from django import template
from iddacultura.forms import OpenIDSignupForm
register = template.Library()


@register.inclusion_tag('iddacultura/registration_form.html', takes_context=True)
def registration_form(context):
    data = {}

    if 'form' in context:
        data['form'] = context['form']
    else:
        data['form'] = OpenIDSignupForm

    if 'next' in context:
        data['next'] = context['next']

    return data

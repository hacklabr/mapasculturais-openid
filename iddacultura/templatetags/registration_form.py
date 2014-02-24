from django import template
from registration.forms import RegistrationForm
register = template.Library()


@register.inclusion_tag('iddacultura/registration_form.html', takes_context=True)
def registration_form(context):
    data = {}

    if 'form' in context:
        data['form'] = context['form']
    else:
        data['form'] = RegistrationForm

    if 'next' in context:
        data['next'] = context['next']

    return data



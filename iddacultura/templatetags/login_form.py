from django import template
from django.contrib.auth.forms import AuthenticationForm
register = template.Library()

@register.inclusion_tag('iddacultura/login_form.html')
def login_form():
    return { 'form': AuthenticationForm }
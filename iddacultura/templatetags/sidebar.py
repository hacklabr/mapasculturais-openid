from django import template
from django.core.urlresolvers import reverse
register = template.Library()


@register.inclusion_tag('iddacultura/sidebar.html', takes_context=True)
def sidebar(context, path):
    data = {}

    data['path'] = path
    data['homepage'] = reverse('homepage')
    data['viewprofile'] = reverse(
        'profiles.views.profile_detail',
        args=[context['user']]
    )
    data['editprofile'] = reverse('profiles.views.edit_profile')
    data['chpassword'] = reverse('django.contrib.auth.views.password_change')

    if 'user' in context:
        data['user'] = context['user']

    return data

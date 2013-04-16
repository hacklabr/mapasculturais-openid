from django import template
register = template.Library()

@register.inclusion_tag('iddacultura/sidebar.html', takes_context = True)
def sidebar(context):
    data = {}
    
    if context.has_key('user'):
        data['user'] = context['user']
        
    return data
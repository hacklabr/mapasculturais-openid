from django.conf import settings

def bootstrap_files(request):
    return {
        'BOOTSTRAP_CSS_URL': settings.BOOTSTRAP_CSS_URL,
        'BOOTSTRAP_JS_URL': settings.BOOTSTRAP_JS_URL
    }
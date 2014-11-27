# Django settings for iddacultura project.

import os
from os.path import abspath, basename, dirname, join
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

DJANGO_ROOT = dirname(dirname(abspath(__file__)))
SITE_ROOT = dirname(DJANGO_ROOT)
SITE_ID = 1  # will change based on domain

#
# Theme related options
#
THEMES_DIR = join(SITE_ROOT, 'themes')
THEME = os.getenv('THEME', 'default')  # don't forget to re-run collectstatic if you change the theme


DEBUG = False
TEMPLATE_DEBUG = DEBUG

RECAPTCHA_PUBLIC_KEY = get_env_setting('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = get_env_setting('RECAPTCHA_PRIVATE_KEY')


ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USERNAME_BLACKLIST = ['edit', ]
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SIGNUP_FORM_CLASS = 'iddacultura.forms.OpenIDSignupForm'
OPENID_FAILED_DISCOVERY_AS_VALID = True

SOCIALACCOUNT_QUERY_EMAIL = True

LOGIN_REDIRECT_URL = '/user_profile/'

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Admin Name', 'admin@email.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'base.db',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-BR'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = join(SITE_ROOT, '../static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(THEMES_DIR, THEME, 'static'),
    os.path.join(THEMES_DIR, 'default', 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hd9w^uun(3$7$c_btdg49ni(k57ul&amp;e+(r931g)p4y5%ls=(9p'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'iddacultura.middleware.MultiSiteMiddleware',
)

ROOT_URLCONF = 'iddacultura.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'iddacultura.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(THEMES_DIR, THEME, 'templates'),
    os.path.join(THEMES_DIR, 'default', 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'absolute.context_processors.absolute',
    'django.contrib.messages.context_processors.messages',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
    'iddacultura.context_processors.site_data',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.admin',
    'iddacultura',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'braces',
    'captcha',
    'absolute',
    'openid_provider',
    'django_extensions',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


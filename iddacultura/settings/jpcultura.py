# coding: utf-8

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'openid-staging',
    }
}

STATIC_ROOT = join(SITE_ROOT, '../webfiles-jpcultura/static/')


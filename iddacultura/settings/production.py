# coding: utf-8

from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = get_env_setting('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'openid',
    }
}

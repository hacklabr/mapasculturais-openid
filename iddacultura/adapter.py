# coding: utf-8

from django.core.exceptions import ImproperlyConfigured
from django.db.models import FieldDoesNotExist
from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import _generate_unique_username_base, get_user_model
from allauth.account.utils import user_username, user_email, user_field
from allauth.account.app_settings import USER_MODEL_USERNAME_FIELD


def generate_unique_username(txts):

    username = _generate_unique_username_base(txts)
    User = get_user_model()
    try:
        max_length = User._meta.get_field(USER_MODEL_USERNAME_FIELD).max_length
    except FieldDoesNotExist:
        raise ImproperlyConfigured(
            "USER_MODEL_USERNAME_FIELD does not exist in user-model"
        )
    i = 0
    while True:
        try:
            if i:
                pfx = str(i + 1)
            else:
                pfx = ''
            ret = username[0:max_length - len(pfx)] + pfx
            query = {USER_MODEL_USERNAME_FIELD + '__exact': ret}
            User.objects.get(**query)
            i += 1
        except User.DoesNotExist:
            return ret


class MapasAccountAdapter(DefaultAccountAdapter):

    def populate_username(self, request, user):
        """
        Fills in a valid username, if required and missing.  If the
        username is already present it is assumed to be valid
        (unique).
        """
        first_name = user_field(user, 'first_name')
        last_name = user_field(user, 'last_name')
        email = user_email(user)
        username = user_username(user)
        if USER_MODEL_USERNAME_FIELD:
            user_username(user,
                          username
                          or generate_unique_username([first_name,
                                                       last_name,
                                                       email,
                                                       'user']))

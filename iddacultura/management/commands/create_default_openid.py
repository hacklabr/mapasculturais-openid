from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from openid_provider.models import OpenID

User = get_user_model()


class Command(BaseCommand):
    args = ''
    help = 'Add a default openID to all users'

    def handle(self, *args, **options):
        for user in User.objects.all():
            if not user.openid_set.filter(default=True).exists():
                oid = OpenID(user=user, default=True)
                oid.save()

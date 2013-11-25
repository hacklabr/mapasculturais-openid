# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from iddacultura.models import UserProfile


class UserProfileInline(admin.StackedInline):
    """
    Define an inline admin descriptor for UserProfile model
    which acts a bit like a singleton
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    """
    Define a new User admin
    """
    inlines = (UserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

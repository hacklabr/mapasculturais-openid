# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from iddacultura.models import UserProfile
from iddacultura.forms import UserProfileForm
from iddacultura.settings import STATIC_URL

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    form = UserProfileForm

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
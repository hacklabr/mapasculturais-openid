# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import TrustedRoot

User = get_user_model()

admin.site.register(User, UserAdmin)

admin.site.register(TrustedRoot)

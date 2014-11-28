from django.contrib import admin
from .models import SiteConfig


class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('site', 'default_name', 'org_name')
    search_fields = ('site', 'default_name', 'org_name')

admin.site.register(SiteConfig, SiteConfigAdmin)

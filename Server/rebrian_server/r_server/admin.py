from django.contrib import admin
from .models import *


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_add', 'date_update', 'description', 'client_is_active')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_editable = ('client_is_active',)
    list_filter = ('client_is_active', 'date_update')
    # fields = ('name', 'client_is_active', 'date_add', 'date_update')
    readonly_fields = ('date_add', 'date_update')
    save_on_top = True


admin.site.register(Client, ClientAdmin)

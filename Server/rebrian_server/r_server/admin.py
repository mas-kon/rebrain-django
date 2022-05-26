from django.contrib import admin
from .models import *


# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_add', 'date_update', 'description', 'client_is_active')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_editable = ('client_is_active',)
    list_filter = ('client_is_active', 'date_update')
    # fields = ('name', 'client_is_active', 'date_add', 'date_update')
    readonly_fields = ('date_add', 'date_update')
    save_on_top = True


# class DiskAdmin(admin.ModelAdmin):
#     list_display = ('id', 'device', 'client_id', 'client')
#     list_display_links = ('id', 'device')
#     search_fields = ('client', 'device')
#     list_filter = ('client',)
#     # fields = ('name', 'client_is_active', 'date_add', 'date_update')
#     # readonly_fields = ('date_add', 'date_update')
#     save_on_top = True
#
#
# class NetAdapterAdmin(admin.ModelAdmin):
#     list_display = ('id', 'client', 'net_adapter_device', 'IPv4')
#     list_display_links = ('id', 'net_adapter_device')
#     search_fields = ('client', 'net_adapter_device', 'IPv4')
#     list_filter = ('client', 'IPv4',)
#     save_on_top = True


admin.site.register(Client, ClientAdmin)
# admin.site.register(Disks, DiskAdmin)
# admin.site.register(NetAdapter, NetAdapterAdmin)

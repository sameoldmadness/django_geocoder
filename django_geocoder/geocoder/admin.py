from django.contrib import admin

from .models import (
    Provider, Request, Address, Geo
)

class ProviderAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'daily_request_limit')


class AddressInline(admin.TabularInline):
    model = Address


class RequestAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'first_address', 'address_count')
    inlines = (AddressInline,)


class GeoInline(admin.TabularInline):
    model = Geo
    readonly_fields = ('status', 'provider', 'latitude', 'longitude')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AddressAdmin(admin.ModelAdmin):
    list_display = ('text', 'request')
    inlines = (GeoInline,)


class GeoAdmin(admin.ModelAdmin):
    list_display = ('status', 'provider', 'latitude', 'longitude')


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Geo, GeoAdmin)

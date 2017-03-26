from django.contrib import admin

from .models import (
    Provider, Request, Address, Geo
)

class ProviderAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'is_drained')


class AddressInline(admin.TabularInline):
    model = Address
    readonly_fields = ('text', 'yandex_coordinates', 'google_coordinates', 'osm_coordinates')
    show_change_link = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class RequestAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'address_count')
    inlines = (AddressInline,)


class GeoInline(admin.TabularInline):
    model = Geo
    readonly_fields = ('provider', 'status', 'latitude', 'longitude')
    show_change_link = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AddressAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'text', 'yandex_coordinates', 'google_coordinates', 'osm_coordinates')
    inlines = (GeoInline,)


class GeoAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'status', 'provider', 'latitude', 'longitude')


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Geo, GeoAdmin)

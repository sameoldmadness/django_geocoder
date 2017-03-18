from django.contrib import admin

from .models import (
    ApiProvider, ApiKey, ApiRequest, GeoRequest, Address, AddressInfo
)


admin.site.register(ApiProvider)
admin.site.register(ApiKey)
admin.site.register(ApiRequest)
admin.site.register(GeoRequest)
admin.site.register(Address)
admin.site.register(AddressInfo)

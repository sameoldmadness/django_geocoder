from django.db import models
from django.dispatch import receiver


class Provider(models.Model):
    YANDEX = 'YA'
    GOOGLE = 'GO'
    OSM = 'OS'
    VENDORS = (
        (YANDEX, 'Yandex.Maps'),
        (GOOGLE, 'Google Maps'),
        (OSM, 'OpenStreetMap'),
    )

    vendor = models.CharField(max_length=2, choices=VENDORS)
    daily_request_limit = models.IntegerField()
    key = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.get_vendor_display()


class Request(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    addresses = models.TextField()

    # def address_list(self):
    #     return self.addresses.splitlines()

    # def first_address(self):
    #     return self.address_list[0]

    # def address_count(self):
    #     return len(self.address_list)

    # def __str__(self):
    #     return '{}: {} (total: {})'.format(self.created_at, self.first_address, self.address_count)


@receiver(models.signals.post_save, sender=Request)
def create_addresses_for_request(sender, instance, **kwargs):
    if not kwargs['created']:
        return

    lines = [a.strip() for a in instance.addresses.splitlines()]
    providers = Provider.objects.all()

    for line in lines:
        address = Address(request=instance, text=line)
        address.save()

        for provider in providers:
            geo = Geo(address=address, provider=provider)
            geo.save()


class Address(models.Model):
    text = models.CharField(max_length=200)
    request = models.ForeignKey('Request', on_delete=models.CASCADE)

    def _coordinates_by_vendor(self, vendor):
        geo = self.geo_set.filter(provider__vendor=vendor)

        return (geo[0].latitude, geo[0].longitude) if len(geo) else None

    def yandex_coordinates(self):
        return self._coordinates_by_vendor(Provider.YANDEX)
    yandex_coordinates.short_description = 'Yandex'

    def google_coordinates(self):
        return self._coordinates_by_vendor(Provider.GOOGLE)
    google_coordinates.short_description = 'Google'

    def osm_coordinates(self):
        return self._coordinates_by_vendor(Provider.OSM)
    osm_coordinates.short_description = 'OSM'

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'addresses'


class Geo(models.Model):
    NEW = 0
    SUCCESS = 1
    ERROR = 2
    STATUSES = (
        (NEW, 'New'),
        (SUCCESS, 'Success'),
        (ERROR, 'Error'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUSES, default=NEW)

    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE)

    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)

    class Meta:
        verbose_name_plural = 'geo'

from datetime import date

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
    last_request_date = models.DateField(default=date.today)
    request_count = models.IntegerField(default=0)
    key = models.CharField(max_length=100, null=True, blank=True)

    def increment_request_count(self):
        if self.last_request_date == date.today():
            self.request_count += 1
        else:
            self.last_request_date = date.today()
            self.request_count = 1

    @property
    def is_drained(self):
        return (
            self.last_request_date == date.today() and
            self.request_count >= self.daily_request_limit
        )

    def __str__(self):
        return self.get_vendor_display()


class Request(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    addresses = models.TextField()

    @property
    def address_count(self):
        return len(self.addresses.splitlines())

    def __str__(self):
        return '{} ({} addresses)'.format(self.created_at.strftime('%y-%m-%d %H:%M'), self.address_count)


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
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)
    request = models.ForeignKey('Request', on_delete=models.CASCADE)

    def _coordinates_by_vendor(self, vendor):
        geo = self.geo_set.filter(provider__vendor=vendor)
        if len(geo) and geo[0].latitude and geo[0].longitude:
            return '{}, {}'.format(geo[0].latitude, geo[0].longitude)
        return ''

    @property
    def yandex_coordinates(self):
        return self._coordinates_by_vendor(Provider.YANDEX)

    @property
    def google_coordinates(self):
        return self._coordinates_by_vendor(Provider.GOOGLE)

    @property
    def osm_coordinates(self):
        return self._coordinates_by_vendor(Provider.OSM)

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

    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'geo'

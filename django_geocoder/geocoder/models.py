from django.db import models


class ApiProvider(models.Model):
    name = models.CharField(max_length=50)
    daily_request_limit = models.IntegerField()


class ApiKey(models.Model):
    key = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=True)
    api_provider = models.ForeignKey('ApiProvider', on_delete=models.CASCADE)


class ApiRequest(models.Model):
    NEW = 0
    SUCCESS = 1
    ERROR = 2
    STATUSES = (
        (NEW, 'New'),
        (SUCCESS, 'Success'),
        (ERROR, 'Error'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUSES, default=NEW)
    api_key = models.ForeignKey('ApiKey', on_delete=models.CASCADE)


class GeoRequest(models.Model):
    addresses = models.TextField()


class Address(models.Model):
    text = models.CharField(max_length=200)
    geo_request = models.ForeignKey('GeoRequest', on_delete=models.CASCADE)


class AddressInfo(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    api_key = models.ForeignKey('ApiKey', on_delete=models.CASCADE)

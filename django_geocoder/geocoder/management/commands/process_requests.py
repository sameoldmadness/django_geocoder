from django.core.management.base import BaseCommand, CommandError
from geocoder.models import Geo
from geocoder.services.api import Api

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def _ok(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def handle(self, *args, **options):
        geo_items = Geo.objects.filter(status=Geo.NEW)
        for geo in geo_items:
            self._ok(geo.address)
            api = Api.withProvider(geo.provider)
            # try:
            response = api.geocode(geo.address.text)
            # except Exception as e:
            #     # geo.status = geo.ERROR
            #     # geo.save()
            #     print('{}: {}'.format(type(e).__name__, e))
            #     continue
            geo.latitude = response['latitude']
            geo.longitude = response['longitude']
            geo.status = geo.SUCCESS
            geo.save()

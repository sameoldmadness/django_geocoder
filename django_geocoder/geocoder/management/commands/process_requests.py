from django.core.management.base import BaseCommand, CommandError
from geocoder.models import Geo
from geocoder.services.api import Api, ApiError

class Command(BaseCommand):
    help = 'Process pending geocode requests'

    def handle(self, *args, **options):
        geo_items = Geo.objects.filter(status=Geo.NEW)
        for geo in geo_items:
            api = Api.withProvider(geo.provider)
            try:
                response = api.geocode(geo.address.text)
            except ApiError as e:
                self.stderr.write('{}: {}'.format(type(e).__name__, e))
                geo.status = geo.ERROR
            else:
                geo.latitude = response['latitude']
                geo.longitude = response['longitude']
                geo.status = geo.SUCCESS
            finally:
                self.stdout.write(
                    'Successfully processed: "{}" for {}'
                        .format(geo.address.text, geo.provider))
                geo.save()

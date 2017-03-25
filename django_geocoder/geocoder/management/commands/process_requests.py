from django.core.management.base import BaseCommand, CommandError
from geocoder.models import Geo
from geocoder.services.api import Api, ApiError

class Command(BaseCommand):
    help = 'Process pending geocode requests'

    def handle(self, *args, **options):
        geo_items = Geo.objects.filter(status=Geo.NEW)
        skipped = {}
        for geo in geo_items:
            if geo.provider.is_drained:
                key = str(geo.provider)
                skipped[key] = skipped.get(key, 0) + 1
                continue
            geo.provider.increment_request_count()
            geo.provider.save()
            api = Api.withProvider(geo.provider)
            try:
                response = api.geocode(geo.address.text)
            except ApiError as e:
                self.stderr.write('{}: {}'.format(type(e).__name__, e))
                geo.status = geo.ERROR
                geo.save()
            else:
                self.stdout.write(
                    'Successfully processed: "{}" for {}'
                        .format(geo.address.text, geo.provider))
                geo.latitude = response['latitude']
                geo.longitude = response['longitude']
                geo.status = geo.SUCCESS
            finally:
                geo.save()
        if len(skipped):
            for provider, count in skipped.items():
                print('Drained: {} – (skipped {})'.format(provider, count))

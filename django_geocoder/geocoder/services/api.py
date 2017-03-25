import json
import requests

from geocoder.models import Provider


class ApiError(Exception):
    """Base class for exceptions in this module."""


class ResponseNotJsonError(ApiError):
    """Response does not contain JSON"""


class UnexpectedJsonStructure(ApiError):
    """Cannot find given key in JSON"""


class Api:
    def __init__(self, key):
        self._key = key

    def geocode(self, address):
        params = self._build_params(address)
        response = requests.get(self._url, params=params)
        try:
            response.raise_for_status()
            json_data = response.json()
            geo_data = self._extract_from_json(json_data)
        except requests.HTTPError:
            raise ApiError(
                'HTTP error',
                {'params': params,
                 'response': response.text,
                 'status': response.status_code})
        except json.decoder.JSONDecodeError:
            raise ResponseNotJsonError(
                'Response does not contain JSON',
                {'params': params,
                 'response': response.text})
        except KeyError as e:
            raise UnexpectedJsonStructure(
                'Cannot find given key in JSON',
                {'params': params,
                 'response': response.text,
                 'key': e.args[0]})
        return geo_data

    @staticmethod
    def withProvider(provider):
        if provider.vendor == Provider.YANDEX:
            return YandexApi(key=provider.key)
        if provider.vendor == Provider.GOOGLE:
            return YandexApi(key=provider.key)
        if provider.vendor == Provider.OSM:
            return OpenStreetMapApi(key=provider.key)
        raise NotImplemented('Unknown provider: {}'.format(provider.key))


class YandexApi(Api):
    _url = 'https://geocode-maps.yandex.ru/1.x'

    def _build_params(self, address):
        params = { 'geocode': address, 'format': 'json' }
        if self._key:
            params['key'] = self._key
        return params

    def _extract_from_json(self, json_data):
        latitude, longitude = json_data \
            ['response2']['GeoObjectCollection']['featureMember'][0] \
            ['GeoObject']['Point']['pos'].split()
        return { 'latitude': latitude, 'longitude': longitude }


class GoogleApi(Api):
    _url = 'https://maps.googleapis.com/maps/api/geocode/json'

    def _build_params(self, address):
        params = { 'address': address }
        if self._key:
            params['key'] = self._key
        return params

    def _extract_from_json(self, json_data):
        location = json_data['results']['geometry']['location']
        return { 'latitude': location['lat'], 'longitude': location['lng'] }


class OpenStreetMapApi(Api):
    _url = 'https://nominatim.openstreetmap.org/search'

    def _build_params(self, address):
        return { 'q': address, 'format': 'json' }

    def _extract_from_json(self, json_data):
        result = json_data[0]
        return { 'latitude': result['lat'], 'longitude': result['lon'] }

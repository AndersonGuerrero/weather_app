from unittest.mock import patch

from django.test import TestCase

from core.tests.helpers import (
    MockResponseWeatherStack,
    MockResponseWeatherStackError,
    MockResponseWeatherStackNotExist
)
from weather.services import WeatherStack
from weather.services.exceptions import WeatherStackError
from weather.constants import INVALID_QUERY, SERVICE_LIMIT_REACHED


class WeatherStackApiTestCase(TestCase):

    @patch(
        "weather.services.weatherstack.requests.get",
        MockResponseWeatherStack
    )
    def test_post_view(self):
        response = self.client.post(
            "/",
            {'street_address': 'Pereira, Colombia'}
        )
        self.assertTrue(response.status_code, 200)
        self.assertTrue('Humidity: 83%' in response.content.decode('utf-8'))

    @patch(
        "weather.services.weatherstack.requests.get",
        MockResponseWeatherStackError
    )
    def test_post_error(self):
        response = self.client.post(
            "/",
            {'street_address': 'Pereira, Colombia'}
        )
        self.assertTrue(response.status_code, 200)
        self.assertIn(SERVICE_LIMIT_REACHED, response.content.decode('utf-8'))

    @patch(
        "weather.services.weatherstack.requests.get",
        MockResponseWeatherStackNotExist
    )
    def test_query_error(self):
        response = self.client.post(
            "/",
            {'street_address': 'Pereira, Colombia'}
        )
        self.assertTrue(response.status_code, 200)
        self.assertIn(INVALID_QUERY, response.content.decode('utf-8'))

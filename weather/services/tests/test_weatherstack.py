from unittest.mock import patch

from django.test import TestCase

from weather.services import WeatherStack
from weather.services.exceptions import WeatherStackError
from weather.constants import INVALID_QUERY, SERVICE_LIMIT_REACHED
from core.tests.helpers import (
    MockResponseWeatherStack,
    MockResponseWeatherStackError,
    MockResponseWeatherStackNotExist
)


class WeatherStackApiTestCase(TestCase):

    @patch(
        "weather.services.weatherstack.requests.get",
        MockResponseWeatherStack
    )
    def test_get_data_success(self):
        service = WeatherStack()
        response = service.get_weather_by_location('Pereira, Colombia')
        keys = []
        if response:
            keys = response.keys()
        self.assertIn('location', keys)
        self.assertIn('current', keys)

    @patch(
        "weather.services.weatherstack.requests.get",
        MockResponseWeatherStackError
    )
    def test_usage_limit_reached(self):
        service = WeatherStack()
        try:
            service.get_weather_by_location('Pereira, Colombia')
        except Exception as e:
            self.assertTrue(isinstance(e, WeatherStackError))
            self.assertEqual(SERVICE_LIMIT_REACHED, e.msg)

    @patch(
        "weather.services.weatherstack.requests.get",
        MockResponseWeatherStackNotExist
    )
    def test_query_error(self):
        service = WeatherStack()
        try:
            service.get_weather_by_location('Pereira, Colombia')
        except Exception as e:
            self.assertTrue(isinstance(e, WeatherStackError))
            self.assertEqual(INVALID_QUERY, e.msg)

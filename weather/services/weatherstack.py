import logging

import requests
from django.conf import settings

from .exceptions import WeatherStackError
from weather.constants import INVALID_QUERY, SERVICE_LIMIT_REACHED


class WeatherStack():

    CODES_RETRY = [602, 601, 615]
    CODES_ACCESS_RESTRICTED = [104, 105, 102, 101, 101]

    def __init__(self):
        self.forecast_days = 1
        self.hourly = 0
        self.api_key = settings.WEATHERSTACK['API_KEY']
        self.base_url = settings.WEATHERSTACK['API_URL']
        self.default_message = (
            'At the moment we have an error to consult the weather'
        )

    def clear_data(self, data: dict):
        if data.get('forecast'):
            data['forecast'] = data['forecast'][
                list(data['forecast'].keys())[0]
            ]
        return data

    def get_weather_by_location(self, location: str):
        try:

            url = (
                f"{self.base_url}/forecast"
                f"?query={location}&access_key={self.api_key}"
            )
            response = requests.get(url)
            if response.status_code == 200:
                response_json = response.json()
                if response_json.get('success') is False:
                    error = response_json.get('error', {})
                    if error['code'] in self.CODES_RETRY:
                        raise WeatherStackError(INVALID_QUERY)
                    elif error['code'] in self.CODES_ACCESS_RESTRICTED:
                        logging.error(str(error))
                        raise WeatherStackError(SERVICE_LIMIT_REACHED)
                else:
                    return self.clear_data(response_json)
            else:
                logging.error(response.content)
                raise WeatherStackError(self.default_message)
        except requests.RequestException as e:
            logging.exception(e)
            raise WeatherStackError(self.default_message)

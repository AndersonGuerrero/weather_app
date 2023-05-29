import logging
from django.conf import settings

import requests
from .exceptions import WeatherStackError
from weather.constants import INVALID_QUERY, SERVICE_LIMIT_REACHED


class WeatherStack():

    CODES_RETRY = [602, 601, 615]
    CODES_ACCESS_RESTRICTED = [104, 105, 102, 101, 101]

    def __init__(self):
        self.api_key = settings.WEATHERSTACK['API_KEY']
        self.base_url = settings.WEATHERSTACK['API_URL']
        self.default_message = 'At the moment we have an error to consult the weather'

    def get_weather_by_location(self, location):
        try:

            url = (
                f"{self.base_url}/current"
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
                        logging.exception(str(error))
                        raise WeatherStackError(SERVICE_LIMIT_REACHED)
                else:
                    return response_json
            else:
                logging.error(response.content)
                raise WeatherStackError(self.default_message)
        except requests.RequestException as e:
            logging.exception(e)
            raise WeatherStackError(self.default_message)
class MockResponseWeatherStackNotExist:
    def __init__(self, url):
        self.status_code = 200

    def json(self):
        return {
            'success': False,
            'error': {
                'code': 615,
                'type': 'request_failed',
                'info': (
                    'Your API request failed. '
                    'Please try again or contact support.'
                )
            }
        }


class MockResponseWeatherStackError:
    def __init__(self, url):
        self.status_code = 200

    def json(self):
        return {
            "success": False,
            "error": {
                "code": 104,
                "type": "usage_limit_reached",
                "info": (
                    "Your monthly API request volume has been reached."
                    " Please upgrade your plan."
                )
            }
        }


class MockResponseWeatherStack:

    def __init__(self, url):
        self.status_code = 200

    def json(self):
        return {
            "request": {
                "type": "City",
                "query": "Pereira, Colombia",
                "language": "en",
                "unit": "m"
            },
            "location": {
                "name": "Pereira",
                "country": "Colombia",
                "region": "Risaralda",
                "lat": "4.813",
                "lon": "-75.696",
                "timezone_id": "America/Bogota",
                "localtime": "2023-05-28 18: 29",
                "localtime_epoch": 1685298540,
                "utc_offset": "-5.0"
            },
            "current": {
                "observation_time": "11: 29 PM",
                "temperature": 22,
                "weather_code": 116,
                "weather_icons": [
                    "https: //img.png"
                ],
                "weather_descriptions": [
                    "Partly cloudy"
                ],
                "wind_speed": 4,
                "wind_degree": 146,
                "wind_dir": "SSE",
                "pressure": 1017,
                "precip": 0.4,
                "humidity": 83,
                "cloudcover": 50,
                "feelslike": 25,
                "uv_index": 4,
                "visibility": 10,
                "is_day": "no"
            }
        }

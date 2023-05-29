import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from weather.forms import SearchWeatherForm
from weather.services import WeatherStack
from weather.services.exceptions import WeatherStackError


class WeatherView(TemplateView):
    template_name = "search.html"
    result_template = 'weather_result.html'

    def post(self, request, *args, **kwargs):
        response_content = "Street address is required"
        location_data = None
        error = False
        form = SearchWeatherForm(request.POST, request.FILES)
        if form.is_valid():
            weather_stack_service = WeatherStack()
            try:
                location_data = weather_stack_service.get_weather_by_location(
                    form.data.get('street_address')
                )
            except WeatherStackError as e:
                error = True
                response_content = str(e.msg)
            except Exception as e:
                error = True
                logging.exception(e)
                response_content = (
                    "We are having unknown problems but "
                    "we are already working to fix it"
                )
        return render(
            request,
            self.result_template,
            {
                'result': location_data,
                'error': error,
                'error_message': response_content,
            }
        )

from django import forms


class SearchWeatherForm(forms.Form):
    street_address = forms.CharField()

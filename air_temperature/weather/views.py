from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import WeatherForm
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
import requests
import logging

logger = logging.getLogger(__name__)
base_url = 'https://api.openweathermap.org/data/2.5/weather'
# Create your views here.
def index(request):
    return HttpResponse('it is hot today :(')

def weather_api(request):
    if request.method == 'GET':
        form = WeatherForm(request.GET or None)
        if form.is_valid():
            # getting inputs
            city = request.GET.get('city')
            lat = request.GET.get('lat')
            lon = request.GET.get('lon')
            zip_code = request.GET.get('zip')

            # Construct the API based on the input type
            if city:
                url = f'{base_url}?q={city}&appid={settings.OPENWEATHER_API_KEY}&units=metric'
            elif lat and lon:
                url = f'{base_url}?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=metric'
            elif zip_code:
                url = f'{base_url}?zip={zip_code}&appid={settings.OPENWEATHER_API_KEY}&units=metric'

            # #make the api request
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logger.error(f'API request failed: {e}')
                return render(request, 'weather/weather.html', {
                    'form': form,
                    'error': 'Failed to fetch weather data, Please try again later',
                })

            weather_data = response.json()
            # extract relevant data
            weather = {
                'city': weather_data.get('name'),
                'temperature': weather_data.get('main', {}).get('temp'),
                'description': weather_data.get('weather', [{}])[0].get('description'),
                'icon': weather_data.get('weather', [{}])[0].get('icon'),
            }
            return render(request, 'weather/weather.html', {
                'form': form,
                'weather': weather,
            })
        else:
            return render(request, 'weather/weather.html', {
                'form': form,
            })
    else:
        form = WeatherForm()
        return render(request, 'weather/weather.html', {
            'form': form,
        })


def get_location(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
    
    url = f'https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={settings.OPENCAGE_API_KEY}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return JsonResponse(data)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to fetch location data'}, status=500)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return 

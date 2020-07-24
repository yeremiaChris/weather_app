import requests
from django.shortcuts import render

from .models import City

from . forms import CityForm

# Create your views here.

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=8a66d8ec5b914be58e7c1d49556e7a2f'
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        
        city_weather = {
            'city':city.name,
            'temperature':r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)


    context = {
        'weather_data': weather_data,
        'form': form
    }

    return render(request,'weather/weather.html',context)

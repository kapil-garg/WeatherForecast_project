from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from django.http import HttpResponse


# Create your views here.
def index(request):
    if request.method == 'POST':  # only true if form is submitted
        form = CityForm(request.POST)  # add actual request data to form for processing
        form.save()  # will validate and save if validate
    form = CityForm()
    # url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=8d7b4448afd0e144840e5e36b66830f2'


    url = 'https://api.weatherapi.com/v1/current.json?key=64749f2031694f0693d115913200611&q={}'
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        if city_weather is not None:
            weather = {
                'city': city_weather['location']['name'],
                'temperature': city_weather['current']['temp_c'],
                'description': city_weather['current']['condition']['text'],
                'icon': city_weather['current']['condition']['icon'],
                'region': city_weather['location']['region'],
                'country': city_weather['location']['country'],
                'wind_speed': city_weather['current']['wind_kph']
            }
            print("weather per city")
            print(weather)
            print()
            weather_data.append(weather)
    weather_data.reverse()
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'WeatherApp/index.html', context)


import requests
from config import open_weather_token
from .forms import CityForm
from django.shortcuts import render
from datetime import datetime

class WeatherData:
    WEATHER_TRANSLATIONS = {
        "thunderstorm with light rain": "Гроза с небольшим дождем",
        "thunderstorm with rain": "Гроза с дождем",
        "thunderstorm with heavy rain": "Гроза с сильным дождем",
        "light thunderstorm": "Слабая гроза",
        "thunderstorm": "Гроза",
        "heavy thunderstorm": "Сильная гроза",
        "ragged thunderstorm": "Неравномерная гроза",
        "thunderstorm with light drizzle": "Гроза с легким моросящим дождем",
        "thunderstorm with drizzle": "Гроза с моросящим дождем",
        "thunderstorm with heavy drizzle": "Гроза с сильным моросящим дождем",
        "light intensity drizzle": "Слабая морось",
        "drizzle": "Морось",
        "heavy intensity drizzle": "Сильная морось",
        "light intensity drizzle rain": "Слабый моросящий дождь",
        "drizzle rain": "Моросящий дождь",
        "heavy intensity drizzle rain": "Сильный моросящий дождь",
        "shower rain and drizzle": "Ливень и моросящий дождь",
        "heavy shower rain and drizzle": "Сильный ливень и моросящий дождь",
        "shower drizzle": "Ливневая морось",
        "light rain": "Легкий дождь",
        "moderate rain": "Умеренный дождь",
        "heavy intensity rain": "Сильный дождь",
        "very heavy rain": "Очень сильный дождь",
        "extreme rain": "Экстремальный дождь",
        "freezing rain": "Ледяной дождь",
        "light intensity shower rain": "Слабый ливневый дождь",
        "shower rain": "Ливневый дождь",
        "heavy intensity shower rain": "Сильный ливневый дождь",
        "ragged shower rain": "Неравномерный ливневый дождь",
        "light snow": "Легкий снег",
        "snow": "Снег",
        "heavy snow": "Сильный снег",
        "sleet": "Дождь со снегом",
        "light shower sleet": "Слабый ливневый дождь со снегом",
        "shower sleet": "Ливневый дождь со снегом",
        "light rain and snow": "Легкий дождь и снег",
        "rain and snow": "Дождь и снег",
        "light shower snow": "Слабый ливневый снег",
        "shower snow": "Ливневый снег",
        "heavy shower snow": "Сильный ливневый снег",
        "mist": "Дымка",
        "smoke": "Дым",
        "haze": "Мгла",
        "sand/dust whirls": "Песчаные/пыльные вихри",
        "fog": "Туман",
        "sand": "Песок",
        "dust": "Пыль",
        "volcanic ash": "Вулканический пепел",
        "squalls": "Шквалы",
        "tornado": "Торнадо",
        "clear sky": "Ясное небо",
        "few clouds": "Небольшие облака",
        "scattered clouds": "Рассеянные облака",
        "broken clouds": "Разорванные облака",
        "overcast clouds": "Пасмурные облака"
    }
    
    WEATHER_CONDITIONS  = {
        "Thunderstorm": "Гроза",
        "Drizzle": "Морось",
        "Rain": "Дождь",
        "Snow": "Снег",
        "Atmosphere": "Атмосферные явления",
        "Clear": "Ясная погода",
        "Clouds": "Облачность"
    }
    
    WIND_DIRECTIONS = {
        0: 'Северный ветер',
        90: 'Восточный ветер',
        180: 'Южный ветер',
        270: 'Западный ветер',
        360: 'Северный ветер',
    }
    
    def __init__(self) -> None:
        self.city = None
        self.latitude = None
        self.longitude = None
        self.clouds = None
        self.feels_like = None
        self.ground_level = None
        self.sea_level = None
        self.humidity = None
        self.pressure = None
        self.temperature = None
        self.min_temperature = None
        self.max_temperature = None
        self.country = None
        self.sunrise = None
        self.sunset = None
        self.timezone = None
        self.visibility = None
        self.description = None
        self.weather_conditions = None
        self.wind_deg = None
        self.wind_direction = None
        self.wind_gust = None
        self.wind_speed = None
        self.city_not_found = False
    
    @staticmethod
    def get_weather_data(city: str, token: str):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Encoding": "*",
            "Connection": "keep-alive"
        }
        return requests.get(url).json()        

    @classmethod
    def translate_description(cls, description: str):
        return cls.WEATHER_TRANSLATIONS.get(description, description)
    
    @classmethod
    def translate_conditions(cls, conditions: str):
        return cls.WEATHER_CONDITIONS.get(conditions, conditions)

    @classmethod
    def get_wind_direction(cls, deg: int):
        if deg in cls.WIND_DIRECTIONS:
            return cls.WIND_DIRECTIONS[deg]
        elif 0 < deg < 90:
            return 'Северо-восточный ветер'
        elif 90 < deg < 180:
            return 'Юго-восточный ветер'
        elif 180 < deg < 270:
            return 'Юго-западный ветер'
        elif 270 < deg < 360:
            return 'Северо-западный ветер'
        return None

def weather_page(request):
    context = {}
    form = CityForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        city = form.cleaned_data['city']
        data = WeatherData.get_weather_data(city, open_weather_token)

        if data.get('cod') == '404':
            context["city_not_found"] = True
        else:
            context = {
                'city': city,
                'clouds': data.get('clouds', {}).get('all'),
                'latitude': data.get('coord', {}).get('lat'),
                'longitude': data.get('coord', {}).get('lon'),
                'feels_like': data.get('main', {}).get('feels_like'),
                'ground_level': data.get('main', {}).get('grnd_level'),
                'sea_level': data.get('main', {}).get('sed_level'),
                'humidity': data.get('main', {}).get('humidity'),
                'pressure': data.get('main', {}).get('pressure'),
                'temperature': data.get('main', {}).get('temp'),
                'min_temperature': data.get('main', {}).get('temp_min'),
                'max_temperature': data.get('main', {}).get('temp_max'),
                'country': data.get('sys', {}).get('country'),
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
                'timezone': f"UTC {'+' if data['timezone'] >= 0 else '-'}{int(abs(data['timezone']) / 3600)}",
                'visibility': data.get('visibility') / 1000,
                'description': WeatherData.translate_description(data['weather'][0]['description']),
                'weather_conditions': WeatherData.translate_conditions(data['weather'][0]['main']),
                'wind_deg': data.get('wind', {}).get('deg'),
                'wind_direction': WeatherData.get_wind_direction(data.get('wind', {}).get('deg')),
                'wind_gust': data.get('wind' ,{}).get('gust'),
                'wind_speed':  data.get('wind', {}).get('speed'),
            }
    context['form'] = form
    return render(request, 'index.html', context)
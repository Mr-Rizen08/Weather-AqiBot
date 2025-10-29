import requests

def get_weather(city):
    parameters = {
        'appid': 'Your_Api',
        'units': 'metric',
        'lang': 'ru'
    }
    parameters["q"] = city
    data = requests.get('https://api.openweathermap.org/data/2.5/weather', params=parameters).json()
    return data

def get_aqi(lon, lat):
    airdata  = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid=Your_Api').json()
    return airdata

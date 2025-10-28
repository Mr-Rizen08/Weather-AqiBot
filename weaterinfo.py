import requests

def get_weather(city):
    parameters = {
        'appid': '#',
        'units': 'metric',
        'lang': 'ru'
    }
    parameters["q"] = city
    data = requests.get('https://api.openweathermap.org/data/2.5/weather', params=parameters).json()
    return data


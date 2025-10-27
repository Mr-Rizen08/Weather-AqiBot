import requests

def get_weater(city):
    parameters = {
        'appid': 'eb8269f63e5bee7531ddcc348bac701f',
        'units': 'metric',
        'lang': 'ru'
    }
    parameters["q"] = city
    data = requests.get('https://api.openweathermap.org/data/2.5/weather', params=parameters).json()
    return data

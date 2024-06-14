import requests
from datetime import datetime

def get_weather(city):
    API_KEY = 'ed7eb50b2d1d8ed53e4627829cf38ee2'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    try:
        status = requests.get(url).json()
        print(status)
        data = status['weather'][0]['description']
        temperature = round(status['main']['temp'] - 273.15, 1)
        min_temp = round(status['main']['temp_min'] - 273.15, 1)
        max_temp = round(status['main']['temp_max'] - 273.15, 1)
        humidity = status['main']['humidity']
        sunrise_unix = status['sys']['sunrise']
        sunrise_time = datetime.fromtimestamp(sunrise_unix).strftime('%H:%M')
        return data, temperature, min_temp, max_temp, sunrise_time, humidity
        # return data
    except Exception as e:
        return None

if __name__ == "__main__":
    city = input()
    get_weather(city)

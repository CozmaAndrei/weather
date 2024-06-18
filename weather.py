import requests
from datetime import datetime
from decouple import config

def get_weather(city):
    API_KEY = config('API_KEY_get_weather')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    try:
        status = requests.get(url).json()
        data = status['weather'][0]['description']
        temperature = round(status['main']['temp'] - 273.15, 1)
        min_temp = round(status['main']['temp_min'] - 273.15, 1)
        max_temp = round(status['main']['temp_max'] - 273.15, 1)
        humidity = status['main']['humidity']
        sunrise_unix = status['sys']['sunrise']
        sunrise_time = datetime.fromtimestamp(sunrise_unix).strftime('%H:%M')
        day = status['dt']
        actual_day = datetime.fromtimestamp(day).strftime('%A')
        return data, temperature, min_temp, max_temp, sunrise_time, humidity, actual_day
    except Exception:
        return None

# if __name__ == "__main__":
#     city = input()
#     get_weather(city)

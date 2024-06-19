import requests, pytz
from datetime import datetime
from decouple import config
from timezonefinder import TimezoneFinder

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
        day = status['dt']
        actual_day = datetime.fromtimestamp(day).strftime('%A')
        return data, temperature, min_temp, max_temp, humidity, actual_day
    except Exception:
        return None

def get_sunrise_and_sunset(city):
    API_KEY = config('API_KEY_get_weather')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    try:
        status = requests.get(url).json()
        sunrise_unix = status['sys']['sunrise']
        sunset_unix = status['sys']['sunset']
        lat = status['coord']['lat']
        lon = status['coord']['lon']
        daytime = status['dt']
        actual_time = datetime.fromtimestamp(daytime).strftime('%H:%M')
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        if timezone_str is None:
            print("Could not determine timezone.")
            return None
        local_timezone = pytz.timezone(timezone_str)
        sunrise_utc = datetime.fromtimestamp(sunrise_unix)
        sunset_utc = datetime.fromtimestamp(sunset_unix)
        sunrise_time = sunrise_utc.astimezone(local_timezone).strftime('%H:%M')
        sunset_time = sunset_utc.astimezone(local_timezone).strftime('%H:%M')
        return sunrise_time, sunset_time, actual_time
    except Exception:
        return None
    
if __name__ == "__main__":
    city = input()
    get_weather(city)
    get_sunrise_and_sunset(city)

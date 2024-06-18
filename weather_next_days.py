import requests
from datetime import datetime, timedelta
from decouple import config

def get_weather_next_days(city):
    API_KEY = config('API_KEY_get_weather')
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
    try:
        status = requests.get(url).json()
        data = status['list'][1]['weather'][0]['description']
        day1 = status['list'][8]['dt']
        day2 = status['list'][16]['dt']
        day3 = status['list'][24]['dt']
        latitude = status['city']['coord']['lat']
        longitude = status['city']['coord']['lon']
        
        day1 = datetime.fromtimestamp(day1).strftime('%A')
        day2 = datetime.fromtimestamp(day2).strftime('%A')
        day3 = datetime.fromtimestamp(day3).strftime('%A')
        # date = datetime.fromtimestamp(day1).strftime('%d-%m-%Y')
        # time = datetime.fromtimestamp(day1).strftime('%H:%M%S')
        
        return data, day1, day2, day3
    except Exception:
        return None
    
def get_min_temp_max_temp(city):
    API_KEY = config('API_KEY_get_weather')
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
    try:
        status = requests.get(url).json()
        the_time = datetime.now()
        actual_time = datetime.now().strftime('%H:%M')
        a_day_after = (the_time + timedelta(days=1)).strftime('%Y-%m-%d')
        two_days_after = (the_time + timedelta(days=2)).strftime('%Y-%m-%d')
        three_days_after = (the_time + timedelta(days=3)).strftime('%Y-%m-%d')
        
        min_temp_a_day_after = float('inf') # max inferior
        max_temp_a_day_after = float('-inf') # min inferior
        min_temp_two_days_after = float('inf')
        max_temp_two_days_after = float('-inf')
        min_temp_tree_days_after = float('inf')
        max_temp_tree_days_after = float('-inf')
        
        for entry in status['list']:
            dt = (datetime.fromtimestamp(entry['dt'])).strftime('%Y-%m-%d')
            temp_min = round(entry['main']['temp_min'] - 273.15, 1)
            temp_max = round(entry['main']['temp_max'] - 273.15, 1)
            
            if dt == a_day_after:
                min_temp_a_day_after = min(min_temp_a_day_after, temp_min)
                max_temp_a_day_after = max(max_temp_a_day_after, temp_max)
            elif dt == two_days_after:
                min_temp_two_days_after = min(min_temp_two_days_after, temp_min)
                max_temp_two_days_after = max(max_temp_two_days_after, temp_max)
            elif dt == three_days_after:
                min_temp_tree_days_after = min(min_temp_tree_days_after, temp_min)
                max_temp_tree_days_after = max(max_temp_tree_days_after, temp_max)
        
        return min_temp_a_day_after, max_temp_a_day_after, min_temp_two_days_after, max_temp_two_days_after, min_temp_tree_days_after, max_temp_tree_days_after
        
    except Exception:
        return None
    
# if __name__ == "__main__":
#     city = input()
#     get_weather_next_days(city)
#     get_min_temp_max_temp(city)
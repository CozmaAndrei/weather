import requests
from datetime import datetime, timedelta
from decouple import config

'''Return description and name of the next 3 days'''
def get_weather_next_days(city):
    API_KEY = config('API_KEY_get_weather')
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
    try:
        status = requests.get(url).json()
        data = status['list'][1]['weather'][0]['description']
        day1 = status['list'][8]['dt']
        day2 = status['list'][16]['dt']
        day3 = status['list'][24]['dt']
        
        day1_date = datetime.fromtimestamp(day1).strftime('%A, %d %B, %Y')
        day2_date = datetime.fromtimestamp(day2).strftime('%A, %d %B, %Y')
        day3_date = datetime.fromtimestamp(day3).strftime('%A, %d %B, %Y')

        return data, day1_date, day2_date, day3_date
    except Exception:
        return None

'''Return 3 lists with all temperatures for the next 3 days'''
def get_all_temps(city):
    API_KEY = config('API_KEY_get_weather')
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
    
    try:
        status = requests.get(url).json()
        current_time = datetime.now()
        a_day_after = (current_time + timedelta(days=1)).date() #date() return only date without hours.minutes.seconds
        two_days_after = (current_time + timedelta(days=2)).date()
        three_days_after = (current_time + timedelta(days=3)).date()
        a_day_after_temps = []
        two_days_after_temps = []
        three_days_after_temps = []
        
        for entry in status['list']:
            dt_txt = entry['dt_txt']
            dt = datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S').date() #date() return only date without hours.minutes.seconds
            temp = round(entry['main']['temp']- 273.15, 1)
            
            if dt == a_day_after:
                a_day_after_temps.append(temp)
                
            elif dt == two_days_after:
                two_days_after_temps.append(temp)
                
            elif dt == three_days_after:
                three_days_after_temps.append(temp)
        all_days_temps = a_day_after_temps + two_days_after_temps + three_days_after_temps  
        return all_days_temps
            
    except Exception:
        return None
    
# if __name__ == "__main__":
#     city = input()
#     get_all_temps(city)
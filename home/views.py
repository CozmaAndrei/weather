from django.shortcuts import render
from helper.weather import get_current_dates, get_sunrise_sunset_time
from helper.weather_next_days import get_weather_next_days, get_all_temps, get_all_descriptions, get_all_times
from .forms import SearchForm


'''This function return the weather conditions'''
def get_weather_conditions():
    weather_condition_sunny = {
        #img sun.png
        'clear sky': 'sunny', 
    }
    weather_condition_night = {
        #img moon.png
        'clear sky': 'night'
    }
    weather_condition_few_clouds = {
        #img day_sun_clouds.png(day) // img night_few_clouds.png(night)
        'few clouds': 'few_clouds',
        'scattered clouds': 'few_clouds',
    }
    weather_condition_clouds = {
        #img clouds.png(day) // img night_clouds.png(night)
        'overcast clouds': 'clouds',
        'broken clouds': 'clouds',
    }
    weather_condtion_light_rain = {
        #img light_rain.png(day) // light_rain.png(night)
        'light rain': 'rainy',
        'moderate rain': 'rainy',
    }
    weather_condition_rainy = {
        #img rain.png(day) // rain.png(night)
        'heavy intensity rain': 'rainy',
    }

    return {
        'weather_condition_sunny': weather_condition_sunny,
        'weather_condition_night': weather_condition_night,
        'weather_condition_few_clouds': weather_condition_few_clouds,
        'weather_condition_clouds': weather_condition_clouds,
        'weather_condtion_light_rain': weather_condtion_light_rain,
        'weather_condition_rainy': weather_condition_rainy,
    }
    
'''This function return data of cities dictionary'''  
def get_static_cities_weather():
    search_form = SearchForm()
    cities = {
        'bucharest': "Bucharest",
        'london': 'London',
        'madrid': 'Madrid',
        'paris': 'Paris',
        'berlin': 'Berlin',
        'copenhagen': 'Copenhagen',
    }
    weather_data = {}
    
    for key, city in cities.items():
        data = get_current_dates(city)
        get_actual_time = get_sunrise_sunset_time(city)
        weather_data[key] = {
            'weather': data[0] if data else None,
            'temperature': data[1] if data else None,
            'min_temp': data[2] if data else None,
            'max_temp': data[3] if data else None,
            'humidity': data[4] if data else None,
            
            'sunrise_time': get_actual_time[0] if get_actual_time else None,
            'sunset_time': get_actual_time[1] if get_actual_time else None,
            'actual_time': get_actual_time[2] if get_actual_time else None,
        }
    
    weather_conditions = get_weather_conditions()
    actual_day = get_current_dates(city)

    context = {
        'actual_day': actual_day[5] if actual_day else None,
        'weather_data': weather_data,
        'search_form': search_form,
        **weather_conditions,
    }
    return context

'''Return all the times for the next days from 3h in 3h'''
def all_times(time):
    all_days_time_context = {}
    if time:
        for i in range(8): #time fro 00:00-21:00
            all_days_time_context[f'time{i}'] = time[i]
    else:
        for i in range(8):
            all_days_time_context[f'time{i}'] = None
    return all_days_time_context

'''Return all the descriptions for the next days from 3h in 3h'''
def all_descriptions(description):
    all_days_description_context = {}
    if description:
        for i in range(1,4): #day1, day2, day3
            for y in range(8): #time from 00:00 to 21:00
                all_days_description_context[f'day{i}_time{y}'] = description[i-1][y]
    else:
        for i in range(1,4):
            for y in range(8):
                all_days_description_context[f'day{i}_time{y}'] = None
    return all_days_description_context

'''Return all the temps for the next days from 3h in 3h'''
def all_temps(temp):
    all_days_temps_context = {}
    if temp:
        for i in range(1,4): #day1, day2, day3
            for y in range(8): #time from 00:00 to 21:00
                all_days_temps_context[f'day{i}_time{y}_temperature'] = temp[i-1][y]
    else:
        for i in range(1,4):
            for y in range(8):
                all_days_temps_context[f'day{i}_time{y}_temperature'] = None

    return all_days_temps_context
    
'''This function is used for POST-search_form'''
def get_cities_weather(request):
    search_form = SearchForm(request.POST)
    if search_form.is_valid():
        city = search_form.cleaned_data['search_city']
        #functions import
        weather_data = get_current_dates(city)
        weather_data_next_days = get_weather_next_days(city)
        weather_conditions = get_weather_conditions()
        sunrise_sunset_time = get_sunrise_sunset_time(city)
        
        all_days_temp = get_all_temps(city)
        all_days_temps_context = all_temps(all_days_temp)
        
        all_days_description = get_all_descriptions(city)
        all_days_description_context = all_descriptions(all_days_description)
        
        all_days_time = get_all_times(city)
        all_days_time_context = all_times(all_days_time)
        
        context = {
            'city': city,
            'search_form': search_form,
            'weather_data_next_days': weather_data_next_days[0] if weather_data_next_days else None,
            'day1_date': weather_data_next_days[1] if weather_data_next_days else None,
            'day2_date': weather_data_next_days[2] if weather_data_next_days else None,
            'day3_date': weather_data_next_days[3] if weather_data_next_days else None,
            
            'weather_data': weather_data[0] if weather_data else None,
            'temperature': weather_data[1] if weather_data else None,
            'min_temp': weather_data[2] if weather_data else None,
            'max_temp': weather_data[3] if weather_data else None,
            'humidity': weather_data[4] if weather_data else None,
            'actual_day': weather_data[5] if weather_data else None,
            
            'sunrise_time': sunrise_sunset_time[0] if sunrise_sunset_time else None,
            'sunset_time': sunrise_sunset_time[1] if sunrise_sunset_time else None,
            'actual_time': sunrise_sunset_time[2] if sunrise_sunset_time else None,
            
            **all_days_time_context,
            **all_days_description_context,
            **all_days_temps_context,
            **weather_conditions,
        }
        return render(request, 'nextdaysweather.html', context)
    else:
        search_form = SearchForm()    
    
'''This function'''
def get_weather_now(request):
    if request.method == "POST":
        post = get_cities_weather(request)
        if post:
            return post
        
    context = get_static_cities_weather()
    return render(request, 'weather_in_capitals.html', context)


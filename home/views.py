from django.shortcuts import render, redirect
from weather import get_current_dates, get_sunrise_sunset_time
from weather_next_days import get_weather_next_days, get_all_temps
from datetime import datetime
from .forms import SearchForm


'''This function return the weather conditions'''
def get_weather_conditions():
    weather_condition_rainy = {
        'light rain': 'rainy',
        'moderate rain': 'rainy',
        'heavy intensity rain': 'rainy',
    }
    
    weather_condition_sunny = {
        'clear sky': 'sunny',
    }
    weather_condition_clouds = {
        'scattered clouds': 'clouds',
        'overcast clouds': 'clouds',
        'few clouds': 'clouds',
        'broken clouds': 'clouds',
    }
    return {
        'weather_condition_rainy': weather_condition_rainy,
        'weather_condition_sunny': weather_condition_sunny,
        'weather_condition_clouds': weather_condition_clouds,
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

'''Return all the temps for next days from 3h in 3h'''
def all_temps(temp):
    all_days_temps_context = {
        #day1
        'day1_time_00': temp[0] if temp else None,
        'day1_time_03': temp[1] if temp else None,
        'day1_time_06': temp[2] if temp else None,
        'day1_time_09': temp[3] if temp else None,
        'day1_time_12': temp[4] if temp else None,
        'day1_time_15': temp[5] if temp else None,
        'day1_time_18': temp[6] if temp else None,
        'day1_time_21': temp[7] if temp else None,
        #day2
        'day2_time_00': temp[8] if temp else None,
        'day2_time_03': temp[9] if temp else None,
        'day2_time_06': temp[10] if temp else None,
        'day2_time_09': temp[11] if temp else None,
        'day2_time_12': temp[12] if temp else None,
        'day2_time_15': temp[13] if temp else None,
        'day2_time_18': temp[14] if temp else None,
        'day2_time_21': temp[15] if temp else None,
        #day3
        'day3_time_00': temp[16] if temp else None,
        'day3_time_03': temp[17] if temp else None,
        'day3_time_06': temp[18] if temp else None,
        'day3_time_09': temp[19] if temp else None,
        'day3_time_12': temp[20] if temp else None,
        'day3_time_15': temp[21] if temp else None,
        'day3_time_18': temp[22] if temp else None,
        'day3_time_21': temp[23] if temp else None,
    }
    return all_days_temps_context
    
'''This function is used for POST-search_form'''
def get_cities_weather(request):
    search_form = SearchForm(request.POST)
    if search_form.is_valid():
        city = search_form.cleaned_data['search_city']
        weather_data = get_current_dates(city)
        weather_data_next_days = get_weather_next_days(city)
        weather_conditions = get_weather_conditions()
        sunrise_sunset_time = get_sunrise_sunset_time(city)
        all_days_temp = get_all_temps(city)
        all_days_temps_context = all_temps(all_days_temp)
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
            
            **all_days_temps_context,
            **weather_conditions,
        }
        return render(request, 'cityweather.html', context)
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
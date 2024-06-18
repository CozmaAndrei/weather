from django.shortcuts import render, redirect
from weather import get_weather
from weather_next_days import get_weather_next_days, get_min_temp_max_temp
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
        data = get_weather(city)
        weather_data[key] = {
            'weather': data[0] if data else None,
            'temperature': data[1] if data else None,
            'min_temp': data[2] if data else None,
            'max_temp': data[3] if data else None,
            'sunrise_time': data[4] if data else None,
            'humidity': data[5] if data else None,
        }
    
    weather_conditions = get_weather_conditions()

    context = {
        'weather_data': weather_data,
        'search_form': search_form,
        **weather_conditions,
    }
    return context

'''This function is used for POST-search_form'''
def get_cities_weather(request):
    search_form = SearchForm(request.POST)
    if search_form.is_valid():
        city = search_form.cleaned_data['search_city']
        weather_data = get_weather(city)
        weather_data_next_days = get_weather_next_days(city)
        max_temp_min_temp = get_min_temp_max_temp(city)
        weather_conditions = get_weather_conditions()
        
        context = {
            'city': city,
            'search_form': search_form,
            'weather_data_next_days': weather_data_next_days[0] if weather_data_next_days else None,
            'day1': weather_data_next_days[1] if weather_data_next_days else None,
            'day2': weather_data_next_days[2] if weather_data_next_days else None,
            'day3': weather_data_next_days[3] if weather_data_next_days else None,
            
            'min_temp_a_day_after': max_temp_min_temp[0] if max_temp_min_temp else None,
            'max_temp_a_day_after': max_temp_min_temp[1] if max_temp_min_temp else None,
            'min_temp_two_days_after': max_temp_min_temp[2] if max_temp_min_temp else None,
            'max_temp_two_days_after': max_temp_min_temp[3] if max_temp_min_temp else None,
            'min_temp_three_days_after': max_temp_min_temp[4] if max_temp_min_temp else None,
            'max_temp_three_days_after': max_temp_min_temp[5] if max_temp_min_temp else None,
            
            
            
            'weather_data': weather_data[0] if weather_data else None,
            'temperature': weather_data[1] if weather_data else None,
            'min_temp': weather_data[2] if weather_data else None,
            'max_temp': weather_data[3] if weather_data else None,
            'sunrise_time': weather_data[4] if weather_data else None,
            'humidity': weather_data[5] if weather_data else None,
            'actual_day': weather_data[6] if weather_data else None,
            'current_time': datetime.now().strftime("%H:%M"),
            'current_data': datetime.now().strftime("%Y-%m-%d"),
            **weather_conditions,
        }
        return render(request, 'cityweather.html', context)
    else:
        search_form = SearchForm()
        
'''This function'''
def get_weather_now(request):
    if request.method == "POST":
        post_response = get_cities_weather(request)
        if post_response:
            return post_response
    
    context = get_static_cities_weather()
    return render(request, 'weather_in_capitals.html', context)
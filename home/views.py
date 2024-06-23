from django.shortcuts import render, redirect
from home.forms import SearchForm
#import helper functions from helper_functions.py
from .helper.helper_functions import get_static_cities_weather, get_cities_weather

'''This function..'''
def show_city_weather(request,city):
    context = get_cities_weather(request,city)
    return render (request, 'nextdaysweather.html', context)

'''This function is the main controler'''
def get_weather_now(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            city = search_form.cleaned_data['search_city']
            return redirect('show_city_weather', city=city)
        else:
            search_form = SearchForm()
        
    context = get_static_cities_weather()
    return render(request, 'weather_in_capitals.html', context)





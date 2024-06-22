from django.shortcuts import render
#import helper functions from helper_functions.py
from .helper.helper_functions import get_static_cities_weather, get_cities_weather

'''This function is the main controler'''
def get_weather_now(request):
    if request.method == "POST":
        post = get_cities_weather(request)
        if post:
            return post
        
    context = get_static_cities_weather()
    return render(request, 'weather_in_capitals.html', context)


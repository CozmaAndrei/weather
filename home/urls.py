from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_weather_now, name='get_weather_now'),
    path('<str:city>/', views.show_city_weather, name='show_city_weather'),
]
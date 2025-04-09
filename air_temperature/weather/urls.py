from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('weather/', views.weather_api, name='weather_api')
]

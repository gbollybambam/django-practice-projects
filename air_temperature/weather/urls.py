from django.urls import path
from django.contrib.auth import views  as auth_views
from . import views

urlpatterns = [
    path('', views.weather_api, name='weather_dashboard'),
    path('get_location/', views.get_location, name='get_location'),
    # authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]

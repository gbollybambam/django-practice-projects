from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import forms
from .views import UserRegisterView, Blog

urlpatterns = [
    path('blog/', Blog, name='blog'),
    path('login/', LoginView.as_view(authentication_form=forms.CustomAuthenticationForm), name='login'),
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

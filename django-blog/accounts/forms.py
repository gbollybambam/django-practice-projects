from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

CustomUser = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'autofocus': True,
        'class': 'form-control'
        }))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
        
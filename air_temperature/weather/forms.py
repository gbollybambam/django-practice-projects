from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class WeatherForm(forms.Form):
    city = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter city name'}),
        label='City'
    )

    lat = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter latitude'}),
        label='Latitude',
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )

    lon = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Longitude'}),
        label='longitude',
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    
    zip_code = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Enter ZIP code(e.g., 12345,us)'}),
        label='ZIP Code'
    )

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        lat = cleaned_data.get('lat')
        lon = cleaned_data.get('lon')
        zip_code = cleaned_data.get('zip_code')

        if sum(bool(x) for x in [city, lat and lon, zip_code]) > 1:
            raise forms.ValidationError(_("Please provide one type of input: city, lat/lon, or ZIP code."))
        if not any([city, lat and lon, zip_code]):
            raise forms.ValidationError(_("Please provide at least one input: lat/lon, or ZIP code."))

        return cleaned_data
    
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

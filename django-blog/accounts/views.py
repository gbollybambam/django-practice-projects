from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from .forms import CustomUserCreationForm



# Create your views here.
class UserRegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog')
        return render(request, 'registration/signup.html', {'form': form})


# api key 
# GET https://newsapi.org/v2/everything?q=Apple&from=2025-04-28&sortBy=popularity&apiKey=API_KEY

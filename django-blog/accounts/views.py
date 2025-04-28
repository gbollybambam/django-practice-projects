from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from blog.models import Post
import requests

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

@login_required
def Blog(request):
    user_posts = Post.objects.all().order_by('-published_at')
    api_key = settings.NEWS_API_KEY
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=' + api_key

    try:
        response = requests.get(url)
        response.raise_for_status()
        api_data = response.json()
        api_posts = api_data.get('articles', [])
    except Exception as e:
        print(f'Error fetching external posts : {e}')
        api_posts = []

    context = {
        'user_posts': user_posts,
        'api_posts': api_posts,
    }

    return render(request, 'blog/blog.html', context)

# api key 
# GET https://newsapi.org/v2/everything?q=Apple&from=2025-04-28&sortBy=popularity&apiKey=API_KEY

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from blog.models import Post
from django.core.paginator import Paginator
import requests
from random import shuffle


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


def get_api_posts():
    try:
        api_key = settings.NEWS_API_KEY
        url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=' + api_key
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        api_data = response.json()
        return api_data.get('articles', [])
    except requests.exceptions.RequestException as e:
        print(f'Error fetching external posts : {e}')
        return []


@login_required
def Blog(request):
    filter_type = request.GET.get('source', 'all')
    user_posts = Post.objects.all().order_by('-published_at')
    api_posts = get_api_posts()

    if filter_type == 'user':
        combined = list(user_posts)
    elif filter_type == 'api':
        combined = api_posts
    else:
        combined = list(user_posts) + api_posts
        shuffle(combined)


    paginator = Paginator(combined, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog.html', {
        'page_obj': page_obj,
        'filter_type': filter_type
    })

# api key 
# GET https://newsapi.org/v2/everything?q=Apple&from=2025-04-28&sortBy=popularity&apiKey=API_KEY

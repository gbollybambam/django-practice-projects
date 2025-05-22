from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from blog.models import Post
from django.core.paginator import Paginator
import requests
from random import shuffle
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm
from django.urls import reverse
# cache system
from django.core.cache import cache


CACHE_TIMEOUT = 60 * 10

# Create your views here.
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

#cached system
def get_cached_api_posts():
    posts = cache.get('newsapi_posts')
    if posts is None:
        posts = get_api_posts()
        cache.set('newsapi_posts', posts, CACHE_TIMEOUT)
    return posts

def serialize_combined_posts(posts):
    serialized = []
    for post in posts:
        if hasattr(post, 'id'):  # User post
            serialized.append({
                'type': 'user',
                'id': post.id
            })
        else:  # API post
            serialized.append({
                'type': 'api',
                'title': post.title,
                'description': post.description,
                'content': post.content,
                'url': post.url,
                'api_index': post.index
            })
    return serialized

def deserialize_combined_posts(serialized):
    user_posts = {p.id: p for p in Post.objects.all()}
    posts = []

    for item in serialized:
        if item['type'] == 'user':
            post = user_posts.get(item['id'])
            if post:
                posts.append(post)
        elif item['type'] == 'api':
            post = APIPost(item, item['api_index'])
            posts.append(post)
    return posts

class APIPost:
    def __init__(self, data, index):
        self.__dict__.update(data)
        self.source = 'api'
        self.index = index

@login_required
def Blog(request):
    filter_type = request.GET.get('source', 'all')
    user_posts = Post.objects.all().order_by('-published_at')
    raw_api_posts = get_cached_api_posts()

    api_posts = [APIPost(post, i) for i, post in enumerate(raw_api_posts)]
    combined = []

    if filter_type == 'user':
        combined = list(user_posts)
        request.session.pop('combined_posts', None)
    elif filter_type == 'api':
        combined = api_posts
        request.session.pop('combined_posts', None)
    else:
        if 'combined_posts' in request.session:
            combined_data = request.session['combined_posts']
            combined = deserialize_combined_posts(combined_data)
        else:
            combined = list(user_posts) + api_posts
            shuffle(combined)
            request.session['combined_posts'] = serialize_combined_posts(combined)
    

    paginator = Paginator(combined, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog.html', {
        'page_obj': page_obj,
        'filter_type': filter_type
    })

@login_required
def BlogDetailView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def api_post_detail(request, index):
    api_posts = get_cached_api_posts()
    try:
        post = api_posts[int(index)]
    except (IndexError, ValueError):
        raise Http404("Post not found.")

    return render(request, 'blog/api_post_detail.html', {
        'post': post
    })

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'
    success_url = '/blog/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        page = self.request.POST.get('page') or self.request.GET.get('page') or '1'
        source = self.request.POST.get('source') or self.request.GET.get('source') or 'all'
        return f"{reverse('blog')}?page={page}&source={source}"


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/edit_post.html'
    success_url = '/blog/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        page = self.request.GET.get('page', '1')
        source = self.request.GET.get('source', 'all')
        return f"{reverse('blog')}?page={page}&source={source}"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = '/blog/'

    def get_success_url(self):
        page = self.request.GET.get('page', '1')
        source = self.request.GET.get('source', 'all')
        return f"{reverse('blog')}?page={page}&source={source}"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

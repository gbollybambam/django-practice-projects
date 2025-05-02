from django.urls import path
from .views import Blog, BlogDetailView, api_post_detail

urlpatterns = [
    path('blog/', Blog, name='blog'),
    path('post/<int:pk>', BlogDetailView, name='post_detail'),
    path('api-post/<int:index>', api_post_detail, name='api_post_detail'),
]

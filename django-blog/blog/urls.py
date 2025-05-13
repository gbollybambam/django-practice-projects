from django.urls import path
from .views import Blog, BlogDetailView, api_post_detail, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', Blog, name='blog'),
    path('post/<int:pk>', BlogDetailView, name='post_detail'),
    path('api-post/<int:index>', api_post_detail, name='api_post_detail'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post')
]

from django.urls import path
from .views import Blog, BlogDetailView

urlpatterns = [
    path('blog/', Blog, name='blog'),
    path('post/<int:pk>', BlogDetailView, name='post_detail'),
]

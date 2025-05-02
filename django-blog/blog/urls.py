from django.urls import path
from .views import Blog, BlogDetailView

urlpatterns = [
    path('blog/', Blog, name='blog'),
    path('blog/<int:pk>', BlogDetailView, name='blog-detail-view')
]
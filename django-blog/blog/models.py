from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Create your models here.
# 🔐 User Authentication & Management (done)
# User registration (done)
# User login/logout (done)
# Password reset via email
# User profile with bio, picture, etc.
# Admin-only dashboard for managing users and posts

# 📝 Blog Features
# Create, edit, delete blog posts (CRUD)
# Rich text editor for posts (use Django CKEditor or TinyMCE)
# Slug URLs for SEO-friendly post links
# Publish/draft options for posts
# Categories/tags for organizing posts
# Comment system (auth + optional guest)
# Like system (users can like posts)
# Pagination on post listing
# Search functionality (basic or full-text)

# 🧩 Dynamic Additions with APIs
# You can integrate these APIs:
# 📰 News API (e.g., NewsAPI.org)
# Pull in tech/news articles for a "Trending" section.
# 🖼️ Unsplash API
# Get dynamic images for your posts or headers.
# ✍️ OpenAI or Hugging Face API
# Generate blog content from prompts or keywords.
# 📊 Weather API / Quote API / Joke API
# Add widgets on your blog’s sidebar for engagement.

# 📱 User Experience & Interface
# Responsive design (use Tailwind CSS or Bootstrap)
# Dark/light mode toggle
# Profile customization (themes, avatars)
# Notifications (e.g., when a post is liked/commented on)
# Bookmark or “Read later” feature

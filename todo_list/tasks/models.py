from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True, help_text="Format: YYYY-MM-DD HH:MM (e.g., 2025-06-01 14:30). Optional.")
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


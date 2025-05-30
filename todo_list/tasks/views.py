from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_at')
    
class TaskDetailView(LoginRequiredMixin, DetailView):
    moodel = Task


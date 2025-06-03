from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.http import require_GET
# Create your views here.

User = get_user_model()

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
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)



@require_GET
def check_username(request):
    username = request.GET.get("username", "").strip()
    if User.objects.filter(username=username).exists():
        return HttpResponse("<p style='color:red'>Username already taken.</p>")
    return HttpResponse("")

@require_GET
def check_email(request):
    email = request.GET.get("email", "").strip()
    if User.objects.filter(email=email).exists():
        return HttpResponse("<p style='color:red'>Email already in use.</p>")
    return HttpResponse("")

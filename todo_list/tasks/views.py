from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
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
    
    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['tasks/partials/task_form_partial.html']
        return [self.template_name]

@login_required
def task_list_view(request):
    user = request.user
    filter_by = request.GET.get("filter", "all")

    if filter_by == "pending":
        pending_tasks = Task.objects.filter(user=user, is_completed=False).order_by('-created_at')
        completed_tasks = Task.objects.none()
        template = 'tasks/partials/pending_tasks.html'
    elif filter_by == "completed":
        pending_tasks = Task.objects.none()
        completed_tasks = Task.objects.filter(user=user, is_completed=True).order_by('-created_at')
        template = 'tasks/partials/completed_tasks.html'
    else:
        pending_tasks = Task.objects.filter(user=user, is_completed=False).order_by('-created_at')
        completed_tasks = Task.objects.filter(user=user, is_completed=True).order_by('-created_at')
        template = 'tasks/task_list.html'

    context = {
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "active_filter": filter_by,
    }

    return render(request, template, context)


    
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

@login_required
@require_POST
def Toggle_task_completion(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = not task.is_completed
    task.save()

    user = request.user

    pending_tasks = Task.objects.filter(user=user, is_completed=False).order_by('-created_at')
    completed_tasks = Task.objects.filter(user=user, is_completed=True).order_by('-created_at')


    return render(request, "tasks/partials/task_lists_partial.html", {'pending_tasks': pending_tasks, 'completed_tasks': completed_tasks}) 
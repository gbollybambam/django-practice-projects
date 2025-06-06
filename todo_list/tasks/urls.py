from django.urls import path
from .views import TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView, Toggle_task_completion
from . import views

urlpatterns = [
    path('', views.task_list_view, name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('detail-view/<int:pk>', TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]

htmx_patterns = [
    path("check-username/", views.check_username, name="check_username"),
    path("check-email/", views.check_email, name="check_email"),
    path('tasks/<int:pk>/toggle/', Toggle_task_completion, name='task_toggle_complete'),
]

urlpatterns += htmx_patterns
from django.contrib import admin
from django.urls import path, include
from todo.views import HomePageView, TaskCreateView, TaskUpdateView, TaskDeleteView, generate_sample_tasks, bulk_task_action

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', HomePageView.as_view(), name='home'),
    path('task/add', TaskCreateView.as_view(), name='task-add'),
    path('task/<int:pk>/edit', TaskUpdateView.as_view(), name='task-edit'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='task-delete'),
    path('task/generate-sample', generate_sample_tasks, name='task-generate-sample'),
    path('task/bulk-action', bulk_task_action, name='task-bulk-action'),
]
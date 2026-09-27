from django.contrib import admin
from django.urls import path, include
from todo.views import (
    HomePageView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    generate_sample_tasks, bulk_task_action,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', HomePageView.as_view(), name='home'),
    path('task/add', TaskCreateView.as_view(), name='task-add'),
    path('task/<int:pk>/edit', TaskUpdateView.as_view(), name='task-edit'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='task-delete'),
    path('task/generate-sample', generate_sample_tasks, name='task-generate-sample'),
    path('task/bulk-action', bulk_task_action, name='task-bulk-action'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/add', CategoryCreateView.as_view(), name='category-add'),
    path('categories/<int:pk>/edit', CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),
]
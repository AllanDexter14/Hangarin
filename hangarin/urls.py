from django.contrib import admin
from django.urls import path, include
from todo.views import (
    HomePageView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    generate_sample_tasks, bulk_task_action,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    PriorityListView, PriorityCreateView, PriorityUpdateView, PriorityDeleteView,
    SubTaskListView, SubTaskCreateView, SubTaskUpdateView, SubTaskDeleteView,
    NoteListView, NoteCreateView, NoteUpdateView, NoteDeleteView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('pwa.urls')),
    
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

    path('priorities/', PriorityListView.as_view(), name='priority-list'),
    path('priorities/add', PriorityCreateView.as_view(), name='priority-add'),
    path('priorities/<int:pk>/edit', PriorityUpdateView.as_view(), name='priority-edit'),
    path('priorities/<int:pk>/delete', PriorityDeleteView.as_view(), name='priority-delete'),

    path('subtasks/', SubTaskListView.as_view(), name='subtask-list'),
    path('subtasks/add', SubTaskCreateView.as_view(), name='subtask-add'),
    path('subtasks/<int:pk>/edit', SubTaskUpdateView.as_view(), name='subtask-edit'),
    path('subtasks/<int:pk>/delete', SubTaskDeleteView.as_view(), name='subtask-delete'),

    path('notes/', NoteListView.as_view(), name='note-list'),
    path('notes/add', NoteCreateView.as_view(), name='note-add'),
    path('notes/<int:pk>/edit', NoteUpdateView.as_view(), name='note-edit'),
    path('notes/<int:pk>/delete', NoteDeleteView.as_view(), name='note-delete'),
]
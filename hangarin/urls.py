from django.contrib import admin
from django.urls import path, include
from todo.views import HomePageView, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', HomePageView.as_view(), name='home'),
    path('task/add', TaskCreateView.as_view(), name='task-add'),
    path('task/<int:pk>/edit', TaskUpdateView.as_view(), name='task-edit'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='task-delete'),
]
from django.forms import ModelForm
from .models import Task, Category, Priority, SubTask, Note


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "deadline", "status", "category", "priority"]


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class PriorityForm(ModelForm):
    class Meta:
        model = Priority
        fields = ["name"]


class SubTaskForm(ModelForm):
    class Meta:
        model = SubTask
        fields = ["parent_task", "title", "status"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["parent_task"].queryset = Task.objects.filter(user=user)


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ["task", "content"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["task"].queryset = Task.objects.filter(user=user)
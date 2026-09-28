from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from faker import Faker
import random
from .models import Task, Priority, Category, SubTask, Note
from .forms import TaskForm, CategoryForm, PriorityForm, SubTaskForm, NoteForm

fake = Faker()


class HomePageView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "home.html"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        query = self.request.GET.get("q")

        if query:
            qs = qs.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.filter(user=self.request.user).count()
        context["completed_tasks"] = Task.objects.filter(user=self.request.user, status="Completed").count()
        context["pending_tasks"] = Task.objects.filter(user=self.request.user, status="Pending").count()
        return context

    def get_ordering(self):
        allowed = ["title", "deadline", "status"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "title"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


@login_required
def generate_sample_tasks(request):
    statuses = ["Pending", "In Progress", "Completed"]
    priorities = list(Priority.objects.all())
    categories = list(Category.objects.all())

    for _ in range(5):
        task = Task.objects.create(
            user=request.user,
            title=fake.sentence(nb_words=5),
            description=fake.paragraph(nb_sentences=3),
            deadline=timezone.make_aware(fake.date_time_this_month()),
            status=fake.random_element(elements=statuses),
            category=random.choice(categories),
            priority=random.choice(priorities),
        )

        for _ in range(random.randint(1, 3)):
            SubTask.objects.create(
                parent_task=task,
                title=fake.sentence(nb_words=4),
                status=fake.random_element(elements=statuses),
            )

        for _ in range(random.randint(1, 2)):
            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2),
            )

    return redirect("home")

@login_required
def bulk_task_action(request):
    if request.method == "POST":
        task_ids = request.POST.getlist("selected_tasks")
        action = request.POST.get("action")

        tasks = Task.objects.filter(id__in=task_ids, user=request.user)

        if action == "complete":
            tasks.update(status="Completed")
            return redirect("home")

        elif action == "delete":
            return render(request, "task_bulk_confirm_delete.html", {"tasks": tasks})

        elif action == "confirm_delete":
            tasks.delete()
            return redirect("home")

    return redirect("home")

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = "categories"
    template_name = "category_list.html"
    paginate_by = 10


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("category-list")


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("category-list")


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "category_confirm_delete.html"
    success_url = reverse_lazy("category-list")

class UserFormKwargsMixin:
    """Passes the logged-in user into the form so dropdowns can be filtered."""
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class ModelNameMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model._meta.verbose_name.title()
        return context


class PriorityListView(LoginRequiredMixin, ListView):
    model = Priority
    context_object_name = "priorities"
    template_name = "priority_list.html"
    paginate_by = 10
    ordering = ["name"]


class PriorityCreateView(LoginRequiredMixin, ModelNameMixin, CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = "crud_form.html"
    success_url = reverse_lazy("priority-list")


class PriorityUpdateView(LoginRequiredMixin, ModelNameMixin, UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = "crud_form.html"
    success_url = reverse_lazy("priority-list")


class PriorityDeleteView(LoginRequiredMixin, ModelNameMixin, DeleteView):
    model = Priority
    template_name = "crud_confirm_delete.html"
    success_url = reverse_lazy("priority-list")


class SubTaskListView(LoginRequiredMixin, ListView):
    model = SubTask
    context_object_name = "subtasks"
    template_name = "subtask_list.html"
    paginate_by = 10

    def get_queryset(self):
        return (SubTask.objects
                .filter(parent_task__user=self.request.user)
                .select_related("parent_task")
                .order_by("parent_task__title", "title"))


class SubTaskCreateView(LoginRequiredMixin, UserFormKwargsMixin, ModelNameMixin, CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "crud_form.html"
    success_url = reverse_lazy("subtask-list")

class SubTaskUpdateView(LoginRequiredMixin, UserFormKwargsMixin, ModelNameMixin, UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "crud_form.html"
    success_url = reverse_lazy("subtask-list")

    def get_queryset(self):
        return SubTask.objects.filter(parent_task__user=self.request.user)


class SubTaskDeleteView(LoginRequiredMixin, ModelNameMixin, DeleteView):
    model = SubTask
    template_name = "crud_confirm_delete.html"
    success_url = reverse_lazy("subtask-list")

    def get_queryset(self):
        return SubTask.objects.filter(parent_task__user=self.request.user)



class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = "notes"
    template_name = "note_list.html"
    paginate_by = 10

    def get_queryset(self):
        return (Note.objects
                .filter(task__user=self.request.user)
                .select_related("task")
                .order_by("-created_at"))


class NoteCreateView(LoginRequiredMixin, UserFormKwargsMixin, ModelNameMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "crud_form.html"
    success_url = reverse_lazy("note-list")


class NoteUpdateView(LoginRequiredMixin, UserFormKwargsMixin, ModelNameMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "crud_form.html"
    success_url = reverse_lazy("note-list")

    def get_queryset(self):
        return Note.objects.filter(task__user=self.request.user)


class NoteDeleteView(LoginRequiredMixin, ModelNameMixin, DeleteView):
    model = Note
    template_name = "crud_confirm_delete.html"
    success_url = reverse_lazy("note-list")

    def get_queryset(self):
        return Note.objects.filter(task__user=self.request.user)
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from todo.models import Priority, Category, Task, SubTask, Note

fake = Faker()


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def handle(self, *args, **options):
        priority_names = ["High", "Medium", "Low", "Critical", "Optional"]
        for name in priority_names:
            Priority.objects.get_or_create(name=name)

        category_names = ["Work", "School", "Personal", "Finance", "Projects"]
        for name in category_names:
            Category.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS("Priorities and Categories created!"))

        statuses = ["Pending", "In Progress", "Completed"]
        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        for _ in range(10):
            Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=statuses),
                category=fake.random_element(elements=categories),
                priority=fake.random_element(elements=priorities),
            )

        self.stdout.write(self.style.SUCCESS("10 Tasks created!"))

        tasks = Task.objects.all()

        for task in tasks:
            for _ in range(2):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=statuses),
                )

        self.stdout.write(self.style.SUCCESS("SubTasks created!"))

        for task in tasks:
            for _ in range(1):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )

        self.stdout.write(self.style.SUCCESS("Notes created!"))
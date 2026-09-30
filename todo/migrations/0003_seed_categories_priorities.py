from django.db import migrations

CATEGORIES = ["Work", "School", "Personal", "Finance", "Projects"]
PRIORITIES = ["high", "medium", "low", "critical", "optional"]


def seed(apps, schema_editor):
    Category = apps.get_model("todo", "Category")
    Priority = apps.get_model("todo", "Priority")
    for name in CATEGORIES:
        Category.objects.get_or_create(name=name)
    for name in PRIORITIES:
        Priority.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0002_task_user"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
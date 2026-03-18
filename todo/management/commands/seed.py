import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from todo.models import Task, Note, SubTask, Category, Priority


class Command(BaseCommand):
    help = "Seed fake data for Task, Note, and SubTask."

    def add_arguments(self, parser):
        parser.add_argument("--tasks", type=int, default=20)
        parser.add_argument("--notes", type=int, default=60)
        parser.add_argument("--subtasks", type=int, default=80)

    def handle(self, *args, **options):
        fake = Faker()

        categories = list(Category.objects.all())
        priorities = list(Priority.objects.all())

        if not categories or not priorities:
            self.stdout.write(self.style.ERROR(
                "Please add Category and Priority records first (manually in admin)."
            ))
            return

        statuses = ["Pending", "In Progress", "Completed"]

        # Create Tasks
        tasks_to_create = options["tasks"]
        created_tasks = []
        for _ in range(tasks_to_create):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=statuses),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                category=random.choice(categories),
                priority=random.choice(priorities),
            )
            created_tasks.append(task)

        # Create Notes
        notes_to_create = options["notes"]
        for _ in range(notes_to_create):
            Note.objects.create(
                task=random.choice(created_tasks),
                content=fake.paragraph(nb_sentences=3),
            )

        # Create SubTasks
        subtasks_to_create = options["subtasks"]
        for _ in range(subtasks_to_create):
            SubTask.objects.create(
                parent_task=random.choice(created_tasks),
                title=fake.sentence(nb_words=5),
                status=fake.random_element(elements=statuses),
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded: {tasks_to_create} tasks, {notes_to_create} notes, {subtasks_to_create} subtasks."
        ))
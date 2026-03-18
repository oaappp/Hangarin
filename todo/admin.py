from django.contrib import admin
from .models import Task, SubTask, Note, Category, Priority


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Display title, status, deadline, priority, category.
    list_display = ("title", "status", "deadline", "priority", "category")

    # Add filters for status, priority, category.
    list_filter = ("status", "priority", "category")

    # Enable search on title and description.
    search_fields = ("title", "description")


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    # Display title, status, and custom field parent_task_name.
    list_display = ("title", "status", "parent_task_name")

    # Filter by status.
    list_filter = ("status",)

    # Enable search on title.
    search_fields = ("title",)

    @admin.display(description="Parent Task")
    def parent_task_name(self, obj):
        return obj.parent_task.title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Display just the name field.
    list_display = ("name",)

    # Make searchable.
    search_fields = ("name",)


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    # Display just the name field.
    list_display = ("name",)

    # Make searchable.
    search_fields = ("name",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # Display task, content, and created_at.
    list_display = ("task", "content", "created_at")

    # Filter by created_at.
    list_filter = ("created_at",)

    # Enable search on content.
    search_fields = ("content",)
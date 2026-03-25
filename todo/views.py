from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Task, Category, Priority, Note, SubTask
from .forms import TaskForm, CategoryForm, PriorityForm, NoteForm, SubTaskForm

from django.contrib.auth import login
from .forms import SignUpForm

from django.db.models.deletion import ProtectedError
from django.contrib import messages

def signup_view(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)  # auto login after signup
        return redirect("todo:dashboard")

    return render(request, "registration/signup.html", {"form": form})


# -------------------------
# DASHBOARD + TASK CRUD
# -------------------------
@login_required
def dashboard(request):
    now = timezone.now()

    pending = Task.objects.filter(status="Pending").order_by("deadline")
    in_progress = Task.objects.filter(status="In Progress").order_by("deadline")
    completed = Task.objects.filter(status="Completed").order_by("-updated_at")

    context = {
        "now": now,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
        "total_tasks": Task.objects.count(),
        "pending_count": pending.count(),
        "in_progress_count": in_progress.count(),
        "completed_count": completed.count(),
        "overdue_count": Task.objects.filter(deadline__lt=now).exclude(status="Completed").count(),
        "recent_tasks": Task.objects.order_by("-updated_at")[:10],
    }
    return render(request, "todo/dashboard.html", context)


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("todo:dashboard")
    return render(request, "todo/task_form.html", {"form": form, "title": "Add Task"})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "todo/task_detail.html", {"task": task})


@login_required
def task_list(request):
    pending = Task.objects.filter(status="Pending").order_by("deadline")
    in_progress = Task.objects.filter(status="In Progress").order_by("deadline")
    completed = Task.objects.filter(status="Completed").order_by("-updated_at")

    context = {
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
        "pending_count": pending.count(),
        "in_progress_count": in_progress.count(),
        "completed_count": completed.count(),
    }
    return render(request, "todo/task_list.html", context)


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("todo:task_detail", pk=task.pk)
    return render(request, "todo/task_form.html", {"form": form, "title": "Edit Task"})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("todo:dashboard")
    return render(request, "todo/confirm_delete.html", {
        "object": task,
        "cancel_url": "todo:dashboard",
        "title": "Delete Task",
        "message": f"Are you sure you want to delete '{task.title}'?"
    })


# -------------------------
# CATEGORY CRUD
# -------------------------
@login_required
def category_list(request):
    categories = Category.objects.order_by("name")
    return render(request, "todo/category_list.html", {"categories": categories})


@login_required
def category_create(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("todo:category_list")
    return render(request, "todo/simple_form.html", {"form": form, "title": "Add Category", "back_url": "todo:category_list"})


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("todo:category_list")
    return render(request, "todo/simple_form.html", {"form": form, "title": "Edit Category", "back_url": "todo:category_list"})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        try:
            category.delete()
            messages.success(request, "Category deleted successfully.")
        except ProtectedError:
            messages.error(
                request,
                "This category cannot be deleted because it is still assigned to one or more tasks."
            )
        return redirect("todo:category_list")

    return render(request, "todo/confirm_delete.html", {
        "object": category,
        "cancel_url": "todo:category_list",
        "title": "Delete Category",
        "message": f"Are you sure you want to delete '{category.name}'?"
    })


# -------------------------
# PRIORITY CRUD
# -------------------------
@login_required
def priority_list(request):
    priorities = Priority.objects.order_by("name")
    return render(request, "todo/priority_list.html", {"priorities": priorities})


@login_required
def priority_create(request):
    form = PriorityForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("todo:priority_list")
    return render(request, "todo/simple_form.html", {"form": form, "title": "Add Priority", "back_url": "todo:priority_list"})


@login_required
def priority_update(request, pk):
    priority = get_object_or_404(Priority, pk=pk)
    form = PriorityForm(request.POST or None, instance=priority)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("todo:priority_list")
    return render(request, "todo/simple_form.html", {"form": form, "title": "Edit Priority", "back_url": "todo:priority_list"})


@login_required
def priority_delete(request, pk):
    priority = get_object_or_404(Priority, pk=pk)

    if request.method == "POST":
        try:
            priority.delete()
            messages.success(request, "Priority deleted successfully.")
        except ProtectedError:
            messages.error(
                request,
                "This priority cannot be deleted because it is still assigned to one or more tasks."
            )
        return redirect("todo:priority_list")

    return render(request, "todo/confirm_delete.html", {
        "object": priority,
        "cancel_url": "todo:priority_list",
        "title": "Delete Priority",
        "message": f"Are you sure you want to delete '{priority.name}'?"
    })


# -------------------------
# NOTE CRUD
# -------------------------
@login_required
def note_list(request):
    notes = Note.objects.select_related("task").order_by("-created_at")
    return render(request, "todo/note_list.html", {"notes": notes})


@login_required
def note_create(request):
    form = NoteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("todo:note_list")
    return render(request, "todo/simple_form.html", {"form": form, "title": "Add Note", "back_url": "todo:note_list"})


@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    form = NoteForm(request.POST or None, instance=note)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("todo:note_list")
    return render(request, "todo/simple_form.html", {"form": form, "title": "Edit Note", "back_url": "todo:note_list"})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
        return redirect("todo:note_list")
    return render(request, "todo/confirm_delete.html", {
        "object": note,
        "cancel_url": "todo:note_list",
        "title": "Delete Note",
        "message": "Are you sure you want to delete this note?"
    })


# -------------------------
# SUBTASK CRUD
# -------------------------
@login_required
def subtask_list(request):
    subtasks = SubTask.objects.select_related("parent_task").order_by("-created_at")
    return render(request, "todo/subtask_list.html", {"subtasks": subtasks})


@login_required
def subtask_create(request):
    form = SubTaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("todo:subtask_list")
    return render(request, "todo/simple_form.html", {"form": form, "title": "Add SubTask", "back_url": "todo:subtask_list"})


@login_required
def subtask_update(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    form = SubTaskForm(request.POST or None, instance=subtask)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("todo:subtask_list")
    return render(request, "todo/simple_form.html", {"form": form, "title": "Edit SubTask", "back_url": "todo:subtask_list"})


@login_required
def subtask_delete(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    if request.method == "POST":
        subtask.delete()
        return redirect("todo:subtask_list")
    return render(request, "todo/confirm_delete.html", {
        "object": subtask,
        "cancel_url": "todo:subtask_list",
        "title": "Delete SubTask",
        "message": f"Are you sure you want to delete '{subtask.title}'?"
    })
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Task, Category, Priority, Note, SubTask


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "deadline", "status", "priority", "category"]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ["name"]


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["task", "content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4}),
        }


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ["parent_task", "title", "status"]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
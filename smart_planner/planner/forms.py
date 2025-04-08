from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudyTask

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class TaskForm(forms.ModelForm):
    class Meta:
        model = StudyTask
        fields = ['subject', 'description', 'due_date', 'completed']

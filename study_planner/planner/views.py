from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import StudyTask
from .forms import StudyTaskForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


# Create your views here.

def home(request):
    return render(request, 'planner/home.html')



@login_required
def dashboard(request):
    # Fetch tasks for the logged-in user
    tasks = StudyTask.objects.filter(user=request.user)

    # Initialize the task form
    form = StudyTaskForm()

    # Handle the form submission for adding tasks
    if request.method == "POST":
        form = StudyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

    # Prepare the tasks data for Task Overview
    total_tasks_count = tasks.count()
    completed_tasks_count = tasks.filter(completed=True).count()
    pending_tasks_count = total_tasks_count - completed_tasks_count

    # Prepare the tasks data for FullCalendar
    tasks_data = [
        {
            'subject': task.subject,
            'date': task.date.strftime('%Y-%m-%d'),
            'time': task.time.strftime('%H:%M'),
            'completed': task.completed
        }
        for task in tasks
    ]

    # Render the template with tasks and form, and pass the tasks data for calendar and task overview
    return render(request, 'planner/dashboard.html', {
        'tasks': tasks,
        'form': form,
        'tasks_data': json.dumps(tasks_data),
        'total_tasks_count': total_tasks_count,
        'completed_tasks_count': completed_tasks_count,
        'pending_tasks_count': pending_tasks_count
    })





def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'planner/register.html')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken. Please choose a different one.")
            return render(request, 'planner/register.html')

        try:
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')

        except IntegrityError:
            # Handle any database errors (e.g., unique constraint violations)
            messages.error(request, "An error occurred while creating your account. Please try again.")
            return render(request, 'planner/register.html')

    return render(request, 'planner/register.html')

def login_view(request):
    print("Login view triggered.") 

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'planner/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')




@login_required
def edit_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)
    
    if request.method == "POST":
        form = StudyTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudyTaskForm(instance=task)
    
    return render(request, 'planner/edit_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')


@login_required
def send_task_reminders(request):
    upcoming_tasks = StudyTask.objects.filter(user=request.user, date__gte=now(), date__lte=now() + timedelta(days=1))

    for task in upcoming_tasks:
        send_mail(
            subject=f"Reminder: {task.subject} Study Session",
            message=f"Don't forget your study session for {task.subject} on {task.date} at {task.time}.",
            from_email='your-email@gmail.com',
            recipient_list=[request.user.email],
        )

    return redirect('dashboard')

from django.contrib.auth.decorators import login_required

@login_required
def send_task_reminders(request):
    upcoming_tasks = StudyTask.objects.filter(user=request.user, date__gte=now(), date__lte=now() + timedelta(days=1))

    for task in upcoming_tasks:
        send_mail(
            subject=f"Reminder: {task.subject} Study Session",
            message=f"Don't forget your study session for {task.subject} on {task.date} at {task.time}.",
            from_email='your-email@gmail.com',
            recipient_list=[request.user.email],
        )

    return redirect('dashboard')

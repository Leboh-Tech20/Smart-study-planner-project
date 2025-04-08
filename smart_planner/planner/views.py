
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.serializers.json import DjangoJSONEncoder
from .forms import RegisterForm, TaskForm
from .models import StudyTask, StudyGoal
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404





# Home
def home(request):
    if request.user.is_authenticated:
        total_tasks = StudyTask.objects.filter(user=request.user).count()
        completed_tasks = StudyTask.objects.filter(user=request.user, completed=True).count()
        pending_tasks = StudyTask.objects.filter(user=request.user, completed=False).count()

        return render(request, 'planner/home.html', {
            'tasks_count': total_tasks,
            'completed_tasks_count': completed_tasks,
            'pending_tasks_count': pending_tasks,
        })
    else:
        # 👇 render welcome page instead of redirecting to login
        return render(request, 'planner/welcome.html')



# Register

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'planner/register.html', {'form': form})

# Login

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'planner/login.html', {'form': form})

# Logout

def user_logout(request):
    logout(request)
    return redirect('welcome')  # Redirect to the named URL for 'welcome'

# Task list + filtering
@login_required
def task_list(request):
    if request.method == 'POST' and 'subject' in request.POST:
        # Form submission to add a new task
        subject = request.POST['subject']
        description = request.POST['description']
        due_date = request.POST['due_date']
        completed = request.POST['completed'] == 'True'
        reminder_time = request.POST.get('reminder_time', None)  # Get reminder time from the form

        # Convert reminder_time to integer if provided
        if reminder_time:
            reminder_time = int(reminder_time)

        # Create new task with reminder_time
        new_task = StudyTask.objects.create(
            user=request.user,
            subject=subject,
            description=description,
            due_date=due_date,
            completed=completed,
            reminder_time=reminder_time  # Store reminder time
        )

        # Redirect to task list to see the added task
        return redirect('tasks')

    elif request.method == 'POST' and 'toggle_task' in request.POST:
        # Handle toggling the task completion status
        task_id = request.POST['task_id']
        task = get_object_or_404(StudyTask, id=task_id, user=request.user)

        # Toggle task completion
        task.completed = not task.completed
        task.save()

        return redirect('tasks')

    # If GET request, display tasks
    tasks = StudyTask.objects.filter(user=request.user)

    # Handle filtering if needed
    filter_status = request.GET.get('filter')
    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'incomplete':
        tasks = tasks.filter(completed=False)

    return render(request, 'planner/tasks.html', {'tasks': tasks})


# Pomodoro
@login_required
def pomodoro_timer(request):
    return render(request, 'planner/pomodoro.html')

# Study Tips Page
@login_required
def study_tips(request):
    return render(request, 'planner/study_tips.html')

# Study Goals
@login_required
def study_goals(request):
    goal, created = StudyGoal.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        goal.weekly_hours = request.POST.get('weekly_hours', goal.weekly_hours)
        goal.target_tasks = request.POST.get('target_tasks', goal.target_tasks)
        goal.save()
    return render(request, 'planner/goals.html', {'goal': goal})

# Progress Tracker
@login_required
def progress_tracker(request):
    tasks = StudyTask.objects.filter(user=request.user)
    total = tasks.count()
    completed = tasks.filter(completed=True).count()

    if total > 0:
        percent_complete = (completed / total) * 100
    else:
        percent_complete = 0  # Avoid division by zero
    
    return render(request, 'planner/progress.html', {
        'total': total,
        'completed': completed,
        'percent_complete': percent_complete,
    })


# Calendar
@login_required
def calendar_view(request):
    tasks = StudyTask.objects.filter(user=request.user)
    
    events = []
    for task in tasks:
        events.append({
            'title': task.subject,
            'start': task.due_date.strftime('%Y-%m-%d'),
            'end': task.due_date.strftime('%Y-%m-%d'),
            'description': task.description,
        })
    
    # Print to verify the data
    print(events)  # Check in the terminal or console
    
    events_json = json.dumps(events)
    
    return render(request, 'planner/calendar.html', {
        'events_json': events_json
    })

def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')  # if already logged in, go to home
    return render(request, 'planner/welcome.html')





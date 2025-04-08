from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('welcome/', views.welcome, name='welcome'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('tasks/', views.task_list, name='tasks'),
    path('pomodoro/', views.pomodoro_timer, name='pomodoro'),
    path('study-tips/', views.study_tips, name='study_tips'),
    path('progress/', views.progress_tracker, name='progress'),
    path('goals/', views.study_goals, name='goals'),
    path('calendar/', views.calendar_view, name='calendar'),
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
